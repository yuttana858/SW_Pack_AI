"""Bridge between board_material records and Auto3D's account board-database CSV.

Sync flow (run by the pipeline once tools access and pairing work):
  1. export   = packaging.boards.export             -> current CSV + revision
  2. plan     = plan_sync(records, export_csv)       -> rows to add / update / keep, never deletes
                                                         rows SW Pack AI does not own
  3. merged   = render_csv(plan.rows)
  4. packaging.boards.save_csv(csv=merged, revision=<from step 1>)   (refused on concurrent edit)
  5. re-export and verify(records, new_export)       -> every managed row matches its record

Only approved records are pushed. Rows owned by SW Pack AI carry provenance "swpack:<id>@<version>".
"""
from __future__ import annotations

import csv
import io
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

CONFIG = Path(__file__).with_name("board_columns.yaml")
TOL = 1e-6


def load_config(path: Path = CONFIG) -> dict:
    return yaml.safe_load(path.read_text())


def _get(rec: dict, path: str) -> Any:
    cur: Any = rec
    for k in path.split("."):
        if isinstance(cur, list):
            k = int(k)
            cur = cur[k] if k < len(cur) else None
        elif isinstance(cur, dict):
            cur = cur.get(k)
        else:
            return None
    return cur


def record_to_row(rec: dict, cfg: dict) -> dict[str, str]:
    marker = cfg["managed_marker"]["prefix"]
    row = {}
    for c in cfg["columns"]:
        src = c["from"]
        if src == "@provenance":
            v = f"{marker}{rec['id']}@{rec['version']}"
        elif src == "@calibrated":
            v = rec.get("status") == "approved" and rec.get("confidence") in ("supplier-certified", "measured")
        else:
            v = _get(rec, src)
        row[c["column"]] = "" if v is None else (str(v).lower() if isinstance(v, bool) else f"{v:g}" if isinstance(v, float) else str(v))
    return row


def parse_csv(text: str) -> tuple[list[str], list[dict[str, str]]]:
    reader = csv.DictReader(io.StringIO(text))
    return list(reader.fieldnames or []), [dict(r) for r in reader]


def render_csv(header: list[str], rows: list[dict[str, str]]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=header, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def _same(a: str, b: str) -> bool:
    try:
        return abs(float(a) - float(b)) <= TOL
    except ValueError:
        return (a or "") == (b or "")


@dataclass
class SyncPlan:
    header: list[str]
    rows: list[dict[str, str]]
    added: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    kept_unmanaged: list[str] = field(default_factory=list)
    stale_managed: list[str] = field(default_factory=list)   # owned rows with no approved record: flagged, not deleted
    skipped_records: list[str] = field(default_factory=list)


def plan_sync(records: list[dict], export_csv: str, cfg: dict | None = None) -> SyncPlan:
    cfg = cfg or load_config()
    idc, mcol, prefix = cfg["id_column"], cfg["managed_marker"]["column"], cfg["managed_marker"]["prefix"]
    header, current = parse_csv(export_csv)
    ours = [c["column"] for c in cfg["columns"]]
    header = header + [c for c in ours if c not in header]
    by_id = {r[idc]: r for r in current}
    plan = SyncPlan(header=header, rows=[])
    wanted = {}
    for rec in records:
        if rec.get("type") != "board_material" or rec.get("status") != "approved":
            plan.skipped_records.append(rec.get("id", "?"))
            continue
        wanted[rec["id"]] = record_to_row(rec, cfg)
    for row in current:
        rid = row.get(idc, "")
        if rid in wanted:
            new = {**row, **wanted[rid]}
            (plan.unchanged if all(_same(row.get(k, ""), v) for k, v in wanted[rid].items()) else plan.updated).append(rid)
            plan.rows.append(new)
        else:
            plan.rows.append(row)
            (plan.stale_managed if (row.get(mcol) or "").startswith(prefix) else plan.kept_unmanaged).append(rid)
    for rid, row in wanted.items():
        if rid not in by_id:
            plan.rows.append(row)
            plan.added.append(rid)
    return plan


def verify(records: list[dict], export_csv: str, cfg: dict | None = None) -> list[str]:
    """Read-back check after save_csv: every approved record must appear with identical values."""
    cfg = cfg or load_config()
    _, rows = parse_csv(export_csv)
    by_id = {r[cfg["id_column"]]: r for r in rows}
    problems = []
    for rec in records:
        if rec.get("type") != "board_material" or rec.get("status") != "approved":
            continue
        want, got = record_to_row(rec, cfg), by_id.get(rec["id"])
        if got is None:
            problems.append(f"{rec['id']}: missing from Auto3D catalogue")
            continue
        problems += [f"{rec['id']}: {k} expected {v!r} got {got.get(k)!r}" for k, v in want.items() if not _same(got.get(k, ""), v)]
    return problems


def check_headers(export_csv: str, cfg: dict | None = None) -> list[str]:
    cfg = cfg or load_config()
    header, _ = parse_csv(export_csv)
    return [c["column"] for c in cfg["columns"] if c["column"] not in header]


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "check-headers":
        missing = check_headers(Path(sys.argv[2]).read_text())
        print("all mapped columns present" if not missing else f"columns not in Auto3D export: {missing}")
        sys.exit(1 if missing else 0)
    print("usage: python -m connectors.auto3d.board_csv check-headers <export.csv>")
    sys.exit(2)
