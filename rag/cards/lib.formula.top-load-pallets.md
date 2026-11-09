---
id: card.lib.formula.top-load-pallets
record_id: lib.formula.top-load-pallets
record_type: formula
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: derived
source_refs:
- kb.performance.stacking-load-calc
generated_from: data/library/formulas/top-load-pallets.yaml
---

# Top load on bottom box, pallets stacked

> Data card generated from `data/library/formulas/top-load-pallets.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **derived**. Do not edit; change the record instead.

## Values

```
F = [(L−1)·m + (P−1)·(L·k·m + m_p)/k] · g
```

| symbol | meaning | SI | US |
|---|---|---|---|
| L | layers per pallet | - | - |
| k | boxes per layer | - | - |
| P | pallets high | - | - |
| m | box mass | kg | lb |
| m_p | pallet mass | kg | lb |

**Valid for:** Rigid deck, even load spread, no overhang, column layers.

**Limitations:** Deckboard gaps and overhang concentrate load.

**Calculator:** `packcalc.stacking.top_load_pallets` (tested against the corpus worked examples). Always compute with the calculator rather than by hand.

## Sources

- `kb.performance.stacking-load-calc`
