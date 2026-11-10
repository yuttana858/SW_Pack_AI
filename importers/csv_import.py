#!/usr/bin/env python3
"""Import plant / supplier CSV files into data records.

  python -m importers.csv_import --type board_material --scope plant:dallas \
      --method supplier-certificate --input boards.csv --out data/plants/dallas/materials

Every row is mapped through importers/profiles/<type>.yaml, converted to SI, validated against
schemas/, and written as one YAML record. Imported records are `draft` unless --approved-by is
given (which records who approved the file). Nothing is written if any row fails, unless
--partial is set. Use --dry-run to see the report only.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from packcalc import units

ROOT = Path(__file__).resolve().parent.parent
CONVERT = {
    "in_to_mm": units.in_to_mm,
    "ect_us_to_si": units.ect_us_to_si,
    "psi_to_kpa": lambda v: v * units.PSI_TO_KPA,
    "lb_msf_to_gsm": lambda v: v * units.LB_PER_MSF_TO_GSM,
    "lb_to_kg": lambda v: v * units.LB_TO_KG,
}
TIER_FOR_SCOPE = {"global": "L1", "company": "L2", "plant": "L3", "machine": "L4"}


def _validator(rtype: str) -> Draft202012Validator:
    res, schema = [], None
    for p in (ROOT / "schemas").glob("*.schema.json"):
        doc = json.loads(p.read_text())
        r = Resource.from_contents(doc)
        res += [(doc["$id"], r), (p.name, r)]
        if p.name == f"{rtype}.schema.json":
            schema = doc
    return Draft202012Validator(schema, registry=Registry().with_resources(res))


def _set(rec: dict, path: str, value: Any) -> None:
    parts = path.split(".")
    cur: Any = rec
    for i, key in enumerate(parts):
        last = i == len(parts) - 1
        nxt = parts[i + 1] if not last else None
        if isinstance(cur, list):
            idx = int(key)
            while len(cur) <= idx:
                cur.append({} if nxt and not nxt.isdigit() else None)
            if last:
                cur[idx] = value
            else:
                if cur[idx] is None:
                    cur[idx] = [] if nxt.isdigit() else {}
                cur = cur[idx]
        else:
            if last:
                cur[key] = value
            else:
                cur = cur.setdefault(key, [] if nxt.isdigit() else {})


def _cast(raw: str, spec: dict) -> Any:
    t = spec.get("type", "string")
    if t == "number":
        v = float(raw)
        v = CONVERT[spec["convert"]](v) if spec.get("convert") else v
        return float(f"{v:.6g}")
    if t == "integer":
        return int(raw)
    if t == "list":
        return [x.strip() for x in re.split(r"[;|]", raw) if x.strip()]
    return raw


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", s.lower()).strip("-")


def import_csv(rtype: str, scope: str, method: str, csv_path: Path, approved_by: str | None = None,
               source_ref: str | None = None) -> tuple[list[dict], list[str]]:
    profile = yaml.safe_load((ROOT / "importers/profiles" / f"{rtype}.yaml").read_text())
    cols = profile["columns"]
    tier = TIER_FOR_SCOPE[scope.split(":")[0]]
    validator = _validator(rtype)
    records, errors = [], []
    with csv_path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        unknown = [c for c in reader.fieldnames or [] if c not in cols]
        if unknown:
            errors.append(f"unknown columns {unknown}; fix the header to match importers/profiles/{rtype}.yaml")
            return [], errors
        for n, row in enumerate(reader, start=2):
            row = {k: (v or "").strip() for k, v in row.items()}
            if not any(row.values()):
                continue
            missing = [c for c, s in cols.items() if s.get("required") and not row.get(c)]
            if missing:
                errors.append(f"line {n}: missing required {missing}")
                continue
            scope_slug = scope.replace(":", ".").replace("/", ".")
            rec: dict[str, Any] = {
                "id": f"{scope_slug}.{rtype.split('_')[0]}.{slug(row[profile['id_column']])}",
                "type": rtype, "version": "1.0.0", "scope": scope, "tier": tier,
                "status": "approved" if approved_by else "draft",
                "confidence": "supplier-certified" if method == "supplier-certificate" else "measured",
                "provenance": {"method": method, "sources": [source_ref or csv_path.name]},
            }
            if approved_by:
                rec["approved_by"], rec["approved_on"] = approved_by, dt.date.today().isoformat()
            try:
                for col, spec in cols.items():
                    if row.get(col) and spec.get("path"):
                        paths = spec["path"] if isinstance(spec["path"], list) else [spec["path"]]
                        for p in paths:
                            _set(rec, p, _cast(row[col], spec))
            except (ValueError, KeyError) as e:
                errors.append(f"line {n}: {e}")
                continue
            errs = [f"line {n}: {'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in validator.iter_errors(rec)]
            if errs:
                errors += errs
                continue
            records.append(rec)
    return records, errors


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--type", required=True, choices=[p.stem for p in (ROOT / "importers/profiles").glob("*.yaml")])
    ap.add_argument("--scope", required=True, help="company | plant:<id> | machine:<plant>/<machine>")
    ap.add_argument("--method", required=True, choices=["supplier-certificate", "lab-test", "plant-measurement"])
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--approved-by")
    ap.add_argument("--source-ref", help="document reference, e.g. supplier certificate number")
    ap.add_argument("--partial", action="store_true", help="write valid rows even if some rows fail")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    recs, errs = import_csv(a.type, a.scope, a.method, a.input, a.approved_by, a.source_ref)
    for e in errs:
        print("ERROR ", e)
    print(f"{len(recs)} valid record(s), {len(errs)} error(s)")
    if a.dry_run or (errs and not a.partial):
        return 1 if errs else 0
    a.out.mkdir(parents=True, exist_ok=True)
    for r in recs:
        (a.out / f"{r['id'].split('.')[-1]}.yaml").write_text(yaml.safe_dump(r, sort_keys=False, allow_unicode=True))
    print(f"wrote {len(recs)} file(s) to {a.out}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
