# SW Pack AI — Data Framework

How packaging knowledge and engineering data are structured, governed and kept in sync
between the RAG assistant and Auto3D. The goal is software engineers can trust as an
industry-standard packaging development tool. It builds on `docs/PLAN.md` (system
architecture) and `corpus/README.md` (the research corpus).

---

## 1. Design principles

1. **One source of truth per number.** Every engineering value (a take-up factor, an allowance, a tolerance, a board's ECT) lives in exactly one structured record. The RAG text, the Auto3D payloads and the calculation engine are all *generated from* that record. They are never typed in twice.
2. **Most specific data wins, and the answer says which data it used.** Machine data overrides plant data, which overrides company data, which overrides the engineering library and published references. Every answer and every CAD change records the tier, scope and version it used.
3. **Numbers come from code, not from the model.** Claude chooses the method and explains the result. The arithmetic is done by a tested calculation library that it calls as a tool.
4. **Automatic where it is safe, manual where it matters.** Reference and library data update through an automated pipeline with review gates. Plant and machine data are entered by people and approved. Once approved, they propagate automatically.
5. **Everything is versioned and reproducible.** A design saved today can be re-checked next year against the exact dataset versions it was built with.

---

## 2. Data tiers and scopes

```
 most specific ──────────────────────────────────────────────► most general
 ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
 │ L4 Machine   │  │ L3 Plant     │  │ L2 Company   │  │ L1 Eng.      │  │ L0 Reference │
 │ line / press │→ │ site data    │→ │ standards    │→ │ library      │→ │ corpus       │
 │ manual       │  │ manual       │  │ manual       │  │ auto + review│  │ auto + review│
 └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

| Tier | What it holds | Who updates | How | Example |
|---|---|---|---|---|
| **L0 Reference** | Published knowledge: standards summaries, research, formulas, regulations (today's `corpus/`) | Research pipeline | Automatic research waves, then an engineer clears VERIFY items | McKee formula; FEFCO style descriptions; PPWR dates |
| **L1 Engineering library** | Structured tables taken from L0: flute profiles, take-up ranges, default allowance factors, grade tables, environmental factor sets, formula registry | Data stewards | Pipeline proposes, steward approves | C-flute take-up 1.40–1.45; RSC `k_s = [1,1,2]` |
| **L2 Company** | House standards: approved board catalogue, house design rules, customer specs, approved safety factors | Engineering standards owner | Manual entry with approval | "Minimum safety factor 4 for grocery" |
| **L3 Plant** | Site reality: supplier-certified board records, measured tolerances, test results, local suppliers | Plant QA / engineering | **Manual only**, with approval | Plant A, supplier X 32ECT C: caliper 3.95 ± 0.12 mm |
| **L4 Machine** | Per line or press: capability envelope, score profiles, allowance overrides, achievable tolerances | Plant engineering | **Manual only**, with approval | Plant A, FFG-2: max blank 2800×1600 mm, joint ±1.0 mm |

**Scope key.** Every record carries a `scope`, one of: `global`, `company`, `plant:<plant_id>`, or `machine:<plant_id>/<machine_id>`.

**Resolution rule.** For a lookup such as "allowance factors for an RSC, C-flute, on machine FFG-2 at Plant A", the resolver tries scopes from most to least specific and returns the first approved, in-effect record. It reports which record it chose and the alternatives it skipped. A record can narrow a range from a more general tier but never widen it without a flagged override.

---

## 3. Two representations, generated from one source

```
                 ┌────────────────────────────┐
                 │  data/  (structured, git)  │  YAML records + JSON Schemas
                 │  + Postgres (L2–L4, live)  │  one record per value set
                 └──────────────┬─────────────┘
          generate              │              generate
   ┌────────────────────────────┼─────────────────────────────┐
   ▼                            ▼                             ▼
RAG "data cards"         calc library (packcalc)        Auto3D payloads
(Markdown, versioned)    tools Claude calls              materials.update,
+ narrative corpus/      tested against golden          measurements.update,
                         worked examples                 fefco.preset inputs
```

- **Narrative knowledge** (explanations, why, best practice) stays in `corpus/` Markdown.
- **Numeric knowledge** moves into `data/` as typed records. Numeric tables in the corpus are replaced by generated "data cards", so text and data cannot drift apart. During migration, a CI check flags any number that appears in both places with different values.
- **Plant and machine data** live in Postgres behind a small admin UI (forms, approval, audit). They are exported to `data/`-shaped snapshots for reproducibility.

---

## 4. Canonical record model

Every record type shares one envelope (`schemas/envelope.schema.json`):

| Field | Purpose |
|---|---|
| `id`, `type`, `version` (semver) | Identity and change tracking |
| `scope` | `global` / `company` / `plant:<id>` / `machine:<plant>/<machine>` |
| `tier` | L0–L4 |
| `status` | draft / reviewed / approved / retired |
| `confidence` | reference / industry-typical / derived / supplier-certified / measured |
| `provenance` | Source ids (corpus `[S#]`), method, measured_by, measured_on, sample size |
| `effective_from` / `effective_to` | Lets a value change on a date without losing history |
| `supersedes` | Previous record ids |
| `approved_by`, `approved_on` | Required for L2–L4 and for L1 promotion |
| `units` | Canonical SI declared per field; conversions happen only at the edges |

Record types for the foundation (schemas in `schemas/`):

| Type | Key content | Consumers |
|---|---|---|
| `board_material` | Liners and medium, flute, caliper ± tolerance, ECT/burst/FCT, moisture, take-up, Auto3D allowance factors | RAG, calc, Auto3D `packaging.materials.update` |
| `allowance_table` | Style × flute × score profile → `k_s`, `k_o` per [L, W, H], joint width, slot width | calc, Auto3D measurement basis |
| `tolerance_spec` | Dimension, caliper, joint gap, fishtail, warp, score position; worst-case and RSS | calc, QA, RAG |
| `machine_spec` | Machine type; sheet min/max; caliper and flute range; speed; score profiles; die type; print units; register and joint tolerances; overrides | Design feasibility checks, routing, RAG |
| `plant` | Location, climate profile (RH/temperature for factors), lines, suppliers, default standards | Resolver, RAG filters |
| `formula` | Expression id, variables with units, validity range, sources, golden test cases | calc library registry, RAG explanation cards |
| `factor_set` | Environmental and stacking multipliers with conditions (RH, days, pattern, overhang) | Stacking/BCT calc |
| `box_style` | FEFCO/ECMA code, panels, flap rules, blank formula id, Auto3D generator support | Auto3D generation, RAG |
| `test_result` | Lab result linked to a material/design: method, conditioning, n, mean, CoV | Calibrates plant data and models |

---

## 5. Synchronisation pipeline ("auto update")

Everything runs as Modal functions, triggered by git pushes (L0/L1) or database change events (L2–L4).

```
change ─► validate ─► diff ─► gate ─► publish ─► verify ─► record
```

1. **Validate.** Schema, units (pint), ranges and physical sanity checks: caliper inside the flute's range; `k_o ≥ k_s`; ECT consistent with liner SCT within tolerance; take-up inside the flute range. Also cross-tier checks: a plant value outside the library range must be flagged.
2. **Diff.** Records what changed and which downstream items are affected: RAG chunks, Auto3D records, designs using that material, eval cases.
3. **Gate.**
   - L0 text that clears validation is auto-published as `draft` and stays below approved data in retrieval.
   - L1 changes need a data-steward approval.
   - L2–L4 are entered manually and already carry an approval, so they publish immediately after validation.
4. **Publish.**
   - **RAG:** re-chunk and re-embed only the changed documents and data cards into a new index version, then swap atomically. Every chunk carries `tier`, `scope`, `version` and `confidence` metadata so retrieval can filter by the user's plant and machine.
   - **Auto3D:** the sync connector converts approved `board_material` records into `packaging.materials.update` / `duplicate` / `activate` payloads and pushes them through the MCP connection. Library-level sync depends on Auto3D (see open items).
   - **Calc library:** formula or factor-set changes cut a new package version. Golden tests must pass before release.
5. **Verify.** After every Auto3D write, read the result back (`packaging.measurements.inspect`, `packaging.dimensions.inspect`) and compare it to the source record within tolerance. A mismatch rolls back with Undo and raises an alert.
6. **Record.** A release manifest lists dataset versions, index version, calc version and Auto3D sync status. Designs store the manifest id they were built with.

**Plant and machine data stay manual.** The pipeline never writes L3 or L4 values. It only *proposes*. For example, it may notice that measured caliper drifted from the record across 12 test results and open a change request for a plant engineer.

---

## 6. Auto3D alignment

| Need | Auto3D capability seen today | Gap / request to the Auto3D team |
|---|---|---|
| Push approved board records | `packaging.materials.update/duplicate/activate` (records are per design and travel with sessions) | A **shared material library** API (account or plant level), so records sync once rather than per design |
| Allowance convention | `insideFactors` / `outsideFactors` [L, W, H]; catalogue example `[1, 1, 2]` | Confirm semantics (working convention: caliper multiples measured from the score line) via `packaging.measurements.inspect` on a paired window |
| Headless generation for server workflows | `auto3d.headless.fefco` (reported unavailable), `headless.projects` | Enable `auto3d.write` for the agent registration |
| Knowledge base | `knowledge.paper_packaging` (Auto3D's curated corpus) | Ingest it as an L0 source; agree on a route to send approved corrections back |
| Machine feasibility | Not present | Either expose a validation hook or keep feasibility checks in the agent (calc + `machine_spec`) |
| Dataset version stamping | Not present | A metadata field on saved designs/projects for the manifest id |

---

## 7. Location and machine segmentation (future-ready now)

- Every record already carries `scope`, so adding a plant means adding records, not changing schemas.
- **User context.** Each engineer session has `plant_id`, and optionally `machine_id`. Retrieval filters to `global ∪ company ∪ plant:<id> ∪ machine:<id>/*` and ranks the most specific first.
- **Feasibility checks.** Before proposing a design, the agent checks the blank against the `machine_spec` envelope for the target line (sheet size, caliper, flute, joint type, print units). It names the constraint that fails and the lines that can run the job instead.
- **Climate-aware strength.** Each plant's and destination's climate profile selects the environmental factor set used in stacking calculations.
- **Machine allowances.** Score profiles differ by line, so `allowance_table` can be scoped to a machine. The resolver picks the machine table when the user designs for that line.

---

## 8. Quality system

| Control | Mechanism |
|---|---|
| Schema and unit validity | `tools/validate_corpus.py` (corpus) and `tools/validate_data.py` (records) in CI |
| Open questions | `docs/REVIEW-QUEUE.md`, regenerated each change; cleared by data stewards |
| Calculation correctness | Golden tests: every worked example in the corpus becomes a unit test of the calc library |
| Answer quality | Eval suite (PLAN.md §6), run nightly; a release is blocked on regression |
| Data ownership | One named steward per domain (materials, structural, dimensional, testing, sustainability, plant data) |
| Audit | Every write records who, what, when, why and the source; Auto3D writes record before/after |

---

## 9. Repository layout (target)

```
corpus/            narrative L0 knowledge (exists)
  company/         L2 narrative house standards (exists)
data/              structured records, YAML
  library/         L1 engineering library (flutes, allowances, factor sets, formulas, styles)
  company/         L2 records
  plants/<plant>/  L3 snapshot exports (source of truth is Postgres)
    machines/      L4 snapshot exports
schemas/           JSON Schemas (envelope + record types)   ← started
packcalc/          Python calc library + golden tests
pipeline/          Modal functions: validate, diff, publish (RAG, Auto3D), verify
connectors/auto3d/ MCP client, payload mappers, read-back verification
tools/             validators, review queue, migration scripts
docs/              PLAN, DATA-FRAMEWORK, RESEARCH-WAVES, REVIEW-QUEUE
```

---

## 10. Roadmap

| Step | Deliverable | Depends on |
|---|---|---|
| 1 | Finish research waves 1–3; engineers clear the high-impact VERIFY items | Network access (done), reviewer time |
| 2 | Schemas for every record type; `validate_data.py`; seed `data/library/` from the corpus (flutes, allowances, factor sets, grade tables, formulas) | Step 1 for values |
| 3 | `packcalc` library (blank size, allowances, McKee, stacking, unit conversions) with golden tests from corpus examples | Step 2 |
| 4 | Data-card generator: `data/` → Markdown cards for RAG; CI check that corpus tables match records | Steps 2–3 |
| 5 | Ingestion pipeline on Modal with metadata filters (tier, scope, version) | PLAN.md Phase 1 |
| 6 | Auto3D sync connector with read-back verification | Auto3D access fixes; shared library API |
| 7 | Plant/machine admin UI (forms, approval, audit) on Postgres; first plant onboarded | Step 2 schemas |
| 8 | Machine feasibility checks and climate-aware calculations in the agent | Steps 3 and 7 |
| 9 | Drift detection: test results vs records produce change requests | Step 7, test data flowing |

---

## 11. Decisions needed

1. **Company and plant structure.** How many plants, and which line types per plant? The answer sets the first `machine_spec` fields.
2. **Data stewards.** Who owns each domain and who approves L1 promotions?
3. **Plant data entry.** A built-in admin UI, or a spreadsheet import with approval as a first step?
4. **Auto3D roadmap.** Will Auto3D offer an account- or plant-level material library and design metadata for manifest stamping?
5. **Standards licences.** Will the company buy the TAPPI/ISO/ASTM/ISTA documents it relies on? With licensed copies, stewards can verify values against the official text; the corpus will still store only summaries.
