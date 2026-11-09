---
id: card.lib.factors.stacking-pattern
record_id: lib.factors.stacking-pattern
record_type: factor_set
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: industry-typical
source_refs:
- kb.performance.environmental-factors#S3
- kb.performance.environmental-factors#S1
- kb.performance.environmental-factors#S5
- kb.performance.environmental-factors#S2
- kb.performance.stacking-load-calc#S3
- kb.logistics.palletization#S28
generated_from: data/library/factor-sets/stacking-pattern.yaml
---

# BCT multipliers for stacking pattern

> Data card generated from `data/library/factor-sets/stacking-pattern.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **industry-typical**. Do not edit; change the record instead.

**Notes:** Two generations of values are kept as separate rows: the original Fibre Box Handbook factors and the FBA/RIT 2021 study [S3]. FBA's 2021 study found columnar-aligned losses larger than the Handbook (use 0.80-0.88 for new designs); interlocked losses consistent with the Handbook; the aligned-interlocked hybrid is not yet in the Handbook. Study basis: 495 x 305 x 330 mm C-flute RSCs, 32 and 44 ECT, filled to about 20 kg, unit-load compression per TAPPI T 804. The ipack table's 0.80 / 0.60 multipliers for 40-60 % interlock loss [S2] are internally inconsistent and are NOT used. VERIFY: Kellicutt 1963 (3-high column, 23 %) and the misaligned-column value (up to 50 %) are attributed through a thesis [S5] only. kb.logistics.palletization notes that hybrid layouts may differ between sources (VERIFY) and cites McKee 1963: each 1 % of tier offset costs about 2.5 % BCT (VERIFY).

## Values

Kind: **stacking-pattern**

| condition | range | basis | value |
|---|---|---|---|
| columnar, aligned - original FBA Handbook (0-8 % loss) | 0.92 – 1 | single-box lab BCT at 23 °C / 50 %RH; multiplier = 1 - fractional loss of the stacked unit |  |
| columnar, aligned - FBA/RIT 2021 study (12-20 % loss) | 0.8 – 0.88 | single-box lab BCT at 23 °C / 50 %RH; multiplier = 1 - fractional loss of the stacked unit |  |
| columnar, aligned, 3 high - Kellicutt 1963 (23 % loss; attribution VERIFY) |  | single-box lab BCT at 23 °C / 50 %RH; multiplier = 1 - fractional loss of the stacked unit | 0.77 |
| misaligned columns - worst case, up to 50 % loss (attribution VERIFY) |  | single-box lab BCT at 23 °C / 50 %RH; multiplier = 1 - fractional loss of the stacked unit; value is the lower bound (>= 0.50) | 0.5 |
| interlocked - original FBA Handbook (40-60 % loss) | 0.4 – 0.6 | single-box lab BCT at 23 °C / 50 %RH; multiplier = 1 - fractional loss of the stacked unit |  |
| interlocked - FBA/RIT 2021 study (49-54 % loss) | 0.46 – 0.51 | single-box lab BCT at 23 °C / 50 %RH; multiplier = 1 - fractional loss of the stacked unit |  |
| aligned-interlocked hybrid - FBA/RIT 2021 study (45-49 % loss; not in Handbook) | 0.51 – 0.55 | single-box lab BCT at 23 °C / 50 %RH; multiplier = 1 - fractional loss of the stacked unit |  |

## Sources

- `kb.performance.environmental-factors#S3`
- `kb.performance.environmental-factors#S1`
- `kb.performance.environmental-factors#S5`
- `kb.performance.environmental-factors#S2`
- `kb.performance.stacking-load-calc#S3`
- `kb.logistics.palletization#S28`
