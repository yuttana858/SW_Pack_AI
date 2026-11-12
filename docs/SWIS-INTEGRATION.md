# SWIS ↔ PACK AI integration

**SWIS** is the name engineers talk to. **PACK AI** is the system behind it: the packaging knowledge
base, tested calculators, the Claude assistant and the conversation memory. SWIS's front end (and
later the PACK AI page) sends each question to the PACK AI service and shows the answer.

```
Engineer ──Azure SSO──► SWIS front end ──────────────────────────────────────────┐
                        (signs the user in, shows answers)                       │ HTTPS
                                                                                 ▼
             https://yuttana858-swis--pack-ai.modal.run   (Modal proxy auth + service key)
             ┌──────────────────────────────────────────────────────────────────────────┐
             │ PACK AI service                                                          │
             │  /api/ask ─► assistant "SWIS" (claude-opus-5-5) ─► knowledge base + calcs│
             │  conversation memory (append-only, survives restarts)                    │
             │  /api/chunk (sources) · /api/feedback · /api/conversations               │
             └──────────────────────────────────────────────────────────────────────────┘
```

Why one assistant named SWIS, rather than a separate SWIS model calling PACK AI for knowledge:
- one AI call per answer instead of two
- one conversation memory instead of two to keep in sync
- every PACK AI accuracy control applies to what engineers see: citations, calculators for every number, grounding checks and plant scope

---

## Authentication

Every request carries **two** credentials, plus the signed-in user.

| Header | Value | Purpose |
|---|---|---|
| `Modal-Key` | proxy token id (`wk-…`) | Modal lets the request reach the service at all |
| `Modal-Secret` | proxy token secret (`ws-…`) | (pair with Modal-Key) |
| `X-Service-Key` | PACK AI service key (`PACKAI_SERVICE_KEY`) | Proves the caller is SWIS, not just anyone holding a Modal token |
| `X-User-Id` | stable user id from Azure (object id `oid`) | **Required.** Conversations belong to this id |
| `X-User-Name` | display name | Shown in the audit log |
| `X-User-Email` | email / UPN | Shown in the audit log |
| `X-User-Plants` | comma list of plant ids, e.g. `dallas` | Which plant data the user may see. Empty = library and company data only |
| `X-User-Roles` | comma list: `engineer`, `steward`, `plant-admin` | Unknown values are ignored; everyone is at least `viewer` |
| `X-SWPack-Plant` | optional: one of the user's plants | Pick the plant for this request when a user has several |

**Where user groups map to these headers:** SWIS maps Azure groups to `X-User-Plants` and `X-User-Roles`. PACK AI trusts these headers only because both credentials above are required. Keep the proxy token and the service key server-side in SWIS, never in a browser.

**Proxy token location:** proxy tokens belong to a Modal workspace. PACK AI runs in workspace `yuttana858`, environment `SWIS`; use the proxy token named **SWIS AI** from there.

---

## Conversations and session memory

- **First question:** send it without `conversation_id`. The response contains a new `conversation_id`.
- **Every follow-up:** send the same `conversation_id`. The assistant answers with the whole conversation in context, so "and at 90 %RH?" or "use the same board" refer to what was said before.
- **Storage:** conversations are stored on the server, append-only, and survive restarts and redeploys. SWIS only stores the id.
- **Plant:** a conversation stays on the plant it started with. Asking with a different plant returns `409`; start a new conversation.
- **Privacy:** a user can only read and continue their own conversations. Another user's id returns `404`.

### Ask (first question)

```bash
curl -sS https://yuttana858-swis--pack-ai.modal.run/api/ask -H "Modal-Key: $MODAL_KEY" -H "Modal-Secret: $MODAL_SECRET" -H "X-Service-Key: $PACKAI_SERVICE_KEY" -H "X-User-Id: 6f1c…" -H "X-User-Name: Jane Engineer" -H "X-User-Plants: dallas" -H "X-User-Roles: engineer" -H "Content-Type: application/json" -d '{"question": "What ECT do I need for a 12 kg box, 400 x 300 mm, 5 layers of 8 on a 25 kg pallet, 2 pallets high, 90 days at 80 %RH?", "effort": "medium"}'
```

### Ask (follow-up in the same conversation)

```bash
curl -sS https://yuttana858-swis--pack-ai.modal.run/api/ask -H "Modal-Key: $MODAL_KEY" -H "Modal-Secret: $MODAL_SECRET" -H "X-Service-Key: $PACKAI_SERVICE_KEY" -H "X-User-Id: 6f1c…" -H "X-User-Plants: dallas" -H "X-User-Roles: engineer" -H "Content-Type: application/json" -d '{"question": "And if it is stored at 90 %RH instead?", "conversation_id": "<id from the first answer>"}'
```

### Response

```json
{
  "conversation_id": "a1b2c3…",
  "message_id": "d4e5f6…",
  "answer": "Markdown answer with citations like [kb.performance.stacking-load-calc#required-bct-with-environmental-factors]",
  "citations": [{"id": "…", "found": true, "chunk_id": "…", "title": "…", "heading": "…", "confidence": "derived", "status": "draft"}],
  "warnings": ["…check before relying on this answer…"],
  "tool_calls": [{"name": "stacking_requirement", "input": {"…": "…"}, "is_error": false}],
  "stop_reason": "end_turn",
  "release_id": "e13a381f475d",
  "plant": "dallas",
  "mode": "assistant"
}
```

`effort` is `medium` for questions and `high` for design work. `mode` is `search-only` until a Claude API key is configured; in that mode the answer lists the best-matching cited sections.

### Other endpoints

| Method and path | Use |
|---|---|
| `GET /api/me` | Check the headers: returns the user as PACK AI sees them |
| `GET /api/conversations` | The user's conversations (id, title, plant, last update) |
| `GET /api/conversations/{id}` | The full transcript with citations and warnings, to re-open a session |
| `GET /api/chunk/{chunk_id}` | The full cited section or data card, for a "show source" panel |
| `POST /api/feedback` | `{message_id, rating: 1 or -1, comment?, correction?}`. A correction goes to the review queue |
| `GET /api/proposals` · `POST /api/proposals/{id}/decision` | Review queue for stewards and plant admins |
| `GET /api/config` | Service mode and knowledge release (no credentials needed beyond Modal's) |

### What SWIS should show

- **The answer**, rendered as Markdown. Turn `[chunk-id]` markers into numbered source links using `citations`.
- **`warnings`**, prominently ("check before relying on this answer").
- **The sources list** (`citations` where `found` is true), with their `status`; draft values should look different.
- **Optionally**, the tool calls as "working".

The PACK AI page in `webapp/static/` already does all of this, and can serve as the reference or as the future full harness.

---

## Answer quality and limits

- **Search-only mode:** without a Claude API key (`ANTHROPIC_API_KEY=none`), answers are search results, not written answers.
- **Before rollout:** with a key, run the answer eval (`python -m evals.run_answers`, about $4 per run) and have engineers review the question sets.
- **Very long conversations:** they are kept in full. If one ever outgrows the model's context window, server-side compaction will be added; that's not needed for normal sessions.
- **Scaling:** the service runs as one container because session memory is SQLite on a Modal Volume. Move to Postgres before scaling out.
