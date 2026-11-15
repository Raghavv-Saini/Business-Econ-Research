import json
from src.eval.run_llm_experiment import load_completed_keys, run_experiment


def test_resumable_experiment_skips_completed_runs(tmp_path, monkeypatch):
    jsonl = tmp_path / "sample.jsonl"
    rec = {
        "record_id": "R1",
        "track": "track1_sec",
        "t0_year": 2019,
        "meta": {
            "blinding_entities": {
                "company_aliases": ["Acme"],
                "founder_names": [],
                "portal_names": [],
                "product_terms": [],
            }
        },
        "t0_payload": {
            "pitch_text": "Acme builds widgets.",
            "financials": {"offering_amount": 50000},
        },
        "outcomes": {
            "funded_outcome": 1,
            "survival_3y_outcome": 1,
            "winner_breakout_outcome": 0,
        },
    }
    jsonl.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    out_csv = tmp_path / "scores.csv"
    calls = []

    def fake_gemini(prompt, **kw):
        calls.append(prompt)
        return {
            "scores": {
                d: 70
                for d in [
                    "team_and_background",
                    "execution_plan",
                    "financial_feasibility",
                    "writing_and_polish",
                    "value_proposition_innovativeness",
                    "market_opportunity",
                    "competitive_moat",
                    "customer_need_alignment",
                    "roi_potential",
                    "long_run_viability",
                ]
            },
            "composite_score": 70.0,
            "predicted_invest": 1,
            "predicted_invest_prob": 0.72,
            "predicted_survival_prob": 0.65,
            "confidence": 75,
            "key_risk_flag": "Early market.",
        }

    monkeypatch.setattr("src.eval.run_llm_experiment.call_gemini_json", fake_gemini)
    run_experiment([str(jsonl)], str(out_csv), n_runs=2)
    assert len(calls) == 8  # 4 arms * 2 runs
    assert len(load_completed_keys(str(out_csv))) == 8
    run_experiment([str(jsonl)], str(out_csv), n_runs=2)
    assert len(calls) == 8  # Resumed without duplicate calls
