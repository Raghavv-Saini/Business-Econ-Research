from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler


def compute_paired_ablation(df_agg: pd.DataFrame, arm_a: str, arm_b: str) -> dict[str, Any]:
    """Compute paired score delta, t-test, Wilcoxon test, and decision-flip rate between two arms."""
    a = df_agg[df_agg["evaluation_mode"] == arm_a][["record_id", "composite_score", "predicted_invest"]].rename(
        columns={"composite_score": "score_a", "predicted_invest": "pred_a"}
    )
    b = df_agg[df_agg["evaluation_mode"] == arm_b][["record_id", "composite_score", "predicted_invest"]].rename(
        columns={"composite_score": "score_b", "predicted_invest": "pred_b"}
    )
    merged = pd.merge(a, b, on="record_id", how="inner").dropna()
    n = len(merged)
    if n == 0:
        return {"n": 0, "mean_delta": None, "sd_delta": None, "t_stat": None, "p_value_t": None, "w_stat": None, "p_value_wilcoxon": None, "flip_rate": None}

    delta = merged["score_a"].astype(float) - merged["score_b"].astype(float)
    mean_delta = float(delta.mean())
    sd_delta = float(delta.std(ddof=1)) if n > 1 else 0.0

    if n > 1 and sd_delta > 0:
        t_res = stats.ttest_rel(merged["score_a"].astype(float), merged["score_b"].astype(float))
        t_stat, p_t = float(t_res.statistic), float(t_res.pvalue)
    else:
        t_stat, p_t = 0.0, 1.0

    non_zero = delta[delta != 0]
    if len(non_zero) >= 1:
        try:
            w_res = stats.wilcoxon(non_zero)
            w_stat, p_w = float(w_res.statistic), float(w_res.pvalue)
        except Exception:
            w_stat, p_w = None, None
    else:
        w_stat, p_w = 0.0, 1.0

    pred_a = merged["pred_a"].round().astype(int)
    pred_b = merged["pred_b"].round().astype(int)
    flip_rate = float((pred_a != pred_b).mean())

    return {
        "n": int(n),
        "arm_a": arm_a,
        "arm_b": arm_b,
        "mean_delta": mean_delta,
        "sd_delta": sd_delta,
        "t_stat": t_stat,
        "p_value_t": p_t,
        "w_stat": w_stat,
        "p_value_wilcoxon": p_w,
        "flip_rate": flip_rate,
    }


def compute_oof_ensemble(
    df: pd.DataFrame,
    y_col: str,
    feature_cols: list[str],
    n_splits: int = 5,
) -> dict[str, Any]:
    """Compute stratified out-of-fold logistic regression metrics guarding against sparse folds."""
    sub = df[feature_cols + [y_col]].dropna().copy()
    if len(sub) < 10 or sub[y_col].nunique() < 2:
        return {"n": int(len(sub)), "roc_auc": None, "pr_auc": None, "brier_score": None, "oof_probs": []}

    y = sub[y_col].astype(int).to_numpy()
    X = sub[feature_cols].astype(float).to_numpy()
    min_cls = int(np.bincount(y).min())
    k = min(n_splits, min_cls)
    if k < 2:
        return {"n": int(len(sub)), "roc_auc": None, "pr_auc": None, "brier_score": None, "oof_probs": []}

    skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
    oof_probs = np.zeros(len(sub), dtype=float)
    for train_idx, val_idx in skf.split(X, y):
        scaler = StandardScaler()
        X_tr = scaler.fit_transform(X[train_idx])
        X_va = scaler.transform(X[val_idx])
        clf = LogisticRegression(max_iter=1000, random_state=42)
        clf.fit(X_tr, y[train_idx])
        oof_probs[val_idx] = clf.predict_proba(X_va)[:, 1]

    return {
        "n": int(len(sub)),
        "features": feature_cols,
        "n_splits": int(k),
        "roc_auc": float(roc_auc_score(y, oof_probs)),
        "pr_auc": float(average_precision_score(y, oof_probs)),
        "brier_score": float(brier_score_loss(y, oof_probs)),
        "oof_probs": [float(p) for p in oof_probs],
    }


