---
id: card.lib.grades.item222-triple-wall
record_id: lib.grades.item222-triple-wall
record_type: grade_table
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: reference
source_refs:
- kb.standards.rule41-item222#S17
- kb.materials.combined-board-grades#S18
- kb.materials.combined-board-grades#S19
- kb.standards.rule41-item222#S4
- kb.standards.rule41-item222#S5
generated_from: data/library/grade-tables/item222-triple-wall.yaml
---

# NMFC Item 222 / UFC Rule 41 triple-wall grades (puncture + facings or ECT)

> Data card generated from `data/library/grade-tables/item222-triple-wall.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **reference**. Do not edit; change the record instead.

**Notes:** Regulatory status: NMFC Item 222 (motor/LTL) and UFC Rule 41 (rail) are carrier tariff material rules, not performance tests; the official texts are paid publications and were not read. Values come from an Item 222-derived chart in a Walmart specification hosted by FBA, plus converter charts. As of 2026-11-09 Item 222 appears to remain in the NMFC (Docket 2026-2 Subject 32 analysis still cites Items 220, 221 and 222; no cancelling docket found) - VERIFY against the current NMFC. UFC Rule 41 supplement effective date VERIFY. Check the current tariff before certifying a box or handling a freight claim. Burst route (Table A) needs burst plus min combined facings; ECT route (Table B) needs ECT only (no facings requirement). The table system enum allows only one of item222-burst / item222-ect; each row carries both routes, so system is set to item222-ect and the burst columns are the Table A alternative. SI values are the corpus unit conversions. Triple wall has no burst route: the 700-1300 values are a minimum PUNCTURE test (in-oz per inch of tear, TAPPI T 803 / ISO 3036), not burst psi. Conflict resolved in the corpus: converter charts (Cary [S4], Nelson [S5] in rule41-item222) label them burst and Nelson lists the 240-300 lb rows as double wall - both wrong per the Item 222-derived chart. A further chart (Arlington, combined-board-grades S13: 61 ECT up to 300 lb, 82 ECT up to 500 lb) does not match and is treated as unreliable. The schema field `puncture` is unitless; the unit and the derived J/m conversion (1 in-oz/in = 0.27801 J/m) are in each row's `limits`. Facings weight includes the centre facings.

## Values

System: **item222-ect**

| wall | grade | ect_lbf_per_in | ect_kn_per_m | min_facings_lb_per_msf | min_facings_gsm | max_gross_lb | max_gross_kg | max_lwh_sum_in | max_lwh_sum_mm | puncture | limits |
|---|---|---|---|---|---|---|---|---|---|---|---|
| triple | 67 ECT / 700 puncture | 67 | 11.73 | 168 | 820 | 240 | 108.9 | 110 | 2794 | 700 | puncture_unit: in-oz per inch of tear; puncture_j_per_m_approx: 195 |
| triple | 80 ECT / 900 puncture | 80 | 14.01 | 222 | 1084 | 260 | 117.9 | 115 | 2921 | 900 | puncture_unit: in-oz per inch of tear; puncture_j_per_m_approx: 250 |
| triple | 90 ECT / 1100 puncture | 90 | 15.76 | 264 | 1289 | 280 | 127 | 120 | 3048 | 1100 | puncture_unit: in-oz per inch of tear; puncture_j_per_m_approx: 306 |
| triple | 112 ECT / 1300 puncture | 112 | 19.61 | 360 | 1758 | 300 | 136.1 | 125 | 3175 | 1300 | puncture_unit: in-oz per inch of tear; puncture_j_per_m_approx: 361 |

## Sources

- `kb.standards.rule41-item222#S17`
- `kb.materials.combined-board-grades#S18`
- `kb.materials.combined-board-grades#S19`
- `kb.standards.rule41-item222#S4`
- `kb.standards.rule41-item222#S5`
