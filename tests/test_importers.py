import csv
from pathlib import Path

import pytest

from importers.csv_import import import_csv

ROOT = Path(__file__).resolve().parent.parent


def write(tmp_path, rows, header=None):
    header = header or list(rows[0])
    p = tmp_path / "in.csv"
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)
    return p


BASE = {"material_id": "M1", "flute": "C", "wall": "single", "caliper_mm": "4.0"}


def test_templates_import_cleanly():
    for t, scope in (("board_material", "plant:example"), ("machine_spec", "machine:example/ffg-1")):
        recs, errs = import_csv(t, scope, "plant-measurement", ROOT / "templates" / f"{t}.csv")
        assert not errs and len(recs) == 1


def test_us_columns_convert_to_si(tmp_path):
    p = write(tmp_path, [{**BASE, "caliper_mm": "", "caliper_in": "0.1575", "ect_lbf_per_in": "32", "burst_psi": "200"}])
    (rec,), errs = import_csv("board_material", "plant:a", "lab-test", p)
    assert not errs
    assert rec["board"]["caliper_mm"]["nominal"] == pytest.approx(4.0005)
    assert rec["board"]["ect_kn_per_m"]["nominal"] == pytest.approx(5.60406)
    assert rec["board"]["burst_kpa"]["nominal"] == pytest.approx(1378.95)
    assert rec["tier"] == "L3" and rec["status"] == "draft" and rec["confidence"] == "measured"


def test_bad_rows_are_reported_not_written(tmp_path):
    p = write(tmp_path, [{**BASE, "flute": "Z"}, {**BASE, "material_id": "", "caliper_mm": "x"}, BASE])
    recs, errs = import_csv("board_material", "plant:a", "lab-test", p)
    assert len(recs) == 1
    assert any("line 2" in e and "flute" in e for e in errs)
    assert any("line 3" in e and "missing required" in e for e in errs)


def test_unknown_header_rejected(tmp_path):
    p = write(tmp_path, [{**BASE, "colour": "brown"}])
    recs, errs = import_csv("board_material", "plant:a", "lab-test", p)
    assert not recs and "unknown columns" in errs[0]


def test_approval_and_tier_from_scope(tmp_path):
    p = write(tmp_path, [BASE])
    (rec,), _ = import_csv("board_material", "machine:a/ffg-2", "supplier-certificate", p, approved_by="J. Smith")
    assert rec["tier"] == "L4" and rec["status"] == "approved" and rec["approved_by"] == "J. Smith"
    assert rec["confidence"] == "supplier-certified"
