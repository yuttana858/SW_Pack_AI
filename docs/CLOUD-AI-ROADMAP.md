# SW Pack AI — Cloud AI Roadmap

This document picks up from the foundation (`docs/DATA-FRAMEWORK.md`) and plans the remaining
pieces before and during the Cloud AI build:

1. Knowledge access for every AI in the ecosystem
2. Data intake: CSV and PDF
3. Auto3D alignment
4. Machine limits (min/max feasibility)
5. New material families
6. Readiness check
7. Cloud AI build phases

---

## 1. One knowledge service for every AI

**Goal:** the Cloud AI (our Modal-hosted assistant), Claude Code / Claude desktop sessions (agents like this one), and future apps all read the same knowledge, with the same scope rules, once a user signs in to the ecosystem.

**Design: the `swpack-kb` MCP server.** One Model Context Protocol server, hosted on Modal as a web endpoint (streamable HTTP), in front of the knowledge store. MCP is the standard way Claude clients attach tools, so every client uses it the same way.

| Tool | Purpose | Mutates? |
|---|---|---|
| `kb.search` | Hybrid search over corpus chunks + data cards; filters for tier, scope, material family, confidence | No |
| `kb.read` | Full corpus section or data card by id (with citations) | No |
| `kb.resolve` | Governing record for a type and filter in the user's plant/machine scope (the `swdata` resolver) | No |
| `calc.*` | The `packcalc` calculators (same definitions as `agent/tools.py`) | No |
| `feasibility.check` | Machine min/max checks (§4) | No |
| `data.propose` | Submit a change request (new value, correction) into the review queue | Creates a *proposal* only |
| `auto3d.sync_status` | Which approved materials are in the Auto3D catalogue, and drift | No |

- **Identity and scope.** Users sign in through the company identity provider (OAuth/SSO). The token carries `company`, `plant_id`, default `machine_id` and role. The server injects these into every resolve and search, so a Plant A engineer sees Plant A data first, and data from plants they are not entitled to never appears.
- **Roles.** `viewer` (read), `engineer` (read + propose), `steward` (approve L1/L2), `plant-admin` (approve L3/L4 for their plant). Approvals happen in the admin UI, not through AI tools.
- **Read-only by design.** No MCP tool writes approved data. AI clients can only *propose*. That keeps the knowledge base trustworthy even when many agents use it.
- **How each client connects:**
  - **Cloud AI (Modal):** the server's read-only tools are safe to attach through the Messages API MCP connector, or through the same host-side client used for Auto3D.
  - **Claude Code and desktop:** add the server once, e.g. `claude mcp add --transport http swpack-kb https://<kb-host>/mcp`, and sign in. The repo can also ship a project `.mcp.json` so every engineer's session picks it up automatically.
  - **Offline / CI:** the git repository remains the source of truth for L0/L1. Agents working in the repo (like this session) use the files and `packcalc` directly.
- **Versioning.** Every response includes the release manifest id (dataset, index, calc versions), so answers can be traced and reproduced.

---

## 2. Data intake: CSV now, PDF next

**CSV (built).** `importers/csv_import.py` with column profiles in `importers/profiles/` and fill-in templates in `templates/`.

```bash
python -m importers.csv_import --type board_material --scope plant:<plant> --method supplier-certificate --input boards.csv --out data/plants/<plant>/materials --dry-run
```

- Every row is mapped to a record, converted to SI (US columns such as `caliper_in`, `ect_lbf_per_in`, `burst_psi`, `basis_weight_lb_msf` are accepted), validated against `schemas/`, and reported with line numbers. If any row fails, nothing is written (unless `--partial`).
- Imported rows are **draft** unless the file was approved (`--approved-by`). Tier comes from scope: plant → L3, machine → L4.
- **Next profiles to add** as files arrive: `tolerance_spec` (house tolerances), `test_result` (lab ECT/BCT/caliper results), `allowance_table` (per-machine score allowances), `plant`.

**PDF (planned).** Supplier certificates, mill data sheets and machine brochures arrive as PDFs.

1. Upload the PDF to the intake area (admin UI or a watched storage bucket on Modal).
2. Claude reads the PDF and returns **structured output against the record schema** (a JSON-schema-constrained response), with each value's page reference.
3. The extraction is written as a **draft** record with `provenance.method: supplier-certificate` and the source document stored next to it.
4. A person compares the values side by side with the PDF page in the admin UI and approves or corrects them. Nothing extracted from a PDF is approved automatically.
5. Golden tests: a small set of real PDFs with hand-checked expected values guards extraction quality.

---

## 3. Auto3D alignment

