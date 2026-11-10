---
id: kb.materials.material-record-schema
title: Board material record schema (template for supplier-certified data)
domain: materials
tags: [schema, material-record, template, supplier-data, auto3d, packaging.materials.update, caliper, ect, take-up, allowance-factors, validation]
applies_to: [corrugated, folding-carton]
confidence: derived
status: draft
last_reviewed: 2026-11-09
reviewer: unreviewed
supersedes: []
sources:
  - id: S1
    title: Corrugated board production (take-up factor ranges, glue per glue line)
    publisher: FEFCO
    url: https://www.fefco.org/lca/dscription-of-production-system/corrugated-board-production
    accessed: 2026-11-09
  - id: S2
    title: Flutes and flute sizes (DIN 55468 flute pitch and height)
    publisher: GDV Transport Information Service
    url: https://tis-gdv.de/?p=199
    accessed: 2026-11-09
  - id: S3
    title: Technical data sheet - Flute S (semichemical fluting; grammage and caliper)
    publisher: Billerud
    url: https://www.billerud.com/globalassets/billerud/packaging-materials/tds/technical-data-sheet---flute-s-2025-01.pdf
    accessed: 2026-11-09
  - id: S4
    title: Conversion chart for edge crush testing
    publisher: Industrial Physics
    url: https://industrialphysics.com/knowledgebase/articles/conversion-chart-for-edge-crush-testing/
    accessed: 2026-11-09
  - id: S5
    title: Testliner quality specifications (moisture window 6.5-9 %)
    publisher: Papierfabrik Palm
    url: https://www.palm.de/fileadmin/Papier/Wellpappenrohpapiere/TL1_EN.pdf
    accessed: 2026-11-09
---

# Board material record schema

This file defines the record an engineer fills in for **each board grade from each supplier**. Filled records live in `company/materials/<supplier>-<grade-id>.yaml` and carry `confidence: supplier-certified`. They override every value in `materials/`, `performance/` and `dimensional/`. The empty template is `company/materials/_template.yaml`.

The `auto3d` block maps 1:1 to the fields accepted by the Auto3D command `packaging.materials.update`, so an agent can push a record into CAD without renaming anything.

## Record structure (YAML)

```yaml
record:            # identity and traceability
material:          # paper build-up and physical properties
performance:       # certified board test results
auto3d:            # exactly the packaging.materials.update fields
```

## Field definitions: record (identity and traceability)

| Field | Type | Required | Meaning |
|---|---|---|---|
| record.id | string | yes | Unique id, `<supplier-slug>-<grade-id>-<rev>` |
| record.supplier | string | yes | Supplier / corrugator / mill legal name |
| record.supplierGradeId | string | yes | Supplier's own grade code as printed on the certificate |
| record.plant | string | no | Producing plant (properties differ by plant/corrugator) |
| record.boardType | enum | yes | `single-wall` / `double-wall` / `triple-wall` / `single-face` / `solid-board` / `folding-carton` |
| record.gradeCode | string | yes | Build-up notation, e.g. `125K/C/125T` (see `materials/paper-grades.md`) |
| record.carrierGrade | string | no | e.g. `32ECT` or `200#` if certified to NMFC Item 222 / UFC Rule 41 |
| record.certificateRef | string | yes if calibrated | Certificate / lab report number |
| record.certificateDate | date | yes if calibrated | YYYY-MM-DD |
| record.validUntil | date | no | Re-certification due date |
| record.confidence | enum | yes | `supplier-certified` / `house-measured` / `industry-typical` |
| record.approvedBy | string | yes if calibrated | Engineer who accepted the data |
| record.notes | string | no | Free text |

## Field definitions: material (build-up and physical)

| Field | Unit | Meaning |
|---|---|---|
| material.flute | enum | `A`,`B`,`C`,`E`,`F`,`G`,`N`,`K`,`BC`,`EB`,`AC`,`EE`,`AAA`,`ACA`,`none` |
| material.outsideLinerGrade / insideLinerGrade / centreLinerGrade | string | Paper grade, e.g. `kraftliner`, `testliner-2`, `white-top-kraftliner` |
| material.mediumGrade / medium2Grade | string | e.g. `semichemical`, `recycled`, `recycled-HP` |
| material.*Gsm | g/m² | Grammage of each ply (ISO 536) |
| material.takeUpFactor / takeUpFactor2 | – | Plant take-up per flute (FEFCO ranges in [S1]) |
| material.adhesiveGsm | g/m² | Total dry starch, all glue lines |
| material.combinedGsm | g/m² | Measured combined grammage |
| material.caliperMm ± caliperToleranceMm | mm | Nominal combined caliper and ± tolerance (uncrushed, as delivered) |
| material.moistureContentPct | % | Moisture at delivery (ISO 287) |
| material.cobb60Outside / cobb60Inside | g/m² | Cobb 60 s water absorption (ISO 535) |
| material.fluteDirection | text | Plain-language statement, mirrors `auto3d.fluteDirectionDegrees` |

