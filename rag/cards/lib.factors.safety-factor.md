---
id: card.lib.factors.safety-factor
record_id: lib.factors.safety-factor
record_type: factor_set
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: industry-typical
source_refs:
- kb.performance.environmental-factors#S8
- kb.performance.environmental-factors#S15
- kb.performance.stacking-load-calc#S6
- kb.performance.environmental-factors#S19
generated_from: data/library/factor-sets/safety-factor.yaml
---

# Overall stacking safety factors on BCT

> Data card generated from `data/library/factor-sets/safety-factor.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **industry-typical**. Do not edit; change the record instead.

**Notes:** BCT_required = F_top x SF. Preferred route: derive SF >= 1 / (product of the applicable multipliers), then add margin for dynamic/transit loads; neither route covers transit dynamics. VERIFY: Hanlon (1984) SF = 4 for long-term storage is attributed via an MSU thesis [S8] whose full text could not be read. Factors of 4 or 5 are often used [S15]. The ISTA 3E x1.4 apply-and-release compression factor [S19] is a test-method factor, not a transit or safety factor, and is deliberately not listed. No sourced transit dynamic-load factor was retrieved (VERIFY). House safety factors belong in company/ (L2) records.

## Values

Kind: **safety-factor**

| condition | value | basis | range |
|---|---|---|---|
| long-term warehouse storage - Hanlon 1984 rule of thumb (attribution VERIFY) | 4 | divisor on lab BCT at 23 °C / 50 %RH: allowable top load = BCT / SF |  |
| general practice for allowable working load from BCT |  | divisor on lab BCT at 23 °C / 50 %RH: allowable top load = BCT / SF | 4 – 5 |
| multiplier route: SF >= 1 / (m1 x m2 x ... x mn) using the other factor sets |  | derived from the product of applicable multipliers relative to lab BCT at 23 °C / 50 %RH |  |

## Sources

- `kb.performance.environmental-factors#S8`
- `kb.performance.environmental-factors#S15`
- `kb.performance.stacking-load-calc#S6`
- `kb.performance.environmental-factors#S19`