def _cronbach_alpha(matrix: np.ndarray) -> float | None:
    if matrix.shape[0] < 3 or matrix.shape[1] < 2:
        return None
    item_vars = matrix.var(axis=0, ddof=1)
    total_var = matrix.sum(axis=1).var(ddof=1)
    if total_var <= 0:
        return None
    k = matrix.shape[1]
    return float((k / (k - 1)) * (1.0 - item_vars.sum() / total_var))


def _fit_glm_logit(
    df: pd.DataFrame,
    y_col: str,
    x_cols: list[str],
    weight_col: str | None = None,
) -> dict[str, Any]:
    cols = [y_col, *x_cols] + ([weight_col] if weight_col else [])
    sub = df[cols].dropna().copy()
    if len(sub) < 12 or sub[y_col].nunique() < 2:
        return {"n": int(len(sub)), "converged": False}

    X = sm.add_constant(sub[x_cols].astype(float), has_constant="add")
    y = sub[y_col].astype(float)
    freq_w = sub[weight_col].astype(float) if weight_col else None
    try:
        model = sm.GLM(y, X, family=sm.families.Binomial(), freq_weights=freq_w)
        res = model.fit(maxiter=200)
        return {
            "n": int(len(sub)),
            "converged": bool(res.converged),
            "pseudo_r2_mcfadden": float(1.0 - res.deviance / res.null_deviance) if res.null_deviance > 0 else None,
            "aic": float(res.aic),
            "params": {k: float(v) for k, v in res.params.items()},
            "pvalues": {k: float(v) for k, v in res.pvalues.items()},
            "bse": {k: float(v) for k, v in res.bse.items()},
        }
    except Exception as exc:
        return {"n": int(len(sub)), "converged": False, "error": str(exc)}


def _binary_eval_metrics(y_true: np.ndarray, probs: np.ndarray) -> dict[str, Any]:
    if len(y_true) < 4 or len(np.unique(y_true)) < 2:
        return {"n": int(len(y_true)), "roc_auc": None}
    probs = np.clip(probs, 1e-6, 1.0 - 1e-6)
    raw_preds = (probs >= 0.5).astype(int)
    base_rate = float(y_true.mean())
    thresh = float(np.quantile(probs, 1.0 - base_rate))
    matched_preds = (probs >= thresh).astype(int)
    return {
        "n": int(len(y_true)),
        "base_rate": base_rate,
        "roc_auc": float(roc_auc_score(y_true, probs)),
        "pr_auc": float(average_precision_score(y_true, probs)),
        "brier_score": float(brier_score_loss(y_true, probs)),
        "confusion_raw_05": confusion_matrix(y_true, raw_preds).tolist(),
        "confusion_baserate_matched": confusion_matrix(y_true, matched_preds).tolist(),
        "baserate_threshold": thresh,
    }


