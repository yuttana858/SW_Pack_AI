"""The assistant's agent loop on the Claude Messages API.

Manual loop (not the beta tool runner) so that every tool call is executed through the user's
scoped ToolBox, logged for audit, and so refusal / max_tokens / pause_turn are handled
explicitly. History is append-only: assistant content is appended exactly as returned
(thinking blocks included), never edited, as preserved thinking requires.

Model: claude-opus-5-5 with adaptive thinking (always on for this model) and an explicit
effort level. Server-side refusal fallback is enabled (`fallbacks="default"`), so a declined
request is re-run on a fallback model inside the same call.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import anthropic

from kb.service import KnowledgeService, UserContext

from .checks import check_answer
from .prompt import system_prompt
from .tools import ALL_TOOLS, ToolBox, ToolLog

FALLBACK_BETA = "server-side-fallback-2026-07-01"


@dataclass(frozen=True)
class AgentConfig:
    model: str = "claude-opus-5-5"
    effort: str = "medium"            # Q&A default; use "high" for design work
    max_tokens: int = 16000
    max_turns: int = 16               # model calls per question (guards runaway loops)
    fallbacks: str | None = "default"


@dataclass
class AgentResult:
    answer: str
    stop_reason: str
    tool_calls: list[ToolLog]
    warnings: list[str]
    messages: list[dict[str, Any]]    # full append-only history, reusable for the next turn
    release_id: str
    usage: dict[str, int] = field(default_factory=dict)
    refusal: dict[str, Any] | None = None
    served_by: str | None = None

    @property
    def used_calculator(self) -> bool:
        return any(t.name not in ("kb_search", "kb_read", "kb_resolve") for t in self.tool_calls)


def context_note(ctx: UserContext) -> str:
    parts = [f"plant: {ctx.plant or 'none (library and company data only)'}"]
    if ctx.machine:
        parts.append(f"machine: {ctx.machine}")
    if ctx.families:
        parts.append(f"material families: {', '.join(ctx.families)}")
    return "Engineer context — " + "; ".join(parts) + "."


class Assistant:
    def __init__(self, service: KnowledgeService, client: Any | None = None, config: AgentConfig = AgentConfig()):
        self.service, self.config = service, config
        self.client = client or anthropic.Anthropic()

    def _request(self, messages: list) -> Any:
        kw: dict[str, Any] = dict(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            system=[{"type": "text", "text": system_prompt(), "cache_control": {"type": "ephemeral"}}],
            tools=ALL_TOOLS,
            messages=messages,
            output_config={"effort": self.config.effort},
            cache_control={"type": "ephemeral"},     # caches the growing conversation prefix
        )
        if self.config.fallbacks:
            kw.update(betas=[FALLBACK_BETA], fallbacks=self.config.fallbacks)
        return self.client.beta.messages.create(**kw)

    def ask(self, question: str, ctx: UserContext, history: list[dict] | None = None) -> AgentResult:
        messages = list(history or [])
        first = not messages
        content = f"{context_note(ctx)}\n\n{question}" if first else question
        messages.append({"role": "user", "content": content})
        box = ToolBox(self.service, ctx)
        usage: dict[str, int] = {}
        response = None
        for _ in range(self.config.max_turns):
            response = self._request(messages)
            for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"):
                usage[k] = usage.get(k, 0) + (getattr(response.usage, k, 0) or 0)
            stop = response.stop_reason
            if stop == "refusal":
                d = getattr(response, "stop_details", None)
                return self._result("", stop, box, messages, usage, response,
                                    ["the request was declined by the model's safety system"],
                                    refusal={"category": getattr(d, "category", None), "explanation": getattr(d, "explanation", None)})
            messages.append({"role": "assistant", "content": response.content})
            if stop == "pause_turn":
                continue
            if stop == "max_tokens":
                return self._result(self._text(response), stop, box, messages, usage, response,
                                    ["answer was cut off at max_tokens; pending tool calls were not run"])
            calls = [b for b in response.content if getattr(b, "type", None) == "tool_use"]
            if stop != "tool_use" or not calls:
                text = self._text(response)
                return self._result(text, stop, box, messages, usage, response, check_answer(text, box.log))
            results = []
            for b in calls:
                out, err = box.run(b.name, dict(b.input))
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": out, **({"is_error": True} if err else {})})
            messages.append({"role": "user", "content": results})   # all results in ONE message
        return self._result(self._text(response) if response else "", "max_turns", box, messages, usage, response,
                            [f"stopped after {self.config.max_turns} model calls without a final answer"])

    @staticmethod
    def _text(response) -> str:
        return "\n".join(b.text for b in response.content if getattr(b, "type", None) == "text").strip()

    def _result(self, text, stop, box, messages, usage, response, warnings, refusal=None) -> AgentResult:
        served = getattr(response, "model", None) if response is not None else None
        return AgentResult(answer=text, stop_reason=stop, tool_calls=box.log, warnings=list(warnings), messages=messages,
                           release_id=self.service.manifest.get("release_id", "?"), usage=usage, refusal=refusal,
                           served_by=served)
