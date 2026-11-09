---
id: card.lib.tolerance.pmmi-tr2-1-rsc
record_id: lib.tolerance.pmmi-tr2-1-rsc
record_type: tolerance_spec
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: reference
source_refs:
- kb.dimensional.tolerances#S3
- kb.dimensional.tolerances#S2
- kb.dimensional.tolerances#S4
- kb.dimensional.tolerances#S7
- kb.dimensional.tolerances#S8
generated_from: data/library/tolerances/pmmi-tr2-1-rsc.yaml
---

# PMMI B155 TR2.1-2018 tolerances for RSC containers

> Data card generated from `data/library/tolerances/pmmi-tr2-1-rsc.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **reference**. Do not edit; change the record instead.

**Notes:** FBA/PMMI B155 TR2.1-2018 is a voluntary technical report; it states it is not a standard and not normative. plus_mm / minus_mm are magnitudes (minus_mm: 1.5 means -1.5 mm). Inch values are primary; mm are the corpus conversions. VERIFY (fishtail): the report's soft conversion of 3/16 in is 4.5 mm, exact is 4.76 mm; max_mm carries the exact 4.76 mm because the inch value governs. Flap-score alignment 3/16 in carries the exact 4.76 mm (no report conversion given). Warp rows are the general limits (approx. 2.1 % of span); the high-speed (>= 50/min) limits belong to TR2.2 only and are not in this record. TR2.1 sets no inside-dimension tolerance for the erected box; derive one by stack-up. AICC cites a usual joint gap design target of 3/8 in (9.5 mm) [S7]; the earlier AICC '1/16 in minimum' [S8] is the flap-end value, not a conflict.

## Values

Applies to: RSC (top- and end-opening), B or C single wall, burst 150-275 psi or ECT 26-44 lbf/in [4.5-7.7 kN/m], panels 4-25 in [10.2-63.5 cm], for automatic erecting, filling and closing. Dimension basis: score.

| feature | plus_mm | minus_mm | note | max_mm | min_mm | per_span_mm |
|---|---|---|---|---|---|---|
| panel, score to score (flat) | 1.5 | 1.5 | ±1/16 in |  |  |  |
| overall flat blank | 3 | 3 | ±1/8 in |  |  |  |
| slot depth from flap-score centreline | 3 | 3 | ±1/8 in |  |  |  |
| slot centring relative to aligning scores |  |  | within 1/16 in | 1.5 |  |  |
| manufacturer's joint gap at flap scorelines |  |  | 1/8 in to 1/2 in (clause 5.1.2) | 12.7 | 3 |  |
| manufacturer's joint fishtail (gap variation on one box, at flap scorelines) |  |  | 3/16 in governs (PMMI states inches); exact 4.76 mm. The report's soft conversion is 4.5 mm. | 4.76 |  |  |
| manufacturer's joint gap at flap ends |  |  | not less than 1/16 in |  | 1.5 |  |
| flap-score alignment at joint (corrugator scores) |  |  | within 3/16 in | 4.76 |  |  |
| major flap gap on closed RSC |  |  | 1/4 in max; major flaps should not overlap | 6.4 |  |  |
| score fold |  |  | must allow a 180° fold (90° each way) without fracture or continuous checking |  |  |  |
| warp, max gap against straight edge, 12 in span |  |  | 1/4 in per 12 in | 6.4 |  | 305 |
| warp, max gap against straight edge, 24 in span |  |  | 1/2 in per 24 in | 12.7 |  | 610 |
| warp, max gap against straight edge, 36 in span |  |  | 3/4 in per 36 in | 19 |  | 915 |
| warp, max gap against straight edge, 48 in span |  |  | 1 in per 48 in | 25.4 |  | 1219 |

## Sources

- `kb.dimensional.tolerances#S3`
- `kb.dimensional.tolerances#S2`
- `kb.dimensional.tolerances#S4`
- `kb.dimensional.tolerances#S7`
- `kb.dimensional.tolerances#S8`
