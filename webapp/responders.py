"""Who answers a question: the Claude assistant, or search-only mode when no API key is configured."""
from __future__ import annotations

import os
from typing import Protocol

from assistant.agent import AgentConfig, AgentResult, Assistant
from kb.service import KnowledgeService, UserContext


class Responder(Protocol):
    mode: str

    def ask(self, question: str, ctx: UserContext, history: list | None, effort: str) -> AgentResult: ...


class AssistantResponder:
    mode = "assistant"

    def __init__(self, service: KnowledgeService, client=None):
        self.service, self.client = service, client

    def ask(self, question, ctx, history, effort):
        return Assistant(self.service, self.client, AgentConfig(effort=effort)).ask(question, ctx, history)


class SearchOnlyResponder:
    """No language model: returns the best-matching sections with citations. Lets engineers use the
    knowledge base (and lets us test the whole app) before an API key is configured."""
    mode = "search-only"

    def __init__(self, service: KnowledgeService):
        self.service = service

    def ask(self, question, ctx, history, effort):
        hits = self.service.search(ctx, question, 5)["result"]
        if not hits:
            text = "No matching sections found in the knowledge base for your scope."
        else:
            lines = ["**Search-only mode** (the AI assistant is not configured yet). Most relevant sections:", ""]
            for h in hits:
                flag = "" if h["status"] == "approved" else f" — {h['status']}, {h['confidence']}"
                where = h["title"] if h["heading"] == h["title"] else f"{h['title']} › {h['heading']}"
                lines.append(f"- **{where}**{flag} [{h['id']}]")
            text = "\n".join(lines)
        msgs = list(history or []) + [{"role": "user", "content": question}, {"role": "assistant", "content": text}]
        return AgentResult(answer=text, stop_reason="search_only", tool_calls=[], warnings=[], messages=msgs,
                           release_id=self.service.manifest.get("release_id", "?"))


def make_responder(service: KnowledgeService) -> Responder:
    choice = os.environ.get("SWPACK_RESPONDER", "auto")
    placeholder = {"", "none", "unset", "todo"}
    has_key = any((os.environ.get(k) or "").strip().lower() not in placeholder for k in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"))
    if choice == "assistant" or (choice == "auto" and has_key):
        return AssistantResponder(service)
    return SearchOnlyResponder(service)
