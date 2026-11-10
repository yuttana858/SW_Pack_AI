---
id: card.lib.factors.storage-time
record_id: lib.factors.storage-time
record_type: factor_set
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: industry-typical
source_refs:
- kb.performance.environmental-factors#S13
- kb.performance.environmental-factors#S1
- kb.performance.environmental-factors#S2
- kb.performance.environmental-factors#S5
- kb.performance.environmental-factors#S8
- kb.performance.environmental-factors#S9
- kb.performance.stacking-load-calc#S1
- kb.performance.stacking-load-calc#S2
generated_from: data/library/factor-sets/storage-time.yaml
---

# BCT multipliers for storage time under load (creep)

> Data card generated from `data/library/factor-sets/storage-time.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **industry-typical**. Do not edit; change the record instead.

**Notes:** FBA BCT loss factors as reproduced by Popil (Georgia Tech RBI) [S13], also in [S1][S2]. Factors are empirical and multiplied with other factors by convention. VERIFY: whether the storage-time factors already include some humidity effect is not stated in [S13]; check the Fibre Box Handbook text. VERIFY: an MSU study reportedly found published retention factors greatly overestimate long-term endurance [S8] (attribution not confirmed), so the product may be non-conservative. Moody & Skidmore 1966 (55 % retained after three months, attribution VERIFY) [S5] and AICC (nearly 45 % loss after 90 days humid storage) [S9] are consistent with 90 days. Kellicutt & Landt log-time relation not retrieved. Do not interpolate between rows without a source.

## Values

Kind: **storage-time**

| condition | value | basis |
|---|---|---|
| 10 days under load | 0.63 | lab BCT at 23 °C / 50 %RH, short-term compression test; multiplier = 1 - fractional loss |
| 30 days under load | 0.6 | lab BCT at 23 °C / 50 %RH, short-term compression test; multiplier = 1 - fractional loss |
| 90 days under load | 0.55 | lab BCT at 23 °C / 50 %RH, short-term compression test; multiplier = 1 - fractional loss |
| 180 days under load | 0.5 | lab BCT at 23 °C / 50 %RH, short-term compression test; multiplier = 1 - fractional loss |

## Sources

- `kb.performance.environmental-factors#S13`
- `kb.performance.environmental-factors#S1`
- `kb.performance.environmental-factors#S2`
- `kb.performance.environmental-factors#S5`
- `kb.performance.environmental-factors#S8`
- `kb.performance.environmental-factors#S9`
- `kb.performance.stacking-load-calc#S1`
- `kb.performance.stacking-load-calc#S2`
