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

## Status log

### Wave 1: complete (2026-11-09). 81 of 135 budgeted searches used

| Agent | Searches | Result |
|---|---|---|
| Strength & freight rules | 12 | Item 222 single/double/triple-wall tables completed from the FBA-hosted Walmart spec; FBA time/RH multipliers confirmed (70 %RH = 0.80); FBA 2021 stacking-pattern study; overhang ranges from the FBA/Virginia Tech reports; ECT methods resolved (T 811 waxed ≈ ISO 13821; T 839 clamp; T 838/T 839 ≈ ISO 3037); T 820 withdrawn → T 836 |
| Standards & testing | 44 | Standards index VERIFY 57 → 9; ISTA 3A drops 9+8 / 9+7 and 0.53/0.46 Grms; 6-Amazon SIOC A–H; Over Boxing revised Mar 2026, PFP cut-off 1 Aug 2026; ASTM/ISO/TAPPI current editions |
| Sustainability & print | 25 | All SOURCE PENDING sections filled; PPWR checked against the EUR-Lex text (grades, Art. 24 empty space, Art. 29 cardboard exclusion, labelling); FBA 2025 repulpability standard; Cepi v3; LCA figures; US EPR dates; GS1 ITF-14 |

Review queue: 320 → 218 items.

**Carried to wave 3** (needs the hosts added after wave 1):
- Kellicutt (FPL R1911-A on ir.library.oregonstate.edu)
- Urbanik–Frank
- handhole/vent factors (Singh et al. 2008)
- print strength loss (MDPI 2021 crush study)
- NMFC Item 222 current status

**Needs purchased standards:**
- ASTM D4169-23e1 tables (cycles, assurance-level drop heights, schedules D/F/G, vibration Grms)

**Hosts that still block automated reads:**
- iso.org and astm.org (bot walls)
- www.fpl.fs.usda.gov (502)
- amazon.com, Lansmont, state agency sites

### Wave 2: complete (2026-11-09). 33 of 135 budgeted searches used

| Agent | Searches | Result |
|---|---|---|
| Styles & terminology | 1 | Read the official FEFCO 12th-edition, FEFCO/ESBO 11th-edition and ECMA 2009 PDFs; FEFCO VERIFY 28 → 5, ECMA 14 → 0; family 08 (retail/e-commerce 0801–0887) confirmed; ECMA style codes confirmed from the drawings |
| Dimensions & tooling | 17 | RSC `k_s = [1,1,2]` confirmed (FEFCO/VDW Quality Catalogue, Atlantic table); PMMI TR2.1 tolerances, warp limits, FEFCO R110 warp factor; CITO creasing formulas; BC caliper corrected to 6.6 mm; 38 → 16 VERIFY |
| Materials | 15 | Full Cepi grade list (5th ed.) limit tables; kraftliner burst conflict resolved; DS Smith typical values; RCT-from-SCT (L&W); DIN 19303 bulk bands; carton grain-direction convention |

Technique note: reading the primary PDFs directly with `curl` + `pdftotext` costs no searches and gives far better data. Most mill websites (SCA, Saica, Mondi, Smurfit Westrock, Stora Enso, Metsä, Billerud, IP, PCA) are still blocked.

### Wave 3: running
