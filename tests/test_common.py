from src.common import build_company_aliases, blind_payload, RUBRIC_DIMENSIONS


def test_build_company_aliases_strips_legal_suffixes():
    aliases = build_company_aliases("Acme Robotics, Inc.", ["AcmeBot"])
    assert "Acme Robotics, Inc." in aliases
    assert "Acme Robotics" in aliases
    assert "AcmeBot" in aliases


def test_blind_payload_masks_entities_and_attaches_social_cues():
    rec = {
        "record_id": "SEC-001",
        "track": "track1_sec",
        "meta": {
            "blinding_entities": {
                "company_aliases": ["Acme Robotics, Inc.", "Acme Robotics"],
                "founder_names": ["Jane Doe"],
                "portal_names": ["Wefunder"],
                "product_terms": ["AcmeOS"],
            }
        },
        "t0_payload": {
            "pitch_text": "Acme Robotics builds AcmeOS with Jane Doe on Wefunder at https://acmerobotics.io.",
            "financials": {"offering_amount": 50000},
        },
    }
    b = blind_payload(rec, "blinded_T0")
    txt = b["t0_payload"]["pitch_text"]
    assert "Acme Robotics" not in txt
    assert "Jane Doe" not in txt
    assert "Wefunder" not in txt
    assert "acmerobotics.io" not in txt
    assert "social_cue" not in b["t0_payload"]
    pos = blind_payload(rec, "social_cue_pos")
    neg = blind_payload(rec, "social_cue_neg")
    assert "strong initial commitments" in pos["t0_payload"]["social_cue"]
    assert "slow initial commitments" in neg["t0_payload"]["social_cue"]
    assert len(RUBRIC_DIMENSIONS) == 10
