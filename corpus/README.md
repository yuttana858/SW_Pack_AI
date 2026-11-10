# SW Pack AI — Packaging Knowledge Corpus

The source documents for the RAG system described in `docs/PLAN.md`. Every file is
Markdown with YAML front-matter, written so the ingestion pipeline can split it at
`##` / `###` headings into self-contained chunks.

## Layout

| Folder | Content |
|---|---|
| `terminology/` | Glossary, abbreviations, synonyms (US / EU / Asia terms) |
| `styles/` | FEFCO (corrugated) and ECMA (folding carton) style codes |
| `materials/` | Paper grades, flutes, combined board grades, paperboard, material record schema |
| `performance/` | ECT, burst, BCT (McKee etc.), environmental factors, stacking calculations |
| `dimensional/` | Inside/outside/manufacturing dimensions, allowances, blank formulas, tolerances |
| `manufacturing/` | Corrugator, converting, die-cutting and tooling |
| `testing/` | ISTA / ASTM / ISO / TAPPI test methods, conditioning |
| `cushioning/` | Fragility, cushion curves, cushion design |
| `logistics/` | Pallets, unit loads, cube utilisation |
| `printing/` | Print processes and their effect on board performance |
| `sustainability/` | Recyclability, regulations (PPWR, EPR), certifications |
| `reference/` | Unit conversions, standards index |
| `agent/` | Rules the assistant must follow when answering or driving CAD tools |
| `company/` | **Your own data** — supplier-certified board records, house tolerances, customer specs (overrides everything else) |

## Front-matter schema

```yaml
---
id: kb.<folder>.<slug>          # stable, unique
title: <human title>
domain: <folder name>
tags: [fefco, rsc, ect, ...]
applies_to: [corrugated | folding-carton | rigid | flexible | cushioning | pallet]
confidence: reference | industry-typical | derived | supplier-certified
status: draft | reviewed | approved
last_reviewed: YYYY-MM-DD
reviewer: <name or "unreviewed">
supersedes: []                  # ids this file replaces
sources:
  - id: S1
    title: <title>
    publisher: <org>
    url: <url>
    accessed: YYYY-MM-DD
---
```

## Confidence levels (retrieval ranks higher levels first)

1. **supplier-certified**: measured or certified by your supplier or lab. Only files in `company/`.
2. **reference**: taken from a published standard or authoritative textbook, and cited.
3. **industry-typical**: common published values that vary by mill or converter. Replace these with your own data.
4. **derived**: worked out from the formulas in this corpus.

## Content rules

- Every number cites a source tag `[S1]`. If sources disagree, the file shows each value and marks the disagreement **VERIFY**.
- Formulas give: the equation, each variable with its units, the range where it is valid, a worked example in SI and US units, and its limits.
- Canonical units are mm, N, kN/m, g/m², kPa, kg, °C and %RH, with US units in brackets.
- Standards text is summarised and cited, never copied word for word (copyright). The assistant points engineers to the standard for anything normative.
- Any value marked industry-typical carries the note *"replace with supplier/house data in `company/`"*.
