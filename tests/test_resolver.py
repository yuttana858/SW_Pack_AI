import datetime as dt

from swdata import Store


def rec(id, scope, status="approved", version="1.0.0", tier=None, **kw):
    tier = tier or {"global": "L1", "company": "L2"}.get(scope.split(":")[0], "L3" if scope.startswith("plant") else "L4")
    return {"id": id, "type": "allowance_table", "scope": scope, "status": status, "version": version,
            "tier": tier, "confidence": "derived", "style": "0201", **kw}


STORE = Store([
    rec("lib", "global", "draft"),
    rec("co", "company"),
    rec("pa", "plant:a"),
    rec("pa-ffg2", "machine:a/ffg-2"),
    rec("pb-old", "plant:b", version="1.0.0", effective_to="2026-01-01"),
    rec("pb-new", "plant:b", version="2.0.0", effective_from="2026-01-02"),
    rec("pc-draft", "plant:c", "draft"),
])
ON = dt.date(2026, 11, 9)


def test_machine_beats_plant_beats_company():
    assert STORE.resolve("allowance_table", plant="a", machine="ffg-2", on=ON).record["id"] == "pa-ffg2"
    assert STORE.resolve("allowance_table", plant="a", machine="other", on=ON).record["id"] == "pa"
    assert STORE.resolve("allowance_table", on=ON).record["id"] == "co"


def test_effective_dates():
    r = STORE.resolve("allowance_table", plant="b", on=ON)
    assert r.record["id"] == "pb-new"
    assert any(i == "pb-old" for i, _ in r.skipped)


def test_min_status_falls_back_and_reports():
    r = STORE.resolve("allowance_table", plant="c", min_status="approved", on=ON)
    assert r.record["id"] == "co" and ("pc-draft", "status draft below approved") in r.skipped
    assert "skipped" in r.explain()


def test_draft_library_only_when_allowed():
    only_lib = Store([rec("lib", "global", "draft")])
    assert only_lib.resolve("allowance_table", min_status="approved").record is None
    assert only_lib.resolve("allowance_table").record["id"] == "lib"


def test_real_data_dir_loads():
    s = Store.from_dir("data")
    r = s.resolve("allowance_table", lambda r: any(row["style"] == "0201" for row in r["rows"]))
    assert r.found and r.record["id"] == "lib.allowance.fefco-0201.default"
