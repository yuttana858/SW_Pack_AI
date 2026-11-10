---
id: card.lib.formula.ect-required
record_id: lib.formula.ect-required
record_type: formula
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: derived
source_refs:
- kb.performance.box-compression#S4
generated_from: data/library/formulas/ect-required.yaml
---

# Required ECT (reverse simplified McKee)

> Data card generated from `data/library/formulas/ect-required.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **derived**. Do not edit; change the record instead.

## Values

```
ECT = BCT_required / (5.87 · sqrt(h · Z))
```

| symbol | meaning | SI | US |
|---|---|---|---|
| BCT_required | required BCT incl. factors | N | lbf |
| h | caliper | mm | in |
| Z | perimeter | mm | in |

**Valid for:** As simplified McKee.

**Limitations:** Re-check with the chosen grade's real caliper.

**Calculator:** `packcalc.compression.ect_required` (tested against the corpus worked examples). Always compute with the calculator rather than by hand.

## Sources

- `kb.performance.box-compression#S4`
