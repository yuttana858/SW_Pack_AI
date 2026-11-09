---
id: card.lib.formula.rsc-blank
record_id: lib.formula.rsc-blank
record_type: formula
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: derived
source_refs:
- kb.dimensional.blank-size-formulas
generated_from: data/library/formulas/rsc-blank.yaml
---

# FEFCO 0201 RSC blank size

> Data card generated from `data/library/formulas/rsc-blank.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **derived**. Do not edit; change the record instead.

## Values

```
BL = 2Ls + 2Ws + J ; BW = Hs + 2F ; F = Ws/2 + a
```

| symbol | meaning | SI | US |
|---|---|---|---|
| Ls, Ws, Hs | score dimensions | mm | in |
| J | joint width | mm | in |
| F | flap length | mm | in |

**Valid for:** RSC with equal flaps meeting at centre.

**Limitations:** Plants may size joint panels differently; use house panel tables.

**Calculator:** `packcalc.dimensions.rsc_blank` (tested against the corpus worked examples). Always compute with the calculator rather than by hand.

## Sources

- `kb.dimensional.blank-size-formulas`
