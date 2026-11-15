from src.ingest.ingest_yc_tier_a import build_track2_record, extract_clean_text_from_html


def test_build_track2_record_skips_unpopulated_and_censors_recent():
    pending = {
        "record_id": "OPTB-016",
        "meta": {
            "t0_text_status": "pending_text_ingestion",
            "accelerator_decision": 1,
            "three_year_outcome": 1,
            "blinding_entities": {
                "company_aliases": ["Xendit"],
                "founder_names": [],
                "product_terms": [],
            },
        },
        "blended_pitch_text": {
            "batch_cycle": "YC S15",
            "one_liner_and_product": None,
        },
    }
    assert build_track2_record(pending, None, "Active") is None

    edicek = {
        "record_id": "OPTB-052",
        "meta": {
            "t0_text_status": "populated_ready",
            "accelerator_decision": 0,
            "three_year_outcome": None,
            "blinding_entities": {
                "company_aliases": ["Edicek"],
                "founder_names": ["Petr Homoky"],
                "product_terms": [],
            },
        },
        "blended_pitch_text": {
            "batch_cycle": "YC S25",
            "one_liner_and_product": "Edicek is a bookmarking app.",
        },
    }
    out = build_track2_record(edicek, None, None)
    assert out is not None and out["outcomes"]["survival_3y_outcome"] is None


def test_extract_clean_text_from_html_strips_scripts_and_nav():
    html = """
    <html><head><script>var x=1;</script><style>body{}</style></head>
    <body><nav>Home | About</nav><article><p>What are you going to make?</p><p>We make rockets.</p></article></body></html>
    """
    text = extract_clean_text_from_html(html)
    assert "We make rockets." in text
    assert "var x=1" not in text
    assert "Home | About" not in text
