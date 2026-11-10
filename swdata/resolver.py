"""Scope resolution: the most specific approved, in-effect record wins.

Precedence (most specific first):
    machine:<plant>/<machine>  >  plant:<plant>  >  company  >  global (L1 library)
Within one scope, the highest status (approved > reviewed > draft) wins, then the newest version.
`min_status` lets production callers refuse drafts; while the library is still being reviewed,
callers may accept drafts but must report that the value is unreviewed.
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable

import yaml

STATUS_RANK = {"draft": 0, "reviewed": 1, "approved": 2}


def _version_key(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in v.split("."))


@dataclass(frozen=True)
class Resolution:
    record: dict[str, Any] | None
    scope_chain: tuple[str, ...]
    skipped: tuple[tuple[str, str], ...] = field(default_factory=tuple)   # (record id, reason)

    @property
    def found(self) -> bool:
        return self.record is not None

    def explain(self) -> str:
        if not self.record:
            return f"no record found in scopes {', '.join(self.scope_chain)}"
        r = self.record
        msg = f"{r['id']} v{r['version']} ({r['tier']}, {r['scope']}, {r['status']}, {r['confidence']})"
        if self.skipped:
            msg += "; skipped: " + "; ".join(f"{i} ({why})" for i, why in self.skipped)
        return msg


class Store:
    def __init__(self, records: Iterable[dict[str, Any]]):
        self.records = [r for r in records if isinstance(r, dict) and "id" in r]

    @classmethod
    def from_dir(cls, data_dir: str | Path, include_examples: bool = False) -> "Store":
        recs = []
        for p in sorted(Path(data_dir).rglob("*.yaml")):
            if p.name.startswith("_") or ("_example" in p.parts and not include_examples):
                continue
            recs.append(yaml.safe_load(p.read_text()))
        return cls(recs)

    @staticmethod
    def scope_chain(plant: str | None = None, machine: str | None = None) -> tuple[str, ...]:
        chain = []
        if plant and machine:
            chain.append(f"machine:{plant}/{machine}")
        if plant:
            chain.append(f"plant:{plant}")
        return tuple(chain + ["company", "global"])

    def resolve(self, rtype: str, match: Callable[[dict], bool] = lambda r: True, *, plant: str | None = None,
                machine: str | None = None, min_status: str = "draft", on: dt.date | None = None) -> Resolution:
        on = on or dt.date.today()
        chain = self.scope_chain(plant, machine)
        skipped: list[tuple[str, str]] = []
        for scope in chain:
            cands = []
            for r in self.records:
                if r.get("type") != rtype or r.get("scope") != scope or not match(r):
                    continue
                if r.get("status") == "retired":
                    skipped.append((r["id"], "retired")); continue
                if STATUS_RANK.get(r.get("status"), -1) < STATUS_RANK[min_status]:
                    skipped.append((r["id"], f"status {r.get('status')} below {min_status}")); continue
                ef, et = r.get("effective_from"), r.get("effective_to")
                if ef and dt.date.fromisoformat(str(ef)) > on:
                    skipped.append((r["id"], f"not effective until {ef}")); continue
                if et and dt.date.fromisoformat(str(et)) < on:
                    skipped.append((r["id"], f"expired {et}")); continue
                cands.append(r)
            if cands:
                best = max(cands, key=lambda r: (STATUS_RANK[r["status"]], _version_key(r["version"])))
                return Resolution(best, chain, tuple(skipped))
        return Resolution(None, chain, tuple(skipped))
