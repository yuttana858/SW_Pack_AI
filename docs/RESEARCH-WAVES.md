# Research waves — closing the corpus review queue

The corpus is researched in **waves** so that no wave hits the shared web-search limit
(200 searches per turn, shared by every agent running at once).

## Budget rules

- At most **3 agents per wave**, each with a hard cap of **45 `WebSearch` calls**, so a wave uses ≤ 135 searches and leaves ≥ 65 spare.
- Primary documents are read with `WebFetch` (or `curl` for PDFs), which does not count toward the search limit. Searches are used only to *find* the right primary URL.
- Each agent keeps a running count of its searches and stops at 45. Anything left unresolved goes into a `## Research log` section at the end of the file, so the next wave can pick it up.
- A new wave starts only after every agent in the previous wave has finished.
- Network: these sessions run in the `SW_Pack_AI` environment, which allows FEFCO, FBA, TAPPI, ISTA, ISO, EUR-Lex, Georgia Tech RBI, USDA FPL, NMFTA, ASTM, ECMA, Wikipedia, CEPI, EPAL, GS1, FTC, 4evergreen, AICC and MSU. Ask for any other host before relying on it.

## Waves

| Wave | Agent | Files | Main targets |
|---|---|---|---|
| 1 | Strength & freight rules | `standards/rule41-item222.md`, `materials/combined-board-grades.md`, `performance/environmental-factors.md`, `performance/box-compression.md`, `performance/board-tests-and-ect.md` | Complete Item 222 / Rule 41 tables, BCT factor tables from primary sources, Kellicutt and newer BCT models, ECT method details |
| 1 | Standards & testing | `testing/standards-index.md`, `testing/distribution-testing.md` | Confirm standard titles and editions, D4169 levels II/III, ISTA 3A sequence |
| 1 | Sustainability & regulation | `sustainability/regulations-and-recyclability.md`, `printing/print-processes.md` | Sections marked SOURCE PENDING, PPWR text from EUR-Lex, US EPR dates, print strength loss, GS1 ITF-14 rules |
| 2 | Styles | `styles/fefco-codes.md`, `styles/ecma-folding-carton.md`, `terminology/glossary.md` | FEFCO 12th-edition PDF, ECMA code meanings |
| 2 | Dimensions & tooling | `dimensional/*.md`, `manufacturing/*.md` | Allowance tables, slot and joint widths, tolerances, warp, nicks, crease channel formulas |
| 2 | Materials | `materials/paper-grades.md`, `materials/flutes.md`, `materials/paperboard-carton.md` | CEPI grade limits, typical RCT/ECT, DIN 19303 |
| 3 | Logistics & cushioning | `logistics/palletization.md`, `cushioning/cushion-design.md`, `reference/units-and-conversions.md` | ISO 6780, pallet ratings, cushion material data |
| 3 | Machine capability (new) | `manufacturing/machine-capability-reference.md` | Typical capability ranges for corrugators, flexo folder-gluers, rotary and flatbed die cutters and digital presses; feeds the machine-spec schema in `docs/DATA-FRAMEWORK.md` |
| 3 | Folding carton design (new) | `styles/folding-carton-design-rules.md` | Carton design rules, glue flaps, tuck friction locks, crease and print registration tolerances |

After each wave: run `python tools/validate_corpus.py`, then `python tools/review_queue.py`, then commit and push.