**Found in Auto3D:** an account-level **board database** with CSV round-trip (`packaging.boards.inspect`, `packaging.boards.export`, `packaging.boards.save_csv` with revision checking, `packaging.boards.select`). This is the shared material library the framework asked for, so materials can sync at account level rather than per design.

**Built:** `connectors/auto3d/board_csv.py` and `board_columns.yaml`.

- `plan_sync()` merges approved `board_material` records into the exported catalogue:
  - It adds new boards and updates changed ones.
  - It **never deletes** rows SW Pack AI does not own; rows it owns are tagged `provenance: swpack:<id>@<version>`.
  - It flags owned rows whose record was retired, rather than deleting them.
- `verify()` re-reads the catalogue after `save_csv` and checks every value.
- `calibrated` is `true` only for approved supplier-certified or measured records, so Auto3D never shows a library default as calibrated.

**To finish once tools access and pairing work:**
1. Run `packaging.boards.export` once and save the CSV. Run `python -m connectors.auto3d.board_csv check-headers export.csv`, fix the column names in `board_columns.yaml`, and set `confirmed: true`.
2. Read `packaging.measurements.inspect` on a paired window to confirm the allowance-factor convention (`insideFactors`/`outsideFactors` measured from the score line), then mark the library allowance record reviewed.
3. Read Auto3D's own knowledge sections (`knowledge.paper_packaging_section`). The pipeline imports them as an L0 source (tagged `auto3d-kb`) and produces a **conflict report** against our library, e.g. take-up factors, flute calipers and Item 222 rows. Conflicts go to the review queue; corrections can then go back to the Auto3D team.
4. Pipeline job: after any approved board change → `plan_sync` → `save_csv` (with revision) → `verify`. The read-back result goes into the release manifest.

---

## 4. Machine min/max limits (future feature, planned now)

The `machine_spec` schema already holds each machine's envelope:
- sheet min/max, caliper range and flutes
- panel, slot and glue-lap limits
- folding styles with per-style box limits (C/E/L/H)
- speeds and tolerances

`manufacturing/machine-capability-reference.md` documents what each limit means, with a 10-point feasibility checklist.

**Feature design: `feasibility.check(design, machine | plant)`**

| Step | Check |
|---|---|
| 1 | Blank fits the sheet envelope, in the machine's axis convention (feed direction vs across) |
| 2 | Caliper and flute within range |
| 3 | Panel, flap, slot and glue-lap dimensions within the FFG/folder-gluer limits |
| 4 | Folding style supported, and box dims within that style's C/E/L/H limits |
| 5 | Print colours, print area and register tolerance vs the design's graphic tolerance |
| 6 | Joint type available (glued, stitched, taped) |
| 7 | Tolerance stack: machine tolerances vs the design's fit clearance |

- **Output:** pass, warn or fail per check, with the limiting value, the margin, and which record set it (machine record id and version). For a plant, it runs on every machine of the right kind and returns the lines that can run the job, ranked by margin.
- **Where it plugs in:**
  - the assistant, before proposing a design
  - Auto3D, after `packaging.fefco.generate`, to flag a blank no line can run
  - quoting/routing later
- **Build order:** pure function in `packcalc/feasibility.py` with golden tests from the BOBST/BHS examples, then the `feasibility.check` tool, then plant-wide routing. It needs at least one real plant's machine records.

---

## 5. New material families

New families can be added without restructuring; this is a plug-in pattern.

| Layer | What a new family adds | Example: honeycomb |
|---|---|---|
| Corpus | `corpus/<topic>/…` files with `applies_to: [honeycomb]` (topic folders stay shared; materials/testing/styles gain family files) | `materials/honeycomb-board.md`, `testing/honeycomb-tests.md` |
| Record family | `material_family` on every record (added to the envelope); a family-specific material type when properties differ | `honeycomb_material`: cell size, core height, facing grammage, flat crush, density |
| Calculators | `packcalc/<family>.py` with golden tests from the family's corpus examples | flat crush capacity, edge load of honeycomb panels |
| Styles | `box_style.system` gains family style systems | pallet/edge-board profiles, tube end-closure types |
| Importer profile | `importers/profiles/<type>.yaml` + CSV template | `honeycomb_material.csv` |
| Auto3D | Mapping only where Auto3D models that family | later |
| Research | A research wave with its own budget, as in `docs/RESEARCH-WAVES.md` | Wave H1–H3 |

Planned families and the properties that make each one different:

