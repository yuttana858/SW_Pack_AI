---
id: card.lib.formula.ect-from-sct
record_id: lib.formula.ect-from-sct
record_type: formula
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: derived
source_refs:
- kb.performance.board-tests-and-ect
generated_from: data/library/formulas/ect-from-sct.yaml
---

# ECT estimate from component SCT

> Data card generated from `data/library/formulas/ect-from-sct.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **derived**. Do not edit; change the record instead.

## Values

```
ECT ≈ C · (Σ SCT_liner + Σ α · SCT_medium),  C ≈ 0.7
```

| symbol | meaning | SI | US |
|---|---|---|---|
| SCT | short-span compression, CD | N/mm | lbf/in |
| α | take-up factor | - | - |

**Valid for:** Grades within the fitted range.

**Limitations:** Empirical; check against measured ECT.

**Calculator:** `packcalc.board.ect_from_sct` (tested against the corpus worked examples). Always compute with the calculator rather than by hand.

## Sources

- `kb.performance.board-tests-and-ect`
