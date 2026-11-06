# SW Pack AI — Implementation Plan

A standalone packaging-engineering assistant built on Claude, grounded in your
own packaging knowledge through retrieval (RAG), hosted on Modal, and able to
drive Auto3D (and later the rest of your application suite) through tools.

---

## 1. What "training" means here

Anthropic does not offer self-serve fine-tuning of current Claude models, and
for this use case you would not want it anyway: packaging specs, board grades,
supplier allowances and customer standards change, and a fine-tuned model
cannot cite where an answer came from. The system "learns" packaging knowledge
in three layers instead:

| Layer | What it holds | How it reaches Claude | Updates |
|---|---|---|---|
| **Retrieval corpus (RAG)** | Your specs, SOPs, FEFCO/ECT tables, supplier board data sheets, past projects, test reports | Vector + keyword search, top chunks injected with citations | Re-index on change (minutes) |
| **System prompt + skills** | Engineering rules ("always state basis: inside/outside/score", "never call a dimension certified"), unit conventions, workflows | Cached system prompt; per-task skill files | Edit + redeploy |
| **Tools** | Live data and actions: Auto3D CAD, measurements, materials, your other apps | Tool use (MCP / custom tools) | Add adapters |

A feedback loop (Phase 5) turns engineer corrections into new corpus documents
and eval cases, which is the practical equivalent of "continued training".

---

## 2. Architecture

```
                ┌──────────────────────────── Modal ────────────────────────────┐
 Engineers ───► │  api (ASGI/FastAPI web endpoint)                              │
 (web UI, CLI,  │    ├─ auth, sessions, audit log                               │
  Slack later)  │    └─ agent loop  ──► Claude API (claude-opus-5-5)            │
                │          │  tools:                                            │
                │          ├─ search_knowledge ──► retriever                    │
                │          ├─ auto3d_* ──────────► MCP client ──► Auto3D MCP    │
                │          └─ <app>_* ───────────► adapters for other suite apps│
                │                                                               │
                │  retriever: hybrid search (vectors + BM25) + rerank           │
                │  embedder:  GPU function (open embedding model) or Voyage API │
                │  ingest:    scheduled function: parse → chunk → embed → upsert│
                │  storage:   Modal Volume (raw docs) + vector DB (pgvector /   │
                │             LanceDB on Volume) + Postgres (sessions, audit)   │
                │  evals:     scheduled function, regression suite              │
                └───────────────────────────────────────────────────────────────┘
```

### Component choices

| Concern | Recommendation | Why |
|---|---|---|
| LLM | `claude-opus-5-5`, adaptive thinking, `effort: "medium"` default, `high` for design tasks; server-side `fallbacks: "default"` for refusals | Best reasoning/price for tool-heavy engineering work |
| Agent loop | Anthropic Python SDK tool runner (`client.beta.messages.tool_runner`) with per-turn hooks | You host it on Modal; hooks give approval gates + audit logging |
| Embeddings | Anthropic has no embeddings endpoint. Option A: open model (e.g. a BGE/E5-class model) on a Modal GPU function. Option B: Voyage AI API | A keeps data in your Modal account; B is less to operate |
| Vector store | Start: LanceDB on a Modal Volume. Scale/multi-user: managed Postgres + pgvector | Zero extra infra to start; easy migration path |
| Retrieval | Hybrid (dense + BM25) → rerank → top 8–15 chunks with source IDs; Claude answers with citations | Packaging text is full of codes (0201, 32ECT, BC-flute) that pure vectors miss |
| Auto3D connection | Host-side MCP client inside the Modal app, exposing Auto3D tools to Claude as custom tools | Lets you gate every mutating call, log it and enforce allow-lists (see §4) |
| Secrets | `modal.Secret` for `ANTHROPIC_API_KEY`, Auto3D token, DB URL | Never in code or images |

### Why host-side MCP instead of the API's MCP connector

The Messages API can call a remote MCP server directly (`mcp_servers` +
`mcp_toolset`, beta `mcp-client-2025-11-20`). That is simpler, but tool calls
then execute on Anthropic's side without passing through your code. Because
Auto3D has ~90 mutating commands (geometry, materials, Library saves, paid
Meshy generation), running the MCP client in your own Modal process is the
safer default: every call passes your policy check and audit log. The
connector remains an option for a read-only "advisor" mode.

---

## 3. What Auto3D exposes today (inspected via its MCP server)

| Family | Highlights | Mutating? |
|---|---|---|
| **Headless** (no app window needed) | `auto3d.headless.inspect`, `auto3d.headless.fefco` (FEFCO 0200–0203 cut/score draft), `auto3d.headless.projects` (list/get/save/delete) | fefco, save, delete |
| **Knowledge** | `knowledge.paper_packaging` (search), `knowledge.paper_packaging_section` (terminology, fefco, papers, flutes, multiwall, performance, referenceGrades, cadReferences, dimensionalEngineering, selectionGuidance, agentRules, …) | No |
| **Packaging** (59 cmds) | `packaging.fefco.generate/preset/configure/convert_basis/catalog`, `packaging.dimensions.inspect/update`, `packaging.measurements.inspect/update`, `packaging.materials.update/activate/duplicate`, `packaging.fefco.unfold/animate/folding.check` | ~30 |
| **Design** | Objects, Materials, Camera, Animation, Rendering, Lighting, Scene, History (undo) | many |
| **AI** | Meshy text/image→3D (`ai.generate` — paid provider credits) | yes |
| **Sessions** | list / select / pair-code for live app windows | — |

Observations that shape the plan:

