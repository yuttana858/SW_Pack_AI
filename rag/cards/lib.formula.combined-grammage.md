---
id: card.lib.formula.combined-grammage
record_id: lib.formula.combined-grammage
record_type: formula
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: derived
source_refs:
- kb.materials.flutes
generated_from: data/library/formulas/combined-grammage.yaml
---

# Combined board grammage

> Data card generated from `data/library/formulas/combined-grammage.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **derived**. Do not edit; change the record instead.

## Values

```
GSM = Σ liners + Σ (medium × α) + adhesive
```

| symbol | meaning | SI | US |
|---|---|---|---|
| α | take-up factor | - | - |

**Valid for:** Any wall count.

**Limitations:** Adhesive from mill/plant data.

**Calculator:** `packcalc.board.combined_grammage` (tested against the corpus worked examples). Always compute with the calculator rather than by hand.

## Sources

- `kb.materials.flutes`
