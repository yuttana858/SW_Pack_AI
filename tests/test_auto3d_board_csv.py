from connectors.auto3d.board_csv import load_config, plan_sync, record_to_row, render_csv, verify

CFG = load_config()


def rec(id, caliper=4.0, status="approved", version="1.0.0"):
    return {"id": id, "type": "board_material", "version": version, "status": status, "confidence": "supplier-certified",
            "title": id, "board": {"flute": "C", "caliper_mm": {"nominal": caliper, "tol_plus": 0.15}},
            "auto3d": {"insideFactors": [1, 1, 2], "outsideFactors": [1, 1, 2]}}


EXPORT = "id,name,flute,caliperMm,provenance\nnominal-b,B nominal,B,3,auto3d\nold,Old,C,4,swpack:old@1.0.0\nm1,m1,C,4,swpack:m1@1.0.0\n"


def test_plan_keeps_unmanaged_and_flags_stale_never_deletes():
    p = plan_sync([rec("m1", caliper=3.9), rec("m2"), rec("draft1", status="draft")], EXPORT, CFG)
    ids = [r["id"] for r in p.rows]
    assert ids == ["nominal-b", "old", "m1", "m2"]
    assert p.updated == ["m1"] and p.added == ["m2"] and p.kept_unmanaged == ["nominal-b"]
    assert p.stale_managed == ["old"] and p.skipped_records == ["draft1"]


def test_row_marks_calibration_only_for_approved_certified():
    assert record_to_row(rec("a"), CFG)["calibrated"] == "true"
    assert record_to_row(rec("b", status="draft"), CFG)["calibrated"] == "false"
    assert record_to_row(rec("a"), CFG)["provenance"] == "swpack:a@1.0.0"


def test_roundtrip_verify():
    recs = [rec("m1", caliper=3.9), rec("m2")]
    p = plan_sync(recs, EXPORT, CFG)
    assert verify(recs, render_csv(p.header, p.rows), CFG) == []
    bad = render_csv(p.header, [{**r, "caliperMm": "5"} if r["id"] == "m2" else r for r in p.rows])
    assert any("m2: caliperMm" in e for e in verify(recs, bad, CFG))


def test_config_is_unconfirmed_until_headers_checked():
    assert CFG["confirmed"] is False
