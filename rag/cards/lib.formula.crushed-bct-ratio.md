---
id: card.lib.formula.crushed-bct-ratio
record_id: lib.formula.crushed-bct-ratio
record_type: formula
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: derived
source_refs:
- kb.performance.board-tests-and-ect
generated_from: data/library/formulas/crushed-bct-ratio.yaml
---

# BCT loss from caliper crush

> Data card generated from `data/library/formulas/crushed-bct-ratio.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **derived**. Do not edit; change the record instead.

## Values

```
BCT_c / BCT_o = sqrt(h_c / h_o)
```

| symbol | meaning | SI | US |
|---|---|---|---|
| h_o, h_c | caliper before/after crushing | mm | in |

**Valid for:** ECT held constant.

**Limitations:** Crushing also lowers bending stiffness, so real loss can be larger.

**Calculator:** `packcalc.compression.crushed_bct_ratio` (tested against the corpus worked examples). Always compute with the calculator rather than by hand.

## Sources

- `kb.performance.board-tests-and-ect`
