---
id: card.lib.factors.pallet-deck
record_id: lib.factors.pallet-deck
record_type: factor_set
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: industry-typical
source_refs:
- kb.performance.environmental-factors#S2
- kb.performance.stacking-load-calc#S2
generated_from: data/library/factor-sets/pallet-deck.yaml
---

# BCT multiplier for pallet deckboard gaps

> Data card generated from `data/library/factor-sets/pallet-deck.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **industry-typical**. Do not edit; change the record instead.

**Notes:** Single secondary source (ipack compression-loss table) [S2]; the same table's interlock multipliers were found internally inconsistent, so treat this row with caution (VERIFY against the Fibre Box Handbook). Deckboard gaps concentrate the load of upper pallets on the boxes below; flexible pallets reduce support further.

## Values

Kind: **pallet-deck**

| condition | range | basis |
|---|---|---|
| pallet deckboard gap (10-25 % loss) | 0.75 – 0.9 | lab BCT at 23 °C / 50 %RH on full flat support; multiplier = 1 - fractional loss |

## Sources

- `kb.performance.environmental-factors#S2`
- `kb.performance.stacking-load-calc#S2`