def _load_records(jsonl_paths: list[Path]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for p in jsonl_paths:
        if not p.exists():
            continue
        with p.open("r", encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                rec = json.loads(line)
                fin = (rec.get("t0_payload") or {}).get("financials") or {}
                out = rec.get("outcomes") or {}
                rows.append(
                    {
                        "record_id": rec["record_id"],
                        "track": rec.get("track"),
                        "t0_year": rec.get("t0_year"),
                        "prelim_stratum": (rec.get("meta") or {}).get("prelim_stratum"),
                        "offering_amount": fin.get("offering_amount"),
                        "total_assets": fin.get("assets_recent", fin.get("total_assets")),
                        "revenues": fin.get("revenue_recent", fin.get("revenues")),
                        "employees": fin.get("employees"),
                        "funded_outcome": out.get("funded_outcome"),
                        "survival_3y_outcome": out.get("survival_3y_outcome"),
                        "winner_breakout_outcome": out.get("winner_breakout_outcome"),
                        "funding_ratio": out.get("funding_ratio"),
                    }
                )
    return pd.DataFrame(rows)


def _generate_figures(
    df_agg: pd.DataFrame,
    df_t1: pd.DataFrame,
    figures_dir: Path,
) -> None:
    figures_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"figure.dpi": 180, "font.size": 10})

    # Fig 1: Blinding / Memorization Delta (Track 1 vs Track 2)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    piv = df_agg.pivot_table(index=["record_id", "track"], columns="evaluation_mode", values="composite_score").reset_index()
    if {"blinded_T0", "unblinded_T0"}.issubset(piv.columns):
        piv["delta_mem"] = piv["unblinded_T0"] - piv["blinded_T0"]
        tracks = [t for t in ["track1_sec", "track2_yc"] if t in piv["track"].unique()]
        data = [piv[piv["track"] == t]["delta_mem"].dropna().to_numpy() for t in tracks]
        labels = ["Track 1: SEC Form C\n(Unfamiliar Cohort)" if t == "track1_sec" else "Track 2: YC Tier-A\n(Famous Cohort)" for t in tracks]
        if data:
            ax.boxplot(data, tick_labels=labels, patch_artist=True)
            ax.axhline(0.0, color="gray", linestyle="--", linewidth=1)
    ax.set_ylabel("Unblinded - Blinded Composite Score (Δ_mem)")
    ax.set_title("Figure 1: Memorization / Name-Recognition Bias Across Cohorts")
    fig.tight_layout()
    fig.savefig(figures_dir / "fig1_blinding_memorization.png")
    plt.close(fig)

    # Fig 2: Social Proof / Herding Cues
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    arms = [a for a in ["social_cue_neg", "blinded_T0", "social_cue_pos"] if a in df_agg["evaluation_mode"].unique()]
    if arms:
        means = [df_agg[df_agg["evaluation_mode"] == a]["composite_score"].mean() for a in arms]
        ses = [df_agg[df_agg["evaluation_mode"] == a]["composite_score"].sem() for a in arms]
        x = np.arange(len(arms))
        ax.bar(x, means, yerr=ses, capsize=5, color=["#d95f02", "#7570b3", "#1b9e77"])
        ax.set_xticks(x)
        ax.set_xticklabels(["Negative Social Cue", "Blinded Baseline (T0)", "Positive Social Cue"])
    ax.set_ylabel("Mean Composite Score (0-100)")
    ax.set_title("Figure 2: Sensitivity to Early Investor Social-Proof Cues (H3)")
    fig.tight_layout()
    fig.savefig(figures_dir / "fig2_herding_cues.png")
    plt.close(fig)

    # Fig 3: ROC & PR Curves on Track 1 Funded Outcome & 3-Year Survival
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.3))
    for ax, y_col, title in [
        (axes[0], "funded_outcome", "Stage 1: Campaign Funded"),
        (axes[1], "survival_3y_outcome", "Stage 2: 3-Year Survival (Funded)"),
    ]:
        sub = df_t1.copy()
        if y_col == "survival_3y_outcome":
            sub = sub[sub["funded_outcome"] == 1]
        sub = sub[[y_col, "predicted_invest_prob", "predicted_survival_prob"]].dropna()
        if len(sub) >= 6 and sub[y_col].nunique() == 2:
            prob_col = "predicted_invest_prob" if y_col == "funded_outcome" else "predicted_survival_prob"
            fpr, tpr, _ = roc_curve(sub[y_col], sub[prob_col])
            auc = roc_auc_score(sub[y_col], sub[prob_col])
            ax.plot(fpr, tpr, label=f"Blinded LLM (AUC={auc:.2f})", linewidth=2)
        ax.plot([0, 1], [0, 1], "k--", linewidth=1)
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title(title)
        ax.legend(loc="lower right")
    fig.suptitle("Figure 3: Two-Stage Out-of-Sample Predictive Discrimination (Track 1)")
    fig.tight_layout()
    fig.savefig(figures_dir / "fig3_roc_pr_curves.png")
    plt.close(fig)

    # Fig 4: Calibration & Base-Rate Comparison
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    sub = df_t1[["funded_outcome", "predicted_invest_prob"]].dropna()
    if len(sub) >= 10:
        sub = sub.copy()
        sub["bin"] = pd.qcut(sub["predicted_invest_prob"], q=min(5, sub["predicted_invest_prob"].nunique()), duplicates="drop")
        cal = sub.groupby("bin", observed=True).agg(
            pred=("predicted_invest_prob", "mean"),
            obs=("funded_outcome", "mean"),
        )
        ax.plot(cal["pred"], cal["obs"], "o-", linewidth=2, label="Blinded Gemini 3.5 Flash-Lite")
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="Perfect Calibration")
    ax.set_xlabel("Predicted Funding Probability")
    ax.set_ylabel("Observed Funding Rate")
    ax.set_title("Figure 4: Probability Calibration (Stage 1 Funding Outcome)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figures_dir / "fig4_calibration_and_errors.png")
    plt.close(fig)


def run_full_analysis(
    scores_csv: Path,
    track1_jsonl: Path,
    track2_jsonl: Path,
    pop_counts_json: Path,
    out_json: Path,
    figures_dir: Path,
) -> dict[str, Any]:
    df_raw = pd.read_csv(scores_csv)
    df_meta = _load_records([track1_jsonl, track2_jsonl])

    # Reliability across runs
    piv_comp = df_raw.pivot_table(index=["record_id", "evaluation_mode"], columns="run_idx", values="composite_score").dropna()
    alpha_comp = _cronbach_alpha(piv_comp.to_numpy()) if len(piv_comp) >= 3 else None

    num_cols = [
        "composite_score",
        "predicted_invest",
        "predicted_invest_prob",
        "predicted_survival_prob",
        "confidence",
    ]
    df_agg = df_raw.groupby(["record_id", "track", "evaluation_mode"], as_index=False)[num_cols].mean()

    ablations = {
        "overall_mem": compute_paired_ablation(df_agg, "unblinded_T0", "blinded_T0"),
        "track1_mem": compute_paired_ablation(df_agg[df_agg["track"] == "track1_sec"], "unblinded_T0", "blinded_T0"),
        "track2_mem": compute_paired_ablation(df_agg[df_agg["track"] == "track2_yc"], "unblinded_T0", "blinded_T0"),
        "herding_pos": compute_paired_ablation(df_agg, "social_cue_pos", "blinded_T0"),
        "herding_neg": compute_paired_ablation(df_agg, "social_cue_neg", "blinded_T0"),
    }

    blind_df = df_agg[df_agg["evaluation_mode"] == "blinded_T0"].copy()
    df_merged = pd.merge(df_meta, blind_df.drop(columns=["track"]), on="record_id", how="inner")
    df_t1 = df_merged[df_merged["track"] == "track1_sec"].copy()
    df_t1["log_offering"] = np.log1p(pd.to_numeric(df_t1["offering_amount"], errors="coerce").clip(lower=0))
    df_t1["log_assets"] = np.log1p(pd.to_numeric(df_t1["total_assets"], errors="coerce").clip(lower=0))
    df_t1["log_revenues"] = np.log1p(pd.to_numeric(df_t1["revenues"], errors="coerce").clip(lower=0))

    # IPW weights from population stratum counts
    df_t1["ipw_weight"] = 1.0
    if pop_counts_json.exists() and "prelim_stratum" in df_t1.columns:
        pop = json.loads(pop_counts_json.read_text(encoding="utf-8"))
        sample_counts = df_t1["prelim_stratum"].value_counts().to_dict()
        weights = {}
        for stratum, s_cnt in sample_counts.items():
            pop_cnt = pop.get(stratum)
            if pop_cnt and s_cnt > 0:
                weights[stratum] = float(pop_cnt) / float(s_cnt)
        if weights:
            df_t1["ipw_weight"] = df_t1["prelim_stratum"].map(weights).fillna(1.0)
            df_t1["ipw_weight"] = df_t1["ipw_weight"] / df_t1["ipw_weight"].mean()

    # Stage 1 & Stage 2 Regressions
    regressions = {
        "stage1_funded_llm_only": _fit_glm_logit(df_t1, "funded_outcome", ["composite_score"]),
        "stage1_funded_full": _fit_glm_logit(df_t1, "funded_outcome", ["composite_score", "log_offering", "log_assets", "log_revenues"]),
        "stage1_funded_ipw": _fit_glm_logit(df_t1, "funded_outcome", ["composite_score", "log_offering", "log_assets", "log_revenues"], weight_col="ipw_weight"),
    }
    df_t1_funded = df_t1[df_t1["funded_outcome"] == 1].copy()
    regressions["stage2_survival_llm_only"] = _fit_glm_logit(df_t1_funded, "survival_3y_outcome", ["composite_score"])
    regressions["stage2_survival_full"] = _fit_glm_logit(df_t1_funded, "survival_3y_outcome", ["composite_score", "log_offering", "log_assets", "log_revenues"])
    regressions["stage2_winner_llm_only"] = _fit_glm_logit(df_t1_funded, "winner_breakout_outcome", ["composite_score"])
    regressions["stage2_winner_full"] = _fit_glm_logit(df_t1_funded, "winner_breakout_outcome", ["composite_score", "log_offering", "log_assets", "log_revenues"])

    # Out-of-fold H4 Ensembles & Discrimination
    stage1_sub = df_t1[["funded_outcome", "predicted_invest_prob"]].dropna()
    stage2_sub = df_t1_funded[["survival_3y_outcome", "predicted_survival_prob"]].dropna()

    discrimination = {
        "stage1_llm_prob": _binary_eval_metrics(stage1_sub["funded_outcome"].to_numpy(), stage1_sub["predicted_invest_prob"].to_numpy()) if len(stage1_sub) else {},
        "stage2_llm_prob": _binary_eval_metrics(stage2_sub["survival_3y_outcome"].to_numpy(), stage2_sub["predicted_survival_prob"].to_numpy()) if len(stage2_sub) else {},
        "oof_stage1_llm_only": compute_oof_ensemble(df_t1, "funded_outcome", ["composite_score"]),
        "oof_stage1_llm_plus_fin": compute_oof_ensemble(df_t1, "funded_outcome", ["composite_score", "log_offering", "log_assets", "log_revenues"]),
        "oof_stage2_llm_only": compute_oof_ensemble(df_t1_funded, "survival_3y_outcome", ["composite_score"]),
        "oof_stage2_fin_only": compute_oof_ensemble(df_t1_funded, "survival_3y_outcome", ["log_offering", "log_assets", "log_revenues"]),
        "oof_stage2_hybrid_h4": compute_oof_ensemble(df_t1_funded, "survival_3y_outcome", ["composite_score", "log_offering", "log_assets", "log_revenues"]),
        "oof_full_cohort_winner_crowd_only": compute_oof_ensemble(df_t1, "winner_breakout_outcome", ["funding_ratio"]),
        "oof_full_cohort_winner_hybrid": compute_oof_ensemble(df_t1, "winner_breakout_outcome", ["composite_score", "funding_ratio", "log_offering", "log_assets"]),
    }

    _generate_figures(df_agg, df_t1, figures_dir)

    summary = {
        "sample_counts": {
            "total_records_scored": int(df_agg["record_id"].nunique()),
            "track1_n": int(len(df_t1)),
            "track1_funded_n": int(len(df_t1_funded)),
            "track2_n": int(len(df_merged[df_merged["track"] == "track2_yc"])),
            "total_llm_calls_logged": int(len(df_raw)),
        },
        "reliability": {
            "cronbach_alpha_composite_across_runs": alpha_comp,
        },
        "ablations": ablations,
        "regressions": regressions,
        "discrimination": discrimination,
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run econometric, IPW, OOF ensemble, and figure analysis.")
    parser.add_argument("--scores-csv", default="results/llm_scores_raw.csv")
    parser.add_argument("--track1", default="data/processed/track1_sec_form_c.jsonl")
    parser.add_argument("--track2", default="data/processed/track2_yc_tier_a.jsonl")
    parser.add_argument("--pop-counts", default="data/processed/sec_population_counts.json")
    parser.add_argument("--out-json", default="results/analysis_summary.json")
    parser.add_argument("--figures-dir", default="results/figures")
    args = parser.parse_args()
    run_full_analysis(
        Path(args.scores_csv),
        Path(args.track1),
        Path(args.track2),
        Path(args.pop_counts),
        Path(args.out_json),
        Path(args.figures_dir),
    )
    print(f"Analysis complete -> {args.out_json}")


if __name__ == "__main__":
    main()
