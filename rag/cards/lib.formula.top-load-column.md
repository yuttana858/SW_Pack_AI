---
id: card.lib.formula.top-load-column
record_id: lib.formula.top-load-column
record_type: formula
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: derived
source_refs:
- kb.performance.stacking-load-calc
generated_from: data/library/formulas/top-load-column.yaml
---

# Top load on bottom box, single column

> Data card generated from `data/library/formulas/top-load-column.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **derived**. Do not edit; change the record instead.

## Values

```
F = (n − 1) · m · g
```

| symbol | meaning | SI | US |
|---|---|---|---|
| n | boxes high incl. bottom | - | - |
| m | gross box mass | kg | lb |
| F | load on bottom box | N | lbf |

**Valid for:** Column-aligned, full-face contact, no load sharing.

**Limitations:** Static only.

**Calculator:** `packcalc.stacking.top_load_column` (tested against the corpus worked examples). Always compute with the calculator rather than by hand.

## Sources

- `kb.performance.stacking-load-calc`