| Family | Distinct properties / methods | Likely new types |
|---|---|---|
| Honeycomb board | Cell size and shape, core height, facing papers, flat crush, edge crush, density | `honeycomb_material` |
| Paper tubes and cores | Ply count, winding angle, ID/OD/wall, radial crush, beam strength, end-closure styles | `tube_material`, `tube_style` |
| Molded pulp | Fibre source, process (wet/dry, thermoformed), wall thickness, draft angles, density, moisture | `pulp_material`, `pulp_tooling_spec` |
| Formed products (pressed fibre, edge protectors, formed trays) | Profile geometry, laminate build-up, compression and edge crush along length | `formed_profile` |
| Solid board, rigid boxes, foam inserts | Board type, wrap and lining, foam density and cushion curves (ties into `cushioning/`) | `solid_board_material`, `foam_material` |

**Retrieval impact:** each chunk and card carries `material_family`, so a question about molded pulp never pulls corrugated answers. Cross-family knowledge (units, pallets, test conditioning) is tagged `multi`.

---

## 6. Have we covered our bases? Readiness check

| Area | Status | Gaps that don't block the build |
|---|---|---|
| Knowledge corpus | 28 files, 312 sections, 753 sources (`corpus/INDEX.md`) | About 200 VERIFY items for engineer review; paywalled standards |
| Engineering library | 60 records, 15 formulas | All draft until stewards approve |
| Calculators | `packcalc` with golden tests | Feasibility module (needs plant data) |
| Scope model | Resolver + tiers + material families | None |
| Data intake | CSV importer + templates | PDF extraction (§2) |
| Auto3D | Board CSV bridge + verify | Column confirmation and pairing (§3) |
| Quality gates | CI: corpus, data, cards, tests | Answer-quality evals (built with the agent) |

**Verdict:** the foundation is ready for the Cloud AI build. The open items are data and review work that proceeds in parallel; none of them changes the architecture.

---

## 7. Cloud AI build phases

Model: `claude-opus-5-5`, with adaptive thinking and an effort setting per route (`medium` for Q&A, `high` for design). Server-side refusal fallback enabled. Prompt caching covers the system prompt (operating rules) and tool definitions. Everything runs on Modal.

| Phase | Deliverable | Exit test |
|---|---|---|
| **C1. Knowledge service** | Modal app: ingestion job (corpus + cards → chunks with tier/scope/family/version metadata), embeddings, hybrid index, `swpack-kb` MCP server (read-only tools, §1), release manifest | Recall@10 ≥ 0.9 on a 50-question retrieval set; Claude Code can attach the server and answer with citations |
| **C2. Assistant core** | Agent loop on the Messages API with the SDK tool runner. Calculator and KB tools; `corpus/agent/engineering-rules.md` as cached system prompt; citations; uses the user's plant scope | ≥ 85 % on the 50-question golden Q&A set; every numeric answer comes from a calculator call |
| **C3. Web front end + identity** | Chat UI, SSO, roles, plant selection, answer feedback (thumbs/corrections → proposals) | Pilot users in one plant |
| **C4. Data admin** | Admin UI: CSV upload (importer), review queue, approvals, record history; PDF extraction (§2) | First plant's materials and machines approved |
| **C5. Auto3D integration** | Board CSV sync + verify; headless FEFCO drafts; live-session co-pilot with confirmation gates (PLAN.md §4) | 20 scripted design requests produce correct drafts, with zero unapproved writes |
| **C6. Feasibility + routing** | `feasibility.check` and plant-wide line selection (§4) | Golden machine cases pass; engineers agree with the line recommendations |
| **C7. New families** | Honeycomb, then tubes, molded pulp, formed products (§5) | Family golden tests and retrieval set per family |

### Sprint C1 status (2026-11-09): built and tested locally; Modal deployment pending workspace

| Item | Status |
|---|---|
| Chunker (`kb/chunker.py`) | Done: 373 chunks (315 corpus sections, 58 data cards), citations resolved, research logs excluded |
| Hybrid index (`kb/index.py`) | Done: BM25 with packaging-code normalisation (T 839, ISO 3037, 32 ECT, 0201); dense embedder pluggable (`kb/embedders.py`: Voyage or self-hosted on Modal GPU); RRF fusion |
| Release manifest (`kb/build.py`) | Done: release id, git commit, corpus hashes, record versions, packcalc version |
| `swpack-kb` MCP server | Done: 6 read-only tools; stdio and streamable HTTP tested end to end; `.mcp.json` for Claude Code |
| Scope isolation | Done: plant/machine data visible only to that plant's users (tested) |
| Retrieval eval | Seed set of 50 questions: recall@10 = 0.98, recall@3 = 0.94 (BM25 only); CI floor 0.9. **Needs engineers** to review and extend |
| Modal app (`deploy/modal_app.py`) | Written and import-checked: `build_index`, `retrieval_eval`, `mcp_http` (proxy auth). **Needs Modal workspace** |
| Per-user identity (SSO) | Phase C3; until then the HTTP endpoint must stay behind Modal proxy auth |

