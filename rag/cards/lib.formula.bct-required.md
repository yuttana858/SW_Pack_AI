---
id: card.lib.formula.bct-required
record_id: lib.formula.bct-required
record_type: formula
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: derived
source_refs:
- kb.performance.stacking-load-calc
- kb.performance.environmental-factors
generated_from: data/library/formulas/bct-required.yaml
---

# Required BCT with factors

> Data card generated from `data/library/formulas/bct-required.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **derived**. Do not edit; change the record instead.

## Values

```
BCT_req = F_top / Π m_i   or   F_top × SF
```

| symbol | meaning | SI | US |
|---|---|---|---|
| F_top | static top load | N | lbf |
| m_i | environmental multipliers | - | - |
| SF | safety factor | - | - |

**Valid for:** Multipliers from lib.factors.*; use multipliers or a safety factor, not both.

**Limitations:** Multiplier values vary by source; see factor-set notes.

**Calculator:** `packcalc.stacking.bct_required` (tested against the corpus worked examples). Always compute with the calculator rather than by hand.

## Sources

- `kb.performance.stacking-load-calc`
- `kb.performance.environmental-factors`