## Field definitions: performance (certified results)

| Field | Unit | Test method |
|---|---|---|
| performance.ectKnPerM | kN/m | ISO 3037 / TAPPI T 839 (record which) |
| performance.ectLbPerIn | lb/in | Same test; 1 lb/in = 0.175 kN/m [S4] |
| performance.burstKpa | kPa | ISO 2759 / TAPPI T 810 |
| performance.fctKpa | kPa | Flat crush, ISO 3035 / TAPPI T 825 |
| performance.bendingStiffness {md, cd} | N·m (corrugated) or mN·m (carton) | State method in `bendingMethod` |
| performance.bctReference {boxStyle, dimsMm, bctN, method, conditioning} | N | Reference box test (ISO 12048 / ASTM D642) for calibrating BCT models |
| performance.conditioning | text | e.g. `ISO 187 23 °C / 50 %RH` |

Standard numbers in this table are given for orientation; check editions in `testing/`.

## Field definitions: auto3d (packaging.materials.update)

Field names are exact; do not rename. Lengths in mm.

| Field | Type | Meaning |
|---|---|---|
| name | string | Display name in CAD, e.g. `ACME 32ECT C 125K/112S/125T` |
| flute | string | Flute code (same enum as material.flute) |
| provenance | string | Where the data came from: `supplier-certified`, `house-measured`, `industry-typical`, `derived` |
| calibrated | boolean | `true` only if all dimensional fields come from a certificate or house measurement |
| insideFactors | number[3] | Allowance factors for inside dimension, order **[L, W, H]** |
| outsideFactors | number[3] | Allowance factors for outside dimension, order **[L, W, H]** |
| outsideLinerGrade | string | Paper grade of outside liner |
| insideLinerGrade | string | Paper grade of inside liner |
| mediumGrade | string | Fluting grade |
| scoreProcess | string | e.g. `rotary-slotter`, `flatbed-die`, `rotary-die`, `crease-matrix` |
| conditioning | string | Conditioning atmosphere of the test data |
| outsideLinerGsm | number | g/m² |
| insideLinerGsm | number | g/m² |
| mediumGsm | number | g/m² |
| fluteDirectionDegrees | number | Flute (corrugator MD-cross) direction in the blank, degrees from the blank X axis: `90` = flutes parallel to box height for a standard RSC |
| caliperMm | number | Nominal combined caliper |
| caliperToleranceMm | number | ± tolerance on caliper |
| outsideLinerMm | number | Thickness of outside liner paper |
| insideLinerMm | number | Thickness of inside liner paper |
| mediumPaperMm | number | Thickness of fluting paper |
| flutePitchMm | number | Flute pitch (DIN 55468 ranges in [S2]) |
| scoreWidthMm | number | Width of score/crease line |
| scoreToleranceMm | number | ± tolerance on score position |
| processToleranceMm | number | ± overall converting tolerance (slotting, die-cut, glue joint) |

**Allowance factor semantics (working convention, to confirm against Auto3D):** factors are multiples of `caliperMm` measured from the **score line**, per axis [L, W, H]: `inside = score − insideFactors ⊙ caliperMm` and `outside = score + outsideFactors ⊙ caliperMm`. This matches the RSC defaults in `dimensional/dimensions-and-allowances.md` (`insideFactors = k_s = [1, 1, 2]`, `outsideFactors = k_o − k_s = [1, 1, 2]`) and the example payload in Auto3D's own `packaging.materials.update` command catalog (`insideFactors: [1, 1, 2]`). Confirm with `packaging.measurements.inspect` (which reports the allowance formulas) on a paired Auto3D window before a record is marked `calibrated: true`. See `dimensional/` for how allowances are derived for each FEFCO style.

## Validation rules

Reject or flag a record when:

1. **Required fields:** any field marked required is empty; `auto3d.name`, `flute`, `caliperMm`, `insideFactors`, `outsideFactors`, `provenance`, `calibrated` must always be present.
2. **Calibration honesty:** `calibrated: true` requires `record.certificateRef`, `record.certificateDate`, `record.approvedBy`, and `provenance` ∈ {`supplier-certified`, `house-measured`}. Records outside `company/` must be `calibrated: false`.
3. **Array shape:** `insideFactors` and `outsideFactors` have exactly 3 finite numbers, ≥ 0, ordered [L, W, H].
4. **Positive values:** all `*Gsm`, `*Mm` (except tolerances, which may be 0) > 0.
5. **Tolerance sanity:** `caliperToleranceMm` < 0.25 × `caliperMm`; `scoreToleranceMm`, `processToleranceMm` ≥ 0.
6. **Caliper vs plies:** `caliperMm` > `outsideLinerMm` + `insideLinerMm` + `mediumPaperMm` (flute height must be positive).
7. **Take-up range:** `takeUpFactor` between 1.10 and 1.60; warn if outside the FEFCO range for the stated flute (A 1.50–1.55, C 1.40–1.45, B 1.30–1.35, E 1.20–1.35, F/G/N 1.15–1.25 [S1]).
8. **Flute pitch range:** warn if `flutePitchMm` is outside DIN 55468 ranges for A (8.0–9.5), C (6.8–8.0), B (5.5–6.5) [S2].
9. **Combined grammage check:** warn if |`combinedGsm` − (Σliners + Σ medium × take-up + adhesive)| > 5 % (formula in `materials/flutes.md`).
10. **Moisture:** warn if `moistureContentPct` outside 5–12 % (mill windows such as 6.5–9 % [S5]; wider bound is a house sanity limit).
11. **Units:** ECT given in both kN/m and lb/in must agree within 2 % (1 lb/in = 0.175 kN/m [S4]).
12. **Flute direction:** `fluteDirectionDegrees` ∈ [0, 180); flag values other than 0 or 90 for review.
13. **Folding carton:** when `boardType: folding-carton`, set `flute: none`, medium fields empty, and use `material.caliperMm` for the board thickness.

