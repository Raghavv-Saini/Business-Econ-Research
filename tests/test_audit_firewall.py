from src.ingest.audit_t0_firewall import audit_record


def test_audit_record_catches_leakage_and_unmasked_alias():
    leaky = {
        "record_id": "TEST-1",
        "track": "track1_sec",
        "meta": {
            "blinding_entities": {
                "company_aliases": ["Acme"],
                "founder_names": [],
                "portal_names": [],
                "product_terms": [],
            }
        },
        "t0_payload": {
            "pitch_text": "We were acquired by Google in 2022 after raising Series A."
        },
    }
    issues = audit_record(leaky)
    assert any("leakage" in i.lower() for i in issues)


def test_audit_record_passes_clean_record():
    clean = {
        "record_id": "TEST-2",
        "track": "track2_yc",
        "meta": {
            "blinding_entities": {
                "company_aliases": ["AcmeWidget"],
                "founder_names": ["Jane Doe"],
                "portal_names": [],
                "product_terms": ["AcmeWidget"],
            }
        },
        "t0_payload": {
            "pitch_text": "AcmeWidget helps engineers automate unit testing with Jane Doe leading engineering.",
            "financials": {"offering_amount": 50000},
        },
    }
    issues = audit_record(clean)
    assert issues == []


def test_audit_record_catches_track2_directory_and_future_year_leakage():
    dir_rec = {
        "record_id": "OPTB-003",
        "track": "track2_yc",
        "t0_year": 2009,
        "meta": {"blinding_entities": {"company_aliases": ["Mixpanel"], "founder_names": [], "portal_names": [], "product_terms": []}},
        "t0_payload": {"pitch_text": "Previously founder at Mixpanel (2009-2019). Status: Active. Team Size: 410."},
    }
    issues = audit_record(dir_rec)
    assert len(issues) >= 2
