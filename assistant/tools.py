"""Tools the assistant can call, bound to one user's scope.

Knowledge tools go through KnowledgeService (scope-enforced). Calculator tools reuse the
definitions in agent/tools.py. The generic `lookup_record` tool is replaced by `kb_resolve`
so the model can never pick a plant or machine outside the user's context.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from agent.tools import TOOLS as CALC_TOOLS, dispatch as calc_dispatch
from kb.service import KnowledgeService, UserContext

STR_OR_NULL = {"type": ["string", "null"]}
KB_TOOLS: list[dict[str, Any]] = [
    {"name": "kb_search", "strict": True,
     "description": "Search the packaging knowledge base (corpus sections and data cards) for the user's scope. "
                    "Returns ranked chunk ids, headings, confidence, status and a snippet. Read promising chunks with kb_read.",
     "input_schema": {"type": "object", "additionalProperties": False, "required": ["query", "k", "kinds", "material_families"],
                      "properties": {"query": {"type": "string"}, "k": {"type": "integer"},
                                     "kinds": {"type": ["array", "null"], "items": {"type": "string", "enum": ["corpus", "card"]}},
                                     "material_families": {"type": ["array", "null"], "items": {"type": "string"}}}}},
    {"name": "kb_read", "strict": True,
     "description": "Read the full text of one chunk (corpus section or data card) with its citations.",
     "input_schema": {"type": "object", "additionalProperties": False, "required": ["chunk_id"],
                      "properties": {"chunk_id": {"type": "string"}}}},
    {"name": "kb_resolve", "strict": True,
     "description": "Get the governing data record for this engineer's plant and machine (machine > plant > company > "
                    "library). record_type: allowance_table, board_material, flute_profile, grade_table, factor_set, "
                    "formula, box_style, tolerance_spec, machine_spec, plant. filter_key is a dotted path such as "
                    "flute.code, factors.kind or style.code; filter_value its value.",
     "input_schema": {"type": "object", "additionalProperties": False,
                      "required": ["record_type", "filter_key", "filter_value", "approved_only"],
                      "properties": {"record_type": {"type": "string", "enum": [
                          "allowance_table", "board_material", "flute_profile", "grade_table", "factor_set", "formula",
                          "box_style", "tolerance_spec", "machine_spec", "plant"]},
                          "filter_key": STR_OR_NULL, "filter_value": STR_OR_NULL, "approved_only": {"type": "boolean"}}}},
]
CALC_FOR_AGENT = [t for t in CALC_TOOLS if t["name"] != "lookup_record"]
ALL_TOOLS = KB_TOOLS + CALC_FOR_AGENT
CALC_NAMES = {t["name"] for t in CALC_FOR_AGENT}


@dataclass
class ToolLog:
    name: str
    input: dict
    output: dict
    is_error: bool


@dataclass
class ToolBox:
    service: KnowledgeService
    ctx: UserContext
    log: list[ToolLog] = field(default_factory=list)

    def run(self, name: str, args: dict) -> tuple[str, bool]:
        """Execute a tool; return (JSON text for the tool_result, is_error)."""
        try:
            if name == "kb_search":
                out = self.service.search(self.ctx, args["query"], args.get("k") or 8, args.get("kinds"),
                                          args.get("material_families"))
            elif name == "kb_read":
                out = self.service.read(self.ctx, args["chunk_id"])
            elif name == "kb_resolve":
                out = self.service.resolve(self.ctx, args["record_type"], args.get("filter_key"),
                                           args.get("filter_value"), bool(args.get("approved_only")))
            elif name in CALC_NAMES:
                out = calc_dispatch(name, args)
            else:
                out = {"error": f"unknown tool {name!r}"}
        except (KeyError, TypeError, ValueError) as e:
            out = {"error": f"{type(e).__name__}: {e}"}
        result = out.get("result", out) if isinstance(out, dict) else out
        is_error = isinstance(result, dict) and "error" in result
        self.log.append(ToolLog(name, args, out, is_error))
        return json.dumps(out, default=str), is_error
