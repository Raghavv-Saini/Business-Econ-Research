import numpy as np
import pandas as pd
from src.analysis.analyze_results import compute_oof_ensemble, compute_paired_ablation


def test_paired_ablation_and_oof_ensemble():
    df = pd.DataFrame(
        {
            "record_id": ["A", "B", "C", "D", "A", "B", "C", "D"],
            "evaluation_mode": ["blinded_T0"] * 4 + ["unblinded_T0"] * 4,
            "composite_score": [50.0, 60.0, 55.0, 65.0, 60.0, 70.0, 65.0, 75.0],
            "predicted_invest": [0, 1, 0, 1, 1, 1, 1, 1],
        }
    )
    res = compute_paired_ablation(df, "unblinded_T0", "blinded_T0")
    assert abs(res["mean_delta"] - 10.0) < 1e-6

    rng = np.random.default_rng(42)
    ens_df = pd.DataFrame(
        {
            "llm_score": rng.normal(60, 10, 40),
            "funding_ratio": rng.uniform(0.5, 2.5, 40),
            "y": ([0, 1] * 20),
        }
    )
    oof = compute_oof_ensemble(ens_df, "y", ["llm_score", "funding_ratio"], n_splits=5)
    assert 0.0 <= oof["roc_auc"] <= 1.0 and len(oof["oof_probs"]) == 40
