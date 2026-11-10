---
id: card.lib.flute.a
record_id: lib.flute.a
record_type: flute_profile
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: industry-typical
source_refs:
- kb.materials.flutes#S15
- kb.materials.flutes#S1
- kb.materials.flutes#S2
- kb.materials.flutes#S3
- kb.materials.flutes#S16
- kb.materials.flutes#S20
- kb.materials.flutes#S4
- kb.materials.flutes#S7
generated_from: data/library/flutes/a.yaml
---

# A-flute (coarse) profile

> Data card generated from `data/library/flutes/a.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **industry-typical**. Do not edit; change the record instead.

**Notes:** Flute height is excluding facings. Range 4.0-4.9 mm is DIN 55468 [S3]; point values 4.8 mm FEFCO/Cepi [S1][S15] and 4.67 mm Nordstrand [S2] fall inside it. US table gives a flute thickness of 4.8 mm (3/16 in) [S20], a different quantity (near single-face caliper); the schema has no field for it. flutes_per_m = [108 (US table, +/-10) [S20], 110 FEFCO [S15]]. flutes_per_ft = 33 +/- 3 [S20]; FBA gives 33 [S16]. take_up range is FEFCO [S15]; take_up_typical 1.54 is Nordstrand [S2]. single_wall_caliper_mm is published combined caliper approx. 4.8-5 mm [S4][S7]. Profiles are plant-specific; replace with plant take-up.

## Values

| field | value |
|---|---|
| code | A |
| flute_height_mm | 4 – 4.9 |
| pitch_mm | 8 – 9.5 |
| flutes_per_m | 108 – 110 |
| flutes_per_ft | 30 – 36 |
| take_up | 1.5 – 1.55 |
| take_up_typical | 1.54 |
| single_wall_caliper_mm | 4.8 – 5 |
| glue_per_line_gsm | 4.5 – 5 |
| typical_uses | fragile goods, heavy stacking (less common today) |

## Sources

- `kb.materials.flutes#S15`
- `kb.materials.flutes#S1`
- `kb.materials.flutes#S2`
- `kb.materials.flutes#S3`
- `kb.materials.flutes#S16`
- `kb.materials.flutes#S20`
- `kb.materials.flutes#S4`
- `kb.materials.flutes#S7`
