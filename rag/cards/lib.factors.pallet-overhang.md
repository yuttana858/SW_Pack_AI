---
id: card.lib.factors.pallet-overhang
record_id: lib.factors.pallet-overhang
record_type: factor_set
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: industry-typical
source_refs:
- kb.performance.environmental-factors#S4
- kb.performance.environmental-factors#S6
- kb.performance.environmental-factors#S14
- kb.logistics.palletization#S18
- kb.performance.stacking-load-calc#S7
generated_from: data/library/factor-sets/pallet-overhang.yaml
---

# BCT multipliers for pallet overhang

> Data card generated from `data/library/factor-sets/pallet-overhang.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **industry-typical**. Do not edit; change the record instead.

**Notes:** Handbook estimate 20-40 % loss vs measured FBA/Virginia Tech Phase 1 data [S14]: loss grows with overhang, long-side overhang costs more than short-side at the same overhang, and adjacent- side overhang (three corners unsupported) costs more than the sum of the single-side effects. The Handbook range is conservative for small single-side overhangs and about right for adjacent overhangs. Phase 2 regression covers 32 ECT B, 44 ECT C, 61 ECT C with 0.25-3.25 in overhang [S6]. VERIFY (conflicting values): environmental-factors gives the Kim et al. 2023 measured range as 0-40 % in its table but 2-40 % in its text; kb.logistics.palletization gives 2.05-40.39 % ; kb.agent.engineering-rules quotes "around 14-28 %" (which matches the full-layer result 13.78-28.21 %). The Kim row keeps the table's 1.00-0.60. Avoid overhang rather than compensate; for real designs use measured or modelled derating.

## Values

Kind: **pallet-overhang**

| condition | range | basis |
|---|---|---|
| overhang 25 mm (1 in) on one side | 0.66 – 0.86 | single-box lab BCT at 23 °C / 50 %RH with full pallet support; multiplier = 1 - fractional loss |
| overhang 50 mm (2 in) on one side and one end | 0.54 – 0.66 | single-box lab BCT at 23 °C / 50 %RH with full pallet support; multiplier = 1 - fractional loss |
| overhang, current Fibre Box Handbook estimate (20-40 % loss) | 0.6 – 0.8 | single-box lab BCT at 23 °C / 50 %RH with full pallet support; multiplier = 1 - fractional loss |
| overhang, Kim et al. 2023 / FBA Phase 1 measured range (0-40 % loss; VERIFY lower bound 0 vs 2.05 %) | 0.6 – 1 | single-box lab BCT at 23 °C / 50 %RH with full pallet support; multiplier = 1 - fractional loss |
| single-side overhang, short side, 32 ECT C (1-29 % loss) | 0.71 – 0.99 | single-box lab BCT at 23 °C / 50 %RH with full pallet support; multiplier = 1 - fractional loss |
| single-side overhang, short side, 48 ECT BC (0.2-33 % loss) | 0.67 – 1 | single-box lab BCT at 23 °C / 50 %RH with full pallet support; multiplier = 1 - fractional loss |
| single-side overhang, long side, 32 ECT C (6-32 % loss) | 0.68 – 0.94 | single-box lab BCT at 23 °C / 50 %RH with full pallet support; multiplier = 1 - fractional loss |
| single-side overhang, long side, 48 ECT BC (4-27 % loss) | 0.73 – 0.96 | single-box lab BCT at 23 °C / 50 %RH with full pallet support; multiplier = 1 - fractional loss |
| adjacent-side overhang (three corners unsupported), 32 ECT C (14-41 % loss) | 0.59 – 0.86 | single-box lab BCT at 23 °C / 50 %RH with full pallet support; multiplier = 1 - fractional loss |
| adjacent-side overhang (three corners unsupported), 48 ECT BC (15-40 % loss) | 0.6 – 0.85 | single-box lab BCT at 23 °C / 50 %RH with full pallet support; multiplier = 1 - fractional loss |
| 1 in (25 mm) single-side overhang, single box (4-19 % loss) | 0.81 – 0.96 | single-box lab BCT at 23 °C / 50 %RH with full pallet support; multiplier = 1 - fractional loss |
| 1 in x 1 in adjacent overhang, single box (22-38 % loss) | 0.62 – 0.78 | single-box lab BCT at 23 °C / 50 %RH with full pallet support; multiplier = 1 - fractional loss |
| full layer on simulated pallet, overhanging (13.78-28.21 % loss) | 0.7179 – 0.8622 | single-box lab BCT at 23 °C / 50 %RH with full pallet support; multiplier = 1 - fractional loss; multiplier derived as 1 - loss from the reported loss range |

## Sources

- `kb.performance.environmental-factors#S4`
- `kb.performance.environmental-factors#S6`
- `kb.performance.environmental-factors#S14`
- `kb.logistics.palletization#S18`
- `kb.performance.stacking-load-calc#S7`
