---
id: card.lib.formula.urbanik-frank
record_id: lib.formula.urbanik-frank
record_type: formula
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: reference
source_refs:
- kb.performance.box-compression#S2
generated_from: data/library/formulas/urbanik-frank.yaml
---

# Urbanik & Frank (2006) refit

> Data card generated from `data/library/formulas/urbanik-frank.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **reference**. Do not edit; change the record instead.

## Values

```
BCT = 2.186 · ECT^0.727 · sqrt(Dx·Dy)^0.273 · Z^0.454
```

| symbol | meaning | SI | US |
|---|---|---|---|
| ECT | edge crush | N/mm | lbf/in |
| Dx, Dy | bending stiffness per width | N·mm | lbf·in |
| Z | perimeter | mm | in |

**Valid for:** Single-wall RSCs within the world-wide data set (409 boxes).

**Limitations:** Not validated for double wall or tubes; flap-score losses not modelled.

**Calculator:** `packcalc.compression.urbanik_frank` (tested against the corpus worked examples). Always compute with the calculator rather than by hand.

## Sources

- `kb.performance.box-compression#S2`
