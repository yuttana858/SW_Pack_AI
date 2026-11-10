---
id: card.lib.formula.max-boxes-high
record_id: lib.formula.max-boxes-high
record_type: formula
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: derived
source_refs:
- kb.performance.stacking-load-calc
generated_from: data/library/formulas/max-boxes-high.yaml
---

# Maximum boxes high

> Data card generated from `data/library/formulas/max-boxes-high.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **derived**. Do not edit; change the record instead.

## Values

```
n_max = floor(BCT·Πm / (m·g)) + 1
```

| symbol | meaning | SI | US |
|---|---|---|---|
| BCT | box compression strength | N | lbf |
| m | box mass | kg | lb |

**Valid for:** As column load.

**Limitations:** Round down; confirm by test.

**Calculator:** `packcalc.stacking.max_boxes_high` (tested against the corpus worked examples). Always compute with the calculator rather than by hand.

## Sources

- `kb.performance.stacking-load-calc`
