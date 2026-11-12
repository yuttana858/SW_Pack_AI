"""swpack-kb MCP server: the knowledge service for every Claude client in the ecosystem.

Run locally (Claude Code / desktop over stdio):
    python -m mcp_server.server
    claude mcp add swpack-kb -- python -m mcp_server.server        # from the repo root

Run over HTTP (what the Modal deployment serves at /mcp):
    python -m mcp_server.server --http --port 8765

User context (plant, machine, families, role) comes from SWPACK_PLANT, SWPACK_MACHINE,
SWPACK_FAMILIES (comma list), SWPACK_ROLE. Per-request identity from SSO tokens replaces this
in phase C3; until then an HTTP server must be private (Modal proxy auth) — see deploy/modal_app.py.

All tools are read-only.
"""
from __future__ import annotations

import argparse
import json
import os
from typing import Any

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

from agent.tools import TOOLS as CALC_TOOLS
from kb.service import CALC_NAMES, KnowledgeService, UserContext

INSTRUCTIONS = """Packaging-engineering knowledge base for PACK AI.
- Search with kb_search, then read full sections with kb_read before relying on them; cite the chunk ids and source titles.
- For governing numbers (materials, allowances, tolerances, factors, machines) use kb_resolve: it applies the user's plant/machine scope.
- Never do engineering arithmetic yourself: call calc with the right calculator (list them with calc_list).
- Report confidence and status; say clearly when a value is draft/unreviewed or marked VERIFY."""
READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)


def context_from_env() -> UserContext:
    fam = tuple(f for f in os.environ.get("SWPACK_FAMILIES", "").split(",") if f)
    return UserContext(user=os.environ.get("SWPACK_USER", "local"), plant=os.environ.get("SWPACK_PLANT") or None,
                       machine=os.environ.get("SWPACK_MACHINE") or None, families=fam,
                       role=os.environ.get("SWPACK_ROLE", "viewer"))


def create_server(service: KnowledgeService, ctx: UserContext) -> MCPServer:
    server = MCPServer(name="swpack-kb", title="PACK AI knowledge base", instructions=INSTRUCTIONS,
                       version=service.manifest["release_id"])

    def kb_search(query: str, k: int = 8, kinds: list[str] | None = None, material_families: list[str] | None = None,
                  confidence: list[str] | None = None) -> dict[str, Any]:
        """Hybrid search over corpus sections and data cards. kinds: corpus | card. material_families:
        corrugated, folding-carton, honeycomb, paper-tube, molded-pulp, ... confidence: reference,
        industry-typical, derived, supplier-certified, measured. Returns ranked chunk ids with snippets."""
        return service.search(ctx, query, k, kinds, material_families, confidence)

    def kb_read(chunk_id: str) -> dict[str, Any]:
        """Full text of one chunk (corpus section or data card) with its resolved citations."""
        return service.read(ctx, chunk_id)

    def kb_resolve(record_type: str, filter_key: str | None = None, filter_value: str | None = None,
                   approved_only: bool = False) -> dict[str, Any]:
        """Governing data record for the user's scope (machine > plant > company > library).
        record_type: allowance_table, board_material, flute_profile, grade_table, factor_set, formula,
        box_style, tolerance_spec, machine_spec, plant. filter_key is a dotted path, e.g. flute.code."""
        return service.resolve(ctx, record_type, filter_key, filter_value, approved_only)

    def calc_list() -> dict[str, Any]:
        """List the engineering calculators and their input schemas (SI units: mm, N, N/mm, kg)."""
        return {"calculators": [{"name": t["name"], "description": t["description"], "input_schema": t["input_schema"]}
                                for t in CALC_TOOLS if t["name"] in CALC_NAMES]}

    def calc(calculator: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Run a tested calculator (see calc_list) and return value, unit, formula id, inputs, warnings, sources."""
        return service.calc(ctx, calculator, arguments)

    def kb_release() -> dict[str, Any]:
        """Release manifest summary: release id, git commit, counts, record status, embedder."""
        m = service.manifest
        return {k: m.get(k) for k in ("release_id", "built_at", "git_commit", "git_dirty", "chunks", "chunk_kinds",
                                      "record_status", "packcalc", "embedder")}

    for fn in (kb_search, kb_read, kb_resolve, calc_list, calc, kb_release):
        server.add_tool(fn, annotations=READ_ONLY)
    return server


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--http", action="store_true")
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    from kb.build import ROOT, build  # noqa: PLC0415
    build_dir = ROOT / "build" / "kb"
    if not (build_dir / "index.json").exists():
        build(build_dir)                       # first run in a fresh checkout
    server = create_server(KnowledgeService.load(build_dir), context_from_env())
    if a.http:
        server.run("streamable-http", port=a.port)
    else:
        server.run("stdio")


if __name__ == "__main__":
    main()
