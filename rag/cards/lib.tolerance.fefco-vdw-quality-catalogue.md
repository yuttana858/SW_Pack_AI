---
id: card.lib.tolerance.fefco-vdw-quality-catalogue
record_id: lib.tolerance.fefco-vdw-quality-catalogue
record_type: tolerance_spec
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: reference
source_refs:
- kb.dimensional.tolerances#S1
- kb.dimensional.tolerances#S11
generated_from: data/library/tolerances/fefco-vdw-quality-catalogue.yaml
---

# FEFCO/VDW Quality Catalogue v4.4 converting tolerances and AQLs

> Data card generated from `data/library/tolerances/fefco-vdw-quality-catalogue.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **reference**. Do not edit; change the record instead.

**Notes:** FEFCO Quality Catalogue written by VDW, version 4.4 (August 2014), published by FEFCO. Dimensions measured crease centreline to crease centreline (or crease centreline to outer edge) at 23 °C / 50 %RH per EN 20187 (ISO 187). plus_mm / minus_mm are magnitudes. Defect class and AQL per row (dimensional defects 2A, AQL 0.65). Dimensions > 1200 mm: tolerance by agreement; machine converting may need special tolerances. Die-cut tolerance is ±0.5 % with a minimum of ±1 mm (schema has no 'minimum tolerance' field; stated in note). Joint gap: normal widths 6 mm and 8 mm, but the catalogue does not say which goes with which wall type (VERIFY). Manually glued die-cuts need special agreement. Warp: flatness 'according to specification' (2B, AQL 1.5) expressed as rise/span %; FEFCO R 110 (2018) replaces it with Warp Factor WF = H x (500 / L)^2 (R 110 prints '/ 2' in its worked examples; the squared form is the one consistent with its figure). The FEFCO Common Footprint (±1 mm, S24) is a separate special-purpose spec and is not in this record.

## Values

Applies to: Corrugated board cases and die-cut articles (FEFCO/VDW Quality Catalogue v4.4). Dimension basis: score.

| feature | plus_mm | minus_mm | aql | note | pct | min_abs_mm |
|---|---|---|---|---|---|---|
| dimension, nominal <= 300 mm | 3 | 3 | 0.65 | item 3.2-2; class 2A |  |  |
| dimension, nominal > 300 to 700 mm | 4 | 4 | 0.65 | item 3.2-2; class 2A |  |  |
| dimension, nominal > 700 to 1200 mm |  |  | 0.65 | ±0.6 % of the dimension; item 3.2-2; class 2A | 0.6 |  |
| dimension, nominal > 1200 mm |  |  |  | by agreement |  |  |
| die-cut article dimension, flatbed die-cutting |  |  | 1.5 | ±0.5 %, minimum ±1 mm; item 3.2-3; class 2B | 0.5 | 1 |
| die-cut article dimension, rotary die-cutting |  |  | 4 | ±0.5 %, minimum ±1 mm; item 3.2-3; class 2B | 0.5 | 1 |
| slot position from longitudinal crease centreline | 2 | 2 | 1 | class 2A |  |  |
| slot depth | 5 | 5 | 1 | class 2A |  |  |
| flap-edge alignment at manufacturer's joint |  |  | 1.5 | 0.5 % of the die-cut height, minimum 3 mm; class 2B | 0.5 | 3 |
| multicolour print register | 2 | 2 |  | no AQL stated in corpus |  |  |
| joint gap, machine-glued die-cut, single wall, rotary | 4 | 4 | 4 | item 3.2-9; normal gap 6 or 8 mm; measured at gap edge on top |  |  |
| joint gap, machine-glued die-cut, single wall, flatbed | 4 | 4 | 1.5 | item 3.2-9; normal gap 6 or 8 mm; measured at gap edge on top |  |  |
| joint gap, machine-glued die-cut, double wall, rotary | 6 | 4 | 4 | item 3.2-9; normal gap 6 or 8 mm; measured at gap edge on top |  |  |
| joint gap, machine-glued die-cut, double wall, flatbed | 6 | 4 | 1.5 | item 3.2-9; normal gap 6 or 8 mm; measured at gap edge on top |  |  |
| glued joint fibre tear |  |  | 0.65 | >= 80 % fibre tear; class 2A | 80 |  |
| warp / flatness |  |  | 1.5 | according to specification; rise / span %; class 2B; see R 110 Warp Factor |  |  |

## Sources

- `kb.dimensional.tolerances#S1`
- `kb.dimensional.tolerances#S11`
