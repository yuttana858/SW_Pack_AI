---
id: card.lib.grades.item222-single-wall
record_id: lib.grades.item222-single-wall
record_type: grade_table
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: industry-typical
source_refs:
- kb.standards.rule41-item222#S17
- kb.standards.rule41-item222#S3
- kb.standards.rule41-item222#S19
- kb.standards.rule41-item222#S2
- kb.materials.combined-board-grades#S18
- kb.materials.combined-board-grades#S1
- kb.materials.combined-board-grades#S2
- kb.materials.combined-board-grades#S3
- kb.materials.combined-board-grades#S4
generated_from: data/library/grade-tables/item222-single-wall.yaml
---

# NMFC Item 222 / UFC Rule 41 single-wall grades (burst + facings or ECT)

> Data card generated from `data/library/grade-tables/item222-single-wall.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **industry-typical**. Do not edit; change the record instead.

**Notes:** Regulatory status: NMFC Item 222 (motor/LTL) and UFC Rule 41 (rail) are carrier tariff material rules, not performance tests; the official texts are paid publications and were not read. Values come from an Item 222-derived chart in a Walmart specification hosted by FBA, plus converter charts. As of 2026-11-09 Item 222 appears to remain in the NMFC (Docket 2026-2 Subject 32 analysis still cites Items 220, 221 and 222; no cancelling docket found) - VERIFY against the current NMFC. UFC Rule 41 supplement effective date VERIFY. Check the current tariff before certifying a box or handling a freight claim. Burst route (Table A) needs burst plus min combined facings; ECT route (Table B) needs ECT only (no facings requirement). The table system enum allows only one of item222-burst / item222-ect; each row carries both routes, so system is set to item222-ect and the burst columns are the Table A alternative. SI values are the corpus unit conversions. VERIFY: the 20, 35 and 50 lb rows (125/150/175 psi burst, 52/66/75 lb/MSF facings, 23/26/29 ECT) appear only in secondary converter charts, not in the Item 222-derived chart; check them against the NMFC text. Confidence is industry-typical for that reason; the 65-120 lb rows are confirmed by the Item 222-derived chart. 125 psi is described as a rarely used light-duty grade. Common parcel/LTL practice expects at least 200 burst or 32 ECT. TAPPI T 810 note that the rules use a minimum, not average, burst (one low test in six) seen only in a search extract - VERIFY.

## Values

System: **item222-ect**

| wall | grade | burst_psi | burst_kpa | ect_lbf_per_in | ect_kn_per_m | min_facings_lb_per_msf | min_facings_gsm | max_gross_lb | max_gross_kg | max_lwh_sum_in | max_lwh_sum_mm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| single | 125# / 23 ECT | 125 | 862 | 23 | 4.03 | 52 | 254 | 20 | 9.1 | 40 | 1016 |
| single | 150# / 26 ECT | 150 | 1034 | 26 | 4.55 | 66 | 322 | 35 | 15.9 | 50 | 1270 |
| single | 175# / 29 ECT | 175 | 1207 | 29 | 5.08 | 75 | 366 | 50 | 22.7 | 60 | 1524 |
| single | 200# / 32 ECT | 200 | 1379 | 32 | 5.6 | 84 | 410 | 65 | 29.5 | 75 | 1905 |
| single | 250# / 40 ECT | 250 | 1724 | 40 | 7.01 | 111 | 542 | 80 | 36.3 | 85 | 2159 |
| single | 275# / 44 ECT | 275 | 1896 | 44 | 7.71 | 138 | 674 | 95 | 43.1 | 95 | 2413 |
| single | 350# / 55 ECT | 350 | 2413 | 55 | 9.63 | 180 | 879 | 120 | 54.4 | 105 | 2667 |

## Sources

- `kb.standards.rule41-item222#S17`
- `kb.standards.rule41-item222#S3`
- `kb.standards.rule41-item222#S19`
- `kb.standards.rule41-item222#S2`
- `kb.materials.combined-board-grades#S18`
- `kb.materials.combined-board-grades#S1`
- `kb.materials.combined-board-grades#S2`
- `kb.materials.combined-board-grades#S3`
- `kb.materials.combined-board-grades#S4`
