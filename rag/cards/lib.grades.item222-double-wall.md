---
id: card.lib.grades.item222-double-wall
record_id: lib.grades.item222-double-wall
record_type: grade_table
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: reference
source_refs:
- kb.standards.rule41-item222#S17
- kb.materials.combined-board-grades#S18
- kb.materials.combined-board-grades#S3
- kb.materials.combined-board-grades#S4
generated_from: data/library/grade-tables/item222-double-wall.yaml
---

# NMFC Item 222 / UFC Rule 41 double-wall grades (burst + facings or ECT)

> Data card generated from `data/library/grade-tables/item222-double-wall.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **reference**. Do not edit; change the record instead.

**Notes:** Regulatory status: NMFC Item 222 (motor/LTL) and UFC Rule 41 (rail) are carrier tariff material rules, not performance tests; the official texts are paid publications and were not read. Values come from an Item 222-derived chart in a Walmart specification hosted by FBA, plus converter charts. As of 2026-11-09 Item 222 appears to remain in the NMFC (Docket 2026-2 Subject 32 analysis still cites Items 220, 221 and 222; no cancelling docket found) - VERIFY against the current NMFC. UFC Rule 41 supplement effective date VERIFY. Check the current tariff before certifying a box or handling a freight claim. Burst route (Table A) needs burst plus min combined facings; ECT route (Table B) needs ECT only (no facings requirement). The table system enum allows only one of item222-burst / item222-ect; each row carries both routes, so system is set to item222-ect and the burst columns are the Table A alternative. SI values are the corpus unit conversions. All rows from the Item 222-derived chart; burst-ECT-weight pairings agree with converter charts. Facings weight includes the centre facing.

## Values

System: **item222-ect**

| wall | grade | burst_psi | burst_kpa | ect_lbf_per_in | ect_kn_per_m | min_facings_lb_per_msf | min_facings_gsm | max_gross_lb | max_gross_kg | max_lwh_sum_in | max_lwh_sum_mm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| double | 200# / 42 ECT | 200 | 1379 | 42 | 7.36 | 92 | 449 | 80 | 36.3 | 85 | 2159 |
| double | 275# / 48 ECT | 275 | 1896 | 48 | 8.41 | 110 | 537 | 100 | 45.4 | 95 | 2413 |
| double | 350# / 51 ECT | 350 | 2413 | 51 | 8.93 | 126 | 615 | 120 | 54.4 | 105 | 2667 |
| double | 400# / 61 ECT | 400 | 2758 | 61 | 10.68 | 180 | 879 | 140 | 63.5 | 110 | 2794 |
| double | 500# / 71 ECT | 500 | 3447 | 71 | 12.43 | 222 | 1084 | 160 | 72.6 | 115 | 2921 |
| double | 600# / 82 ECT | 600 | 4137 | 82 | 14.36 | 270 | 1318 | 180 | 81.6 | 120 | 3048 |

## Sources

- `kb.standards.rule41-item222#S17`
- `kb.materials.combined-board-grades#S18`
- `kb.materials.combined-board-grades#S3`
- `kb.materials.combined-board-grades#S4`
