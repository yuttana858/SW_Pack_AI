# PACK AI (project SW_Pack_AI)

Engineers talk to **SWIS**, the PACK AI assistant. Today SWIS is the PACK AI chat page at `https://yuttana858-swis--pack-ai.us-east.modal.run`, with a single-user login (Azure SSO later). Integration contract: `docs/SWIS-INTEGRATION.md`; deployment: `docs/DEPLOY.md`.

Foundation for an intelligent packaging-development assistant: a Claude-based RAG system
that grounds answers in a cited packaging knowledge base and drives Auto3D through tools.

| Path | What it is |
|---|---|
| `docs/PLAN.md` | System architecture and delivery phases (Modal, RAG, Auto3D connector) |
| `docs/DATA-FRAMEWORK.md` | Data tiers (reference → library → company → plant → machine), sync pipeline, segmentation |
| `docs/RESEARCH-WAVES.md` | How the corpus is researched within search limits; wave log |
| `docs/CLOUD-AI-ROADMAP.md` | Knowledge access for all AIs, CSV/PDF intake, Auto3D alignment, machine limits, new material families, Cloud AI build phases |
| `docs/REVIEW-QUEUE.md` | Every value still marked VERIFY, for engineer review (generated) |
| `corpus/` | L0 narrative knowledge base, cited Markdown (see `corpus/README.md`, inventory in `corpus/INDEX.md`) |
| `corpus/company/` | Your own certified data: overrides everything else |
| `schemas/` | JSON Schemas for every structured record type |
| `data/library/` | L1 engineering library: formulas, allowances, flutes, grade tables, factor sets, styles, tolerances |
| `data/plants/<plant>/` | L3/L4 plant and machine records (`_example/` shows the shape) |
| `packcalc/` | Tested calculation library the assistant calls instead of doing arithmetic |
| `swdata/` | Record loading and scope resolution (machine > plant > company > library) |
| `rag/cards/` | Generated data cards for the RAG index; never hand-edit |
| `importers/`, `templates/` | CSV importer, column profiles and fill-in templates for plant/supplier data |
| `connectors/auto3d/` | Auto3D board-database CSV bridge (plan, merge, verify) |
| `agent/` | Claude tool definitions and dispatcher |
| `kb/` | Knowledge service: chunker, hybrid index (BM25 + optional embeddings), release manifest, retrieval eval |
| `mcp_server/` | `swpack-kb` MCP server (read-only tools: search, read, resolve, calculators) |
| `deploy/modal_app.py` | Modal deployment (index build into a Volume, `/mcp` HTTP endpoint); not deployed yet |
| `assistant/` | Assistant core: Claude agent loop (`claude-opus-5-5`), scoped tools, grounding checks, CLI |
| `webapp/` | Web app: chat UI, sign-in (OIDC or dev), conversations, feedback, corrections review queue |
| `evals/` | Retrieval and answer-quality eval sets (seed sets; engineers extend) and the live answer-eval runner |
| `.mcp.json` | Lets Claude Code sessions in this repo attach `swpack-kb` automatically |
| `tools/` | Validators, review queue, card generator |
| `tests/` | Golden tests (corpus worked examples), registry and resolver tests |

## Everyday commands

```bash
pip install -r requirements.txt
```

```bash
python tools/validate_corpus.py corpus && python tools/validate_data.py && python tools/generate_cards.py --check && python -m pytest -q tests
```

```bash
python tools/generate_cards.py
```

```bash
python tools/review_queue.py
```

## Knowledge service (local)

```bash
python -m kb.build
```

```bash
python -m kb.evaluate --k 10
```

```bash
python -m mcp_server.server --http --port 8765
```

Claude Code picks up `swpack-kb` from `.mcp.json` when opened in this repo. Set `SWPACK_PLANT` / `SWPACK_MACHINE` there to scope answers to a plant.

## Assistant (needs a Claude API key; each question spends credit)

```bash
python -m assistant.cli "What ECT do I need for a 12 kg box stacked 5 high for 90 days?" --plant <plant> -v
```

```bash
python -m evals.run_answers --dry-run
```

## Web app

```bash
python -m webapp.app
```

Open http://127.0.0.1:8080. Without an identity provider it offers developer sign-in personas. Without an API key it runs in search-only mode. Production uses **Sign in with GitHub** for members of the company GitHub organization; deploy steps are in `docs/DEPLOY.md`.

## Adding plant data

1. Copy `data/plants/_example/` to `data/plants/<plant_id>/`; set `scope: plant:<plant_id>` (machines: `machine:<plant_id>/<machine_id>`).
2. Fill in the values, set `status: approved` with `approved_by` / `approved_on`.
3. Run the commands above; CI blocks anything that fails validation.

The resolver then prefers your plant and machine records over the library automatically.
