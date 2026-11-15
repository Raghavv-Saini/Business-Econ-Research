from src.ingest.ingest_sec_form_c import (
    parse_cu_amount_raised,
    parse_ctr_is_failure,
    code_issuer_outcomes,
)


def test_parse_cu_and_ctr_xml_variants():
    assert (
        parse_cu_amount_raised(
            "<progressUpdate><amountRaised>125000.50</amountRaised></progressUpdate>"
        )
        == 125000.50
    )
    assert parse_cu_amount_raised("<other/>") is None
    assert (
        parse_ctr_is_failure(
            "<termination><reason>Ceased operations and dissolved</reason></termination>"
        )
        is True
    )
    assert (
        parse_ctr_is_failure(
            "<termination><over25MillionAssets>true</over25MillionAssets></termination>"
        )
        is False
    )


def test_code_issuer_outcomes_two_stage_and_delinquency_fallback():
    funded_alive = code_issuer_outcomes(
        submissions=[
            {"type": "C", "date": "20190301"},
            {"type": "C-AR", "date": "20230401"},
        ],
        c_tr_flags={},
        has_form_d_post=False,
        website_alive=False,
    )
    assert funded_alive["funded_outcome"] == 1
    assert funded_alive["survival_3y_outcome"] == 1

    delinquent_rescued = code_issuer_outcomes(
        submissions=[
            {"type": "C", "date": "20190301"},
            {"type": "C-AR", "date": "20200401"},
        ],
        c_tr_flags={},
        has_form_d_post=True,
        website_alive=False,
    )
    assert delinquent_rescued["survival_3y_outcome"] == 1
    assert delinquent_rescued["winner_breakout_outcome"] == 1

    unfunded = code_issuer_outcomes(
        submissions=[
            {"type": "C", "date": "20190301"},
            {"type": "C-W", "date": "20190601"},
        ],
        c_tr_flags={},
        has_form_d_post=False,
        website_alive=True,
    )
    assert unfunded["funded_outcome"] == 0
    assert unfunded["survival_3y_outcome"] is None
