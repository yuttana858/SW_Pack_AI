"""Formula registry and packcalc must stay in step."""
import importlib
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RECORDS = [yaml.safe_load(p.read_text()) for p in (ROOT / "data/library/formulas").glob("*.yaml")]


def test_every_record_points_to_real_code_and_tests():
    for r in RECORDS:
        mod, fn = r["formula"]["implementation"].rsplit(".", 1)
        assert callable(getattr(importlib.import_module(mod), fn)), r["id"]
        for t in r["formula"]["golden_tests"]:
            path, *names = t.split("::")
            text = (ROOT / path).read_text()
            assert f"def {names[-1]}" in text, f"{r['id']}: missing test {t}"


def test_every_formula_id_used_in_code_has_a_record():
    ids = {r["id"] for r in RECORDS}
    used = set()
    for p in (ROOT / "packcalc").glob("*.py"):
        used |= set(re.findall(r'"(lib\.formula\.[a-z0-9-]+)"', p.read_text()))
    assert used <= ids, f"formula ids without a registry record: {sorted(used - ids)}"
