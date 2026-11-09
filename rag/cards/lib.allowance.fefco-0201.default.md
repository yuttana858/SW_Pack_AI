---
id: card.lib.allowance.fefco-0201.default
record_id: lib.allowance.fefco-0201.default
record_type: allowance_table
record_version: 0.2.0
tier: L1
scope: global
status: draft
confidence: derived
source_refs:
- kb.dimensional.dimensions-and-allowances
generated_from: data/library/allowances/fefco-0201-default.yaml
---

# RSC (FEFCO 0201) default allowance factors, caliper multiples

> Data card generated from `data/library/allowances/fefco-0201-default.yaml` v0.2.0. Tier L1, applies to all plants. Status **draft**, confidence **derived**. Do not edit; change the record instead.

**Notes:** k_s = [1, 1, 2] (inside -> score) is confirmed by the FEFCO/VDW Quality Catalogue v4.4 (crease dims = (L+t) x (B+t) x (H+2t)) and by the Atlantic Packaging RSC allowance table (depth allowance = 2 x length/width allowance for every flute). k_o = [2, 2, 4] is a geometric derivation with no primary source. Converters differ in the caliper they apply, not in the multiples, so plant/machine tables should record the measured caliper. 

## Values

Convention: `caliper-multiples-from-score` (inside = score − k_s·t; outside = score + (k_o − k_s)·t, per [L, W, H]).

| style | flute | k_s | k_o | joint_width_mm |
|---|---|---|---|---|
| 0201 | * | 1, 1, 2 | 2, 2, 4 | 32 |

## Sources

- `kb.dimensional.dimensions-and-allowances`
