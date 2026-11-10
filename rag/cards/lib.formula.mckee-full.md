---
id: card.lib.formula.mckee-full
record_id: lib.formula.mckee-full
record_type: formula
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: reference
source_refs:
- kb.performance.box-compression#S1
- kb.performance.box-compression#S4
generated_from: data/library/formulas/mckee-full.yaml
---

# Full McKee with bending stiffness

> Data card generated from `data/library/formulas/mckee-full.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **reference**. Do not edit; change the record instead.

## Values

```
BCT = 2.028 · ECT^0.746 · sqrt(Dx·Dy)^0.254 · Z^0.492
```

| symbol | meaning | SI | US |
|---|---|---|---|
| ECT | edge crush | N/mm | lbf/in |
| Dx, Dy | MD/CD bending stiffness per width | N·mm | lbf·in |
| Z | perimeter | mm | in |

**Valid for:** Single-wall RSCs, tall near-square boxes buckling elastically.

**Limitations:** Constants fitted on 1963 data; refit to own boxes recommended.

**Calculator:** `packcalc.compression.mckee_full` (tested against the corpus worked examples). Always compute with the calculator rather than by hand.

## Sources

- `kb.performance.box-compression#S1`
- `kb.performance.box-compression#S4`
