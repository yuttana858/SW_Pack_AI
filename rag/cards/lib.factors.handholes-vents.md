---
id: card.lib.factors.handholes-vents
record_id: lib.factors.handholes-vents
record_type: factor_set
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: industry-typical
source_refs:
- kb.performance.environmental-factors#S18
- kb.performance.environmental-factors#S10
- kb.performance.environmental-factors#S11
generated_from: data/library/factor-sets/handholes-vents.yaml
---

# BCT multiplier for handholes and vent holes (screening)

> Data card generated from `data/library/factor-sets/handholes-vents.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **industry-typical**. Do not edit; change the record instead.

**Notes:** VERIFY: the 10-40 % loss range comes only from the abstract of Singh et al. (2008), J. Applied Packaging Research 2(4):227-238 [S18]; the full text was not reachable, so which geometries give which loss is unknown. It does not separate handholes from vents or position from area. Use the upper end (0.60) for cut-outs near vertical edges or corners or for large vent areas. Search- extract findings only: handholes in top flaps cost less than in vertical side panels; strength falls roughly linearly with cut-out area; 0 % and 4 % cut-out boxes did not differ significantly [S10][S11]. For real designs test the box with its cut-outs (TAPPI T 804 / ISO 12048) or use FEM/cut-out models; ASTM D6804 is the handhole design guide.

## Values

Kind: **handholes-vents**

| condition | range | basis |
|---|---|---|
| handholes or vent holes in sidewalls, single-wall RSC-type box (10-40 % loss) | 0.6 – 0.9 | BCT of the same box without cut-outs (tested or predicted); multiplier = 1 - L_cutout |

## Sources

- `kb.performance.environmental-factors#S18`
- `kb.performance.environmental-factors#S10`
- `kb.performance.environmental-factors#S11`
