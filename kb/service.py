"""KnowledgeService: the one API behind the MCP server, the Cloud AI agent and tests.

Read-only. Scope (plant/machine) comes from the caller's identity; the service never lets a
client widen it. Every response carries the release id so answers are traceable.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agent.tools import TOOLS as CALC_TOOLS
from swdata import Store

from .index import HybridIndex

ROOT = Path(__file__).resolve().parent.parent
CALC_NAMES = [t["name"] for t in CALC_TOOLS if t["name"] != "lookup_record"]


@dataclass(frozen=True)
class UserContext:
    user: str = "anonymous"
    plant: str | None = None
    machine: str | None = None
    families: tuple[str, ...] = ()          # empty = all families
    role: str = "viewer"                    # viewer | engineer | steward | plant-admin


class KnowledgeService:
    def __init__(self, index: HybridIndex, manifest: dict, store: Store, embedder=None):
        self.index, self.manifest, self.store, self.embedder = index, manifest, store, embedder

    @classmethod
    def load(cls, build_dir: Path = ROOT / "build" / "kb", data_dir: Path = ROOT / "data", embedder=None):
        return cls(HybridIndex.load(build_dir / "index.json"), json.loads((build_dir / "manifest.json").read_text()),
                   Store.from_dir(data_dir), embedder)

    def _envelope(self, payload: Any) -> dict:
        return {"release_id": self.manifest["release_id"], "result": payload}

    def _scope_filter(self, ctx: UserContext) -> list[str]:
        allowed = ["global", "company"]
        if ctx.plant:
            allowed.append(f"plant:{ctx.plant}")
            allowed += sorted({c["scope"] for c in self.index.chunks if c["scope"].startswith(f"machine:{ctx.plant}/")})
        return allowed

    def search(self, ctx: UserContext, query: str, k: int = 8, kinds: list[str] | None = None,
               families: list[str] | None = None, confidence: list[str] | None = None) -> dict:
        filters = {"scope": self._scope_filter(ctx), "kind": kinds, "confidence": confidence,
                   "material_family": families or list(ctx.families) or None}
        hits = self.index.search(query, k=min(max(k, 1), 25), filters=filters, embedder=self.embedder)
        # most specific scope first among equal-relevance hits: machine > plant > company > global
        rank = {"machine": 0, "plant": 1, "company": 2, "global": 3}
        hits.sort(key=lambda h: (-h["score"], rank[h["scope"].split(":")[0]]))
        return self._envelope(hits)

    def read(self, ctx: UserContext, chunk_id: str) -> dict:
        c = self.index.read(chunk_id)
        if c is None or c["scope"] not in self._scope_filter(ctx):
            return self._envelope({"error": f"no chunk {chunk_id!r} in your scope"})
        return self._envelope(c)

    def resolve(self, ctx: UserContext, record_type: str, filter_key: str | None = None, filter_value: str | None = None,
                approved_only: bool = False) -> dict:
        args = dict(record_type=record_type, filter_key=filter_key, filter_value=filter_value, plant=ctx.plant,
                    machine=ctx.machine, approved_only=approved_only)
        return self._envelope(_lookup(self.store, **args))

    def calc(self, ctx: UserContext, name: str, args: dict) -> dict:
        if name not in CALC_NAMES:
            return self._envelope({"error": f"unknown calculator {name!r}; available: {CALC_NAMES}"})
        from agent.tools import dispatch  # noqa: PLC0415
        return self._envelope(dispatch(name, args))


def _lookup(store: Store, **kw) -> dict:
    from agent.tools import _lookup as lookup  # noqa: PLC0415
    return lookup(**kw, store=store)
