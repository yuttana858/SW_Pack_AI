#!/usr/bin/env python3
"""Validate data/ YAML records against schemas/ and the tier/scope rules.

Each YAML file holds one record (a mapping) whose `type` selects
schemas/<type>.schema.json. Files under a directory named `_example` are
validated but may not be `approved`.

Usage: python tools/validate_data.py [data_dir]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
EXPECTED_TIER = {"library": "L1", "company": "L2"}


def load_registry() -> tuple[Registry, dict]:
    resources, by_type = [], {}
    for p in SCHEMAS.glob("*.schema.json"):
        doc = json.loads(p.read_text())
        res = Resource.from_contents(doc)
        resources += [(doc["$id"], res), (p.name, res)]
        by_type[p.name.removesuffix(".schema.json")] = doc
    return Registry().with_resources(resources), by_type


def physical_checks(rec: dict) -> list[str]:
    errs = []
    if rec.get("type") == "allowance_table":
        for i, row in enumerate(rec.get("rows", [])):
            if any(o < s for s, o in zip(row["k_s"], row["k_o"])):
                errs.append(f"rows[{i}]: k_o must be >= k_s on every axis")
    if rec.get("type") == "board_material":
        cal = rec.get("board", {}).get("caliper_mm", {})
        if cal and not (0.3 <= cal.get("nominal", 0) <= 20):
            errs.append("board.caliper_mm.nominal outside 0.3–20 mm")
    return errs


def main(data_dir: Path) -> int:
    registry, by_type = load_registry()
    errors, ids, files = [], {}, sorted(data_dir.rglob("*.yaml"))
    for path in files:
        rel = path.relative_to(data_dir)
        rec = yaml.safe_load(path.read_text())
        t = rec.get("type") if isinstance(rec, dict) else None
        if t not in by_type or t == "envelope":
            errors.append(f"{rel}: unknown or missing type {t!r}")
            continue
        v = Draft202012Validator(by_type[t], registry=registry)
        errors += [f"{rel}: {'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in v.iter_errors(rec)]
        errors += [f"{rel}: {m}" for m in physical_checks(rec)]
        top = rel.parts[0]
        if top in EXPECTED_TIER and rec.get("tier") != EXPECTED_TIER[top]:
            errors.append(f"{rel}: records under {top}/ must be tier {EXPECTED_TIER[top]}")
        if top == "plants" and rec.get("tier") not in ("L3", "L4"):
            errors.append(f"{rel}: records under plants/ must be tier L3 or L4")
        if "_example" in rel.parts and rec.get("status") == "approved":
            errors.append(f"{rel}: example records must not be approved")
        if rec.get("id") in ids:
            errors.append(f"{rel}: duplicate id {rec.get('id')} (also {ids[rec.get('id')]})")
        ids[rec.get("id")] = rel
    print(f"Checked {len(files)} records: {len(errors)} error(s)")
    for e in errors:
        print("ERROR  ", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data"))