1. **Headless mode is the right first target for a server-side agent.** It needs
   no browser window, so the Modal agent can generate and save FEFCO drafts
   unattended. At inspection time `auto3d.headless.fefco` reported
   `available: false`, so confirm with the Auto3D side what enables it
   (likely the `auto3d.write` scope on the agent registration).
2. **Live-session commands require a paired, open app window** (pair code flow).
   Treat these as "co-pilot" features where the engineer is watching.
3. **Auto3D ships its own curated corrugated knowledge base.** Use it as a
   second retrieval source alongside your private corpus; your corpus wins on
   conflicts (supplier-specific data), and answers say which source was used.
4. **Dimensions carry a basis (inside / outside / score) and tolerances are
   explicitly *not* supplier-certified.** Bake that into the system prompt:
   the agent must always state basis and never present allowances as certified.

---

## 4. Safety and control model

Each tool is classified once, in a registry (`tools/registry.yaml`):

| Class | Examples | Policy |
|---|---|---|
| `read` | `*.inspect`, `knowledge.*`, `fefco.catalog`, `convert_basis`, `folding.check` | Auto-run |
| `write_reversible` | `dimensions.update`, `fefco.generate`, `materials.update` (all support Undo) | Auto-run in a sandbox/headless draft; require confirmation in a live session |
| `write_persistent` | `headless.projects save/delete`, `ai.project.save`, Library saves | Always require user confirmation |
| `paid` | `ai.generate`, `ai.creation.refine` | Confirmation + per-user budget |
| `blocked` | credential dialogs (`ai.connection.*`) | Never exposed to the model |

Plus: every call logged (user, session, tool, args, result, Claude request
ID); deletes need `expectedRevision`; a "dry-run" mode that returns the planned
tool sequence without executing it.

---

## 5. Phased delivery

### Phase 0 — Foundations (week 1)
- Repo layout: `app/` (Modal app), `agent/`, `rag/`, `connectors/auto3d/`,
  `evals/`, `corpus/` (manifests only, not raw docs).
- Modal project, secrets, Volume; CI running unit tests + `modal deploy --env dev`.
- Collect corpus: list document sources, owners, confidentiality level.
- **Exit:** `modal run app::health` reaches Claude and the Auto3D MCP server.

### Phase 1 — Knowledge assistant, read-only (weeks 2–3)
- Ingestion: PDF/DOCX/XLSX/HTML parsers → structure-aware chunking (keep tables
  intact; one chunk per spec row group) → metadata (doc type, FEFCO code,
  flute, board grade, supplier, revision date).
- Hybrid retriever + reranker; `search_knowledge` tool returning chunk IDs.
- Agent with read-only tools: `search_knowledge`, Auto3D `knowledge.*`,
  `packaging.fefco.catalog`, `convert_basis`.
- Answers carry citations; "I don't know" when retrieval is weak.
- **Exit:** ≥85% pass on a 50-question golden set written with your engineers.

### Phase 2 — Auto3D headless control (weeks 4–5)
- MCP client connector + tool registry/policy layer (§4).
- Workflows: "spec → box": requirements in plain language → board/flute
  recommendation (RAG) → `convert_basis` → `headless.fefco` → inspect →
  propose save → `projects save` on approval.
- **Exit:** 20 scripted design requests produce correct drafts (dimensions
  within tolerance, correct basis stated) with zero unapproved persistent writes.

### Phase 3 — Live-session co-pilot (weeks 6–7)
- Session pairing flow in the UI; agent can inspect scene, update
  dimensions/materials, run `folding.check`, unfold/animate, render.
- Confirmation UI for live writes; undo button wired to History.
- **Exit:** engineers complete 5 real jobs with the co-pilot; feedback logged.

### Phase 4 — Rest of the application suite (weeks 8+)
- One adapter per app (MCP server if the app has one; otherwise a thin
  REST/CLI wrapper exposed as custom tools) registered in the same policy layer.
- Use tool search (`defer_loading`) once the tool count passes ~50 so the
  context stays small.

### Phase 5 — Learning loop and operations (ongoing)
- Thumbs/corrections in UI → reviewed → added as corpus notes and eval cases.
- Nightly eval run on Modal schedule; alert on regression.
- Prompt caching on system prompt + tool definitions (check
  `usage.cache_read_input_tokens`); usage/cost dashboard per user.

---

## 6. Evaluation

- **Retrieval:** recall@10 on question → expected-source pairs.
- **Answers:** golden Q&A graded by rubric (correct value, correct basis/units,
  cites a source, no certified-allowance claims).
- **Actions:** scripted Auto3D tasks checked against `packaging.dimensions.inspect`
  / `packaging.measurements.inspect` output — numeric checks, not LLM grading.
- **Safety:** red-team prompts trying to trigger deletes/paid calls without approval.

---

## 7. Rough running cost (to validate in Phase 1)

| Item | Driver |
|---|---|
| Claude API | Opus 5.5 is $4 / $20 per M input/output tokens; cached prefix reads $0.20/M. A typical tool-using design turn is ~20–40K input (mostly cached) + 2–5K output |
| Modal | Web endpoint (CPU, scales to zero), embedding GPU only during ingest, nightly evals |
| Storage | Volume + Postgres; small |

---

## 8. Open questions for you

1. **Other apps in the suite:** names, and does each have an API, CLI or MCP server?
2. **Auto3D access:** MCP endpoint URL and auth method for a server-side
   agent registration; how to enable `auto3d.write` / `headless.fefco`.
3. **Corpus:** where the documents live (SharePoint, Drive, file share, PLM)
   and any confidentiality constraints (does data need to stay in your
   Modal account → choose self-hosted embeddings).
4. **Users and UI:** internal web UI, Slack, or embedded inside Auto3D?
5. **Approval policy:** who may approve persistent saves and paid Meshy calls?
