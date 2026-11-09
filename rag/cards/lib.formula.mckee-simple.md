---
id: card.lib.formula.mckee-simple
record_id: lib.formula.mckee-simple
record_type: formula
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: reference
source_refs:
- kb.performance.box-compression#S1
- kb.performance.box-compression#S4
generated_from: data/library/formulas/mckee-simple.yaml
---

# Simplified McKee BCT

> Data card generated from `data/library/formulas/mckee-simple.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **reference**. Do not edit; change the record instead.

## Values

```
BCT = 5.87 · ECT · sqrt(h · Z),  Z = 2(L + W)
```

| symbol | meaning | SI | US |
|---|---|---|---|
| BCT | predicted box compression strength | N | lbf |
| ECT | edge crush strength | N/mm | lbf/in |
| h | combined caliper | mm | in |
| Z | perimeter 2(L+W) | mm | in |

**Valid for:** Single-wall RSCs, depth >= Z/7, near-square footprint; dimensionless constant (any consistent units).

**Limitations:** Over-predicts single-wall BCT by ~7.6 % on average; ignores crushing, print, handholes; confirm by test.

**Calculator:** `packcalc.compression.mckee_simple` (tested against the corpus worked examples). Always compute with the calculator rather than by hand.

## Sources

- `kb.performance.box-compression#S1`
- `kb.performance.box-compression#S4`
