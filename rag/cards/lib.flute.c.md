---
id: card.lib.flute.c
record_id: lib.flute.c
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
- kb.materials.flutes#S7
generated_from: data/library/flutes/c.yaml
---

# C-flute (medium) profile

> Data card generated from `data/library/flutes/c.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **industry-typical**. Do not edit; change the record instead.

**Notes:** Flute height excluding facings: DIN 55468 range 3.2-4.0 mm [S3]; FEFCO 3.6 mm [S1][S15]; Nordstrand 3.61 mm [S2]. US flute thickness 4.0 mm (5/32 in) [S20] is a different quantity (no schema field). flutes_per_m = [128 (US table, +/-10) [S20], 130 FEFCO [S15]]. flutes_per_ft = 39 +/- 3 per US table [S20]; FBA gives 38 [S16] (both kept: VERIFY which nominal to use; they agree within the +/-3 band). take_up range FEFCO [S15], typical 1.43 Nordstrand [S2]. Other corpus values: kb.performance.board-tests-and-ect quotes C 1.45 and approx. 1.42 (both inside the FEFCO range); kb.dimensional.tolerances (FEFCO/VDW catalogue) gives C flute height >= 3.1 to < 4.0 mm, slightly different from DIN 3.2-4.0 (VERIFY). single_wall_caliper_mm approx. 3.5-4 mm [S7].

## Values

| field | value |
|---|---|
| code | C |
| flute_height_mm | 3.2 – 4 |
| pitch_mm | 6.8 – 8 |
| flutes_per_m | 128 – 130 |
| flutes_per_ft | 36 – 42 |
| take_up | 1.4 – 1.45 |
| take_up_typical | 1.43 |
| single_wall_caliper_mm | 3.5 – 4 |
| glue_per_line_gsm | 5 – 5.5 |
| typical_uses | standard shipping cases (RSC) |

## Sources

- `kb.materials.flutes#S15`
- `kb.materials.flutes#S1`
- `kb.materials.flutes#S2`
- `kb.materials.flutes#S3`
- `kb.materials.flutes#S16`
- `kb.materials.flutes#S20`
- `kb.materials.flutes#S7`