## Example record (EXAMPLE / NOT CERTIFIED)

> **EXAMPLE — NOT CERTIFIED. Values are illustrative placeholders to show the format. Do not use for design.** Only the flute geometry ranges, the take-up value and the medium caliper are taken from published sources ([S1][S2][S3]); every other number is invented for illustration.

```yaml
# EXAMPLE / NOT CERTIFIED — illustrative only
record:
  id: example-supplier-c32-125k112s125t-r0
  supplier: "EXAMPLE SUPPLIER (not a real company)"
  supplierGradeId: "EX-C-32"
  plant: "Example plant"
  boardType: single-wall
  gradeCode: "125K/C/125T"
  carrierGrade: "32ECT"
  certificateRef: null            # none: not certified
  certificateDate: null
  validUntil: null
  confidence: industry-typical
  approvedBy: null
  notes: "EXAMPLE / NOT CERTIFIED. Replace every value with certificate data."
material:
  flute: C
  outsideLinerGrade: kraftliner
  insideLinerGrade: testliner-2
  centreLinerGrade: null
  mediumGrade: semichemical
  medium2Grade: null
  outsideLinerGsm: 125
  insideLinerGsm: 125
  centreLinerGsm: null
  mediumGsm: 112
  medium2Gsm: null
  takeUpFactor: 1.43              # FEFCO typical C-flute [S1]
  takeUpFactor2: null
  adhesiveGsm: 10                 # illustrative (2 glue lines)
  combinedGsm: 420                # = 125 + 125 + 112*1.43 + 10
  caliperMm: 3.9                  # illustrative
  caliperToleranceMm: 0.15        # illustrative
  moistureContentPct: 8.0         # illustrative
  cobb60Outside: 30               # illustrative
  cobb60Inside: 35                # illustrative
  fluteDirection: "Flutes vertical (parallel to box height) for RSC"
performance:
  ectKnPerM: 5.6                  # illustrative (= 32 lb/in x 0.175)
  ectLbPerIn: 32
  ectMethod: "ISO 3037"
  burstKpa: null
  fctKpa: null
  bendingStiffness: { md: null, cd: null }
  bendingMethod: null
  bctReference:
    boxStyle: "FEFCO 0201"
    dimsMm: [400, 300, 300]
    bctN: null
    method: "ISO 12048"
    conditioning: "ISO 187 23 °C / 50 %RH"
  conditioning: "ISO 187 23 °C / 50 %RH"
auto3d:                           # packaging.materials.update payload
  name: "EXAMPLE 32ECT C 125K/112S/125T (NOT CERTIFIED)"
  flute: C
  provenance: industry-typical
  calibrated: false
  insideFactors: [1.0, 1.0, 2.0]  # score→inside, RSC default; illustrative
  outsideFactors: [1.0, 1.0, 2.0] # score→outside, RSC default; illustrative
  outsideLinerGrade: kraftliner
  insideLinerGrade: testliner-2
  mediumGrade: semichemical
  scoreProcess: rotary-slotter
  conditioning: "ISO 187 23 °C / 50 %RH"
  outsideLinerGsm: 125
  insideLinerGsm: 125
  mediumGsm: 112
  fluteDirectionDegrees: 90
  caliperMm: 3.9
  caliperToleranceMm: 0.15
  outsideLinerMm: 0.18            # illustrative
  insideLinerMm: 0.19             # illustrative
  mediumPaperMm: 0.19             # Flute S 112 g/m2 caliper 190 um [S3]
  flutePitchMm: 7.4               # within DIN 55468 C range 6.8-8.0 [S2]
  scoreWidthMm: 3.0               # illustrative
  scoreToleranceMm: 1.0           # illustrative
  processToleranceMm: 1.5         # illustrative
```

Validation of the example: rule 6 → 0.18 + 0.19 + 0.19 = 0.56 mm < 3.9 mm ✓; rule 7 → 1.43 within C range ✓; rule 9 → 125 + 125 + 160.2 + 10 = 420.2 vs 420 ✓; rule 2 → `calibrated: false` because no certificate ✓.
