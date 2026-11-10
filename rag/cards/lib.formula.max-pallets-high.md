---
id: card.lib.formula.max-pallets-high
record_id: lib.formula.max-pallets-high
record_type: formula
record_version: 0.1.0
tier: L1
scope: global
status: draft
confidence: derived
source_refs:
- kb.performance.stacking-load-calc
generated_from: data/library/formulas/max-pallets-high.yaml
---

# Maximum pallets high

> Data card generated from `data/library/formulas/max-pallets-high.yaml` v0.1.0. Tier L1, applies to all plants. Status **draft**, confidence **derived**. Do not edit; change the record instead.

## Values

```
P_max = floor((BCT·Πm − (L−1)·m·g) / ((L·k·m + m_p)·g/k)) + 1
```

| symbol | meaning | SI | US |
|---|---|---|---|
| BCT | box compression strength | N | lbf |

**Valid for:** As pallet load.

**Limitations:** 0 means a single pallet already overloads the bottom box.

**Calculator:** `packcalc.stacking.max_pallets_high` (tested against the corpus worked examples). Always compute with the calculator rather than by hand.

## Sources

- `kb.performance.stacking-load-calc`
