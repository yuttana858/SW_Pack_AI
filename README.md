# SW Pack AI

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

## Adding plant data

1. Copy `data/plants/_example/` to `data/plants/<plant_id>/`; set `scope: plant:<plant_id>` (machines: `machine:<plant_id>/<machine_id>`).
2. Fill in the values, set `status: approved` with `approved_by` / `approved_on`.
3. Run the commands above; CI blocks anything that fails validation.

The resolver then prefers your plant and machine records over the library automatically.
