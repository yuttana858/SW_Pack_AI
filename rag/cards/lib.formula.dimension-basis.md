---
id: card.lib.formula.dimension-basis
record_id: lib.formula.dimension-basis
record_type: formula
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: derived
source_refs:
- kb.dimensional.dimensions-and-allowances
generated_from: data/library/formulas/dimension-basis.yaml
---

# Inside / score / outside conversion

> Data card generated from `data/library/formulas/dimension-basis.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **derived**. Do not edit; change the record instead.

## Values

```
score = inside + k_s·t ; outside = inside + k_o·t   (per [L, W, H])
```

| symbol | meaning | SI | US |
|---|---|---|---|
| t | combined caliper | mm | in |
| k_s, k_o | allowance factors | - | - |

**Valid for:** Allowance factors from an allowance_table record (RSC [1,1,2] / [2,2,4]).

**Limitations:** k_o is derived, not published.

**Calculator:** `packcalc.dimensions.convert_dims` (tested against the corpus worked examples). Always compute with the calculator rather than by hand.

## Sources

- `kb.dimensional.dimensions-and-allowances`
