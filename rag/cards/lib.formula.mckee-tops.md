---
id: card.lib.formula.mckee-tops
record_id: lib.formula.mckee-tops
record_type: formula
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: reference
source_refs:
- kb.performance.box-compression#S3
generated_from: data/library/formulas/mckee-tops.yaml
---

# McKee TOPS variant

> Data card generated from `data/library/formulas/mckee-tops.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **reference**. Do not edit; change the record instead.

## Values

```
BCT = 5.87 · ECT · Z^0.4924 · h^0.5076
```

| symbol | meaning | SI | US |
|---|---|---|---|
| BCT | box compression strength | N | lbf |
| ECT | edge crush | N/mm | lbf/in |
| h | caliper | mm | in |
| Z | perimeter | mm | in |

**Valid for:** As simplified McKee.

**Limitations:** About 4 % below the rounded form for the reference box.

**Calculator:** `packcalc.compression.mckee_tops` (tested against the corpus worked examples). Always compute with the calculator rather than by hand.

## Sources

- `kb.performance.box-compression#S3`
