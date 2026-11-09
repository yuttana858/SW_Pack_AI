---
id: card.lib.factors.relative-humidity
record_id: lib.factors.relative-humidity
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
- kb.performance.environmental-factors#S7
- kb.performance.environmental-factors#S16
generated_from: data/library/factor-sets/relative-humidity.yaml
---

# BCT multipliers for relative humidity under load

> Data card generated from `data/library/factor-sets/relative-humidity.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **industry-typical**. Do not edit; change the record instead.

**Notes:** FBA BCT loss factors reproduced in [S13] (table credits USDA FPL), also [S1][S2]. Factors apply to RH under load. VERIFY: FBA updated the Handbook numbers in 2019 from a Clemson study of RH under load on modern containerboard [S16]; those values were not retrieved - check the current Handbook edition. Popil's first-order model (SCT50/SCT_RH = 0.00945 RH + 0.51) gives 0.79 at 80 %RH vs table 0.68 (less conservative); [S13] calls its ratio a 27 % loss. Use the table for design. Do not interpolate between rows without a source. Cyclic RH increases loss further with no single value. Chilled storage: treat as a humidity case at the cold-store RH (derived from [S13]); no frozen/freeze-thaw multiplier was retrieved (VERIFY).

## Values

Kind: **relative-humidity**

| condition | value | basis |
|---|---|---|
| 50 %RH (reference) | 1 | lab BCT at 23 °C / 50 %RH; RH is equilibrium RH under load; multiplier = 1 - fractional loss |
| 60 %RH | 0.9 | lab BCT at 23 °C / 50 %RH; RH is equilibrium RH under load; multiplier = 1 - fractional loss |
| 70 %RH | 0.8 | lab BCT at 23 °C / 50 %RH; RH is equilibrium RH under load; multiplier = 1 - fractional loss |
| 80 %RH | 0.68 | lab BCT at 23 °C / 50 %RH; RH is equilibrium RH under load; multiplier = 1 - fractional loss |
| 90 %RH | 0.48 | lab BCT at 23 °C / 50 %RH; RH is equilibrium RH under load; multiplier = 1 - fractional loss |
| 100 %RH | 0.15 | lab BCT at 23 °C / 50 %RH; RH is equilibrium RH under load; multiplier = 1 - fractional loss |
| cyclic RH (no single value; loss increases further) |  | lab BCT at 23 °C / 50 %RH; RH is equilibrium RH under load; multiplier = 1 - fractional loss |

## Sources

- `kb.performance.environmental-factors#S13`
- `kb.performance.environmental-factors#S1`
- `kb.performance.environmental-factors#S2`
- `kb.performance.environmental-factors#S7`
- `kb.performance.environmental-factors#S16`