**Deploy checklist (when the Modal workspace exists):**
1. `modal token new`.
2. `modal deploy deploy/modal_app.py`.
3. `modal run deploy/modal_app.py::build_index`.
4. `modal run deploy/modal_app.py::retrieval_eval`.
5. Create a proxy auth token for the Cloud AI and attach the endpoint URL + `/mcp`.
6. Optional: `modal secret create swpack-kb VOYAGE_API_KEY=...`, then rebuild with `embedder="voyage"`.

### Phase C3 status (2026-11-10): web app built and tested locally; identity provider to be chosen

| Item | Status |
|---|---|
| Web UI (`webapp/static`) | Done. Chat with numbered citation chips; source panel (full section or data card); warnings box; expandable tool audit; thumbs and corrections; conversation history; plant selector; Question vs Design-work depth; review queue; light/dark; phone layout. Browser-tested at desktop and phone widths, no console errors, no horizontal scroll |
| API (`webapp/app.py`) | Done. `/api/ask`, conversations, chunk read, feedback, proposals, decisions. Conversations are pinned to a plant and stored append-only |
| Identity (`webapp/auth.py`) | Done. OIDC verification (JWKS, issuer, audience, expiry) with group → role and plant mapping; dev personas for local use, refused in production. The plant header can only select a granted plant |
| Roles | viewer (ask), engineer (+ corrections), plant-admin (decide own plants), steward (decide all) |
| Corrections | Thumbs-down with a correction creates a proposal carrying the question, answer and cited chunks. Decisions are audited; applying accepted corrections to the corpus or records is phase C4 |
| Search-only mode | Without an API key the app returns the best-matching cited sections, so it is usable before the assistant is switched on |
| Storage | SQLite (one file, Volume on Modal, max one container); Postgres in C4 |
| Modal `web` endpoint | Written and import-checked; needs workspace, secrets and an identity provider |
| Tests | 9 API tests: sign-in, plant enforcement, privacy, feedback → proposal → role-gated decision, OIDC signature, audience and expiry checks |

**Needs your decision:** which identity provider, and the groups for roles and plants (`docs/IDENTITY-SETUP.md`).

### Sprint C2 status (2026-11-10): built and tested offline; live run needs an API key

| Item | Status |
|---|---|
| Agent loop (`assistant/agent.py`) | Done. Manual loop on `client.beta.messages.create` with `claude-opus-5-5`, explicit effort (`medium` Q&A, `high` design), server-side refusal fallback (`fallbacks="default"`), cached system prompt + tools, append-only history. Handles `tool_use` (all results in one message), `pause_turn`, `max_tokens` (no half-formed tool calls run), `refusal` (category reported), and a max-turns guard |
| Scoped tools (`assistant/tools.py`) | Done. kb_search / kb_read / kb_resolve go through the user's scope; the model cannot pick another plant; 6 calculators; every call is logged for audit |
| System prompt (`assistant/prompt.py`) | Done. Role preamble + `corpus/agent/engineering-rules.md`, byte-stable for caching; user context goes in the first user turn |
| Grounding checks (`assistant/checks.py`) | Done. Flags citations that were never retrieved and numbers not traceable to a tool result (e.g. a unit conversion done "in the head") |
| CLI (`assistant/cli.py`) | Done. Single question or `--chat`; `-v` shows the tool audit and token usage |
| Modal `ask` function | Written; needs Modal workspace + `anthropic` secret |
| Answer-quality eval | Seed set of 30 questions with programmatic grading (`evals/answers_seed.yaml`, `evals/run_answers.py`); target pass rate 85 %. Rough cost per full run ≈ $4 at list prices. **Needs an API key and your go-ahead to run; engineers should review and extend to 50+** |
| Tests | 10 offline tests with a scripted client cover every loop branch and the request shape; grader tests; every eval citation prefix exists |

**To run live:** set `ANTHROPIC_API_KEY` (or `ant auth login`), then:
1. `python -m evals.run_answers --limit 5` as a smoke test.
2. A full run.
3. Tune the prompt and effort against the results.

The first live run also confirms the strict tool schemas (nullable types) against the API.

**Original sprint scope (C1):**
1. `modal` app skeleton, secrets, Volume.
2. Chunker that honours `##` sections and front-matter, and indexes data cards.
3. Embedding job.
4. Hybrid index.
5. `swpack-kb` MCP server with `kb.search`, `kb.read`, `kb.resolve` and `calc.*`.
6. A 50-question retrieval eval set written with two engineers.
7. CI deploy to a dev environment.
