---
id: kb.performance.board-tests-and-ect
title: Corrugated Board Tests — ECT Methods, ECT Estimation, Burst, FCT, PAT, Bending Stiffness, Caliper
domain: performance
tags: [ect, edge-crush, tappi-t811, tappi-t839, tappi-t838, iso-3037, fefco, rct, sct, maltenfort, burst, mullen, fct, pat, bending-stiffness, caliper, unit-conversion]
applies_to: [corrugated]
confidence: reference
status: draft
last_reviewed: 2026-11-09
reviewer: unreviewed
supersedes: []
sources:
  - id: S1
    title: Finite Element-Based Simulation for Edgewise Compression Behavior of Corrugated Paperboard for Packaging of Agricultural Products
    publisher: MDPI Applied Sciences 10(19):6716
    url: https://www.mdpi.com/2076-3417/10/19/6716
    accessed: 2026-11-09
  - id: S2
    title: Which ECT?
    publisher: ResearchGate (R. Popil)
    url: https://www.researchgate.net/publication/356634635_Which_ECT
    accessed: 2026-11-09
  - id: S3
    title: An evaluation of ECT sample height for small flute board grades and Box Manufacturer's Certification compliance
    publisher: ResearchGate
    url: https://www.researchgate.net/publication/288270860_An_evaluation_of_ECT_sample_height_for_small_flute_board_grades_and_Box_Manufacturer's_Certification_compliance
    accessed: 2026-11-09
  - id: S4
    title: Relationship between the edgewise compression strength of corrugated board and the compression strength of liner and fluting medium papers
    publisher: ResearchGate
    url: https://www.researchgate.net/publication/254317912_Relationship_between_the_edgewise_compression_strength_of_corrugated_board_and_the_compression_strength_of_liner_and_fluting_medium_papers
    accessed: 2026-11-09
  - id: S5
    title: Predicting Box Compression Strength (slides)
    publisher: Georgia Tech Renewable Bioproducts Institute (R. Popil)
    url: https://research.gatech.edu/sites/default/files/rbi/pdfs/Predicting%20Box%20Compression%20Strength_3.pdf
    accessed: 2026-11-09
  - id: S6
    title: Corrugation Technical Guidelines (RCT, take-up factors)
    publisher: Venkraft
    url: https://www.venkraft.com/Pdf/CorrugationTechnicalGuidlines.pdf
    accessed: 2026-11-09
  - id: S7
    title: Edge Crush Testing (ECT)
    publisher: Mecmesin
    url: https://www.mecmesin.com/test-type/edge-crush-test-ect
    accessed: 2026-11-09
  - id: S8
    title: TAPPI Standards (equipment list)
    publisher: RDM Test Equipment
    url: https://rdmtest.com/tappi/
    accessed: 2026-11-09
  - id: S9
    title: TAPPI T839 Edge Compression Test (ECT) – Clamp Method
    publisher: Purple Diamond
    url: https://purple-diamond.com/testing-standards/tappi-testing-standards/tappi-t839-edge-compression-test-ect-clamp-method/
    accessed: 2026-11-09
  - id: S10
    title: Ring crush and short span compression for predicting edgewise compressive strength
    publisher: ResearchGate
    url: https://www.researchgate.net/publication/293701195_Ring_crush_and_short_span_compression_for_predicting_edgewise_compressive_strength
    accessed: 2026-11-09
  - id: S11
    title: Box compression analysis of world-wide data spanning 46 years (Urbanik & Frank 2006)
    publisher: USDA Forest Service Treesearch
    url: https://research.fs.usda.gov/treesearch/25180
    accessed: 2026-11-09
  - id: S12
    title: Box Compression Strength Calculator (McKee)
    publisher: opscalculators.com
    url: https://opscalculators.com/packaging-engineering/box-compression-calculator/
    accessed: 2026-11-09
---

# Corrugated Board Tests and ECT

> **Source access note (2026-11-09):** sources were consulted through web-search extracts; full
> standards and papers could not be downloaded in the drafting session. Standards text is not
> reproduced; consult the current TAPPI / ISO / FEFCO document for anything normative.
> Several sub-topics below have no retrieved source yet and are marked **VERIFY**.

## Edge crush test (ECT) — what it measures

ECT is the edgewise compressive strength of a short column of combined board, loaded parallel to
the flutes, reported as force per unit width (kN/m [lbf/in]). It is the main input to McKee BCT
prediction (see `kb.performance.box-compression`) and the basis of ECT-grade box certificates
(see `kb.standards.rule41-item222`).

## ECT test methods and why values differ

| Method | Specimen preparation (summary) | Notes |
|---|---|---|
| TAPPI T 811 | Edges reinforced (wax-dipped), rectangular specimen | Reference method for many North American certificates; naming conflicts between sources — see below |
| TAPPI T 838 | Neck-down specimen | — |
| TAPPI T 839 | Unwaxed specimen held in clamps | Clamp method [S9] |
| ISO 3037 | International edgewise crush method | Comparison data not retrieved — **VERIFY** |
| FEFCO No. 8 | European method | Compared with T 838 in [S1] |

Why values differ:
- Clamp (T 839) results read clearly higher than the wax-dip method on some boards, so changing
  the verification method changes reported values [S2].
- Popil's comparison of T 811, T 838 and T 839 on single-wall board found no simple trend with
  medium basis weight: T 839 read much lower than the others for low-weight medium and much higher
  for heavy medium, attributed to clamping pressure and flat-crush resistance [S1].
- An average gap of about 31 % between T 838 and FEFCO No. 8 is reported [S1]. The same extract
  gives the smallest gap between T 838 and T 811 as "about 15 kN/m" — **VERIFY** (this magnitude
  looks implausible for ECT; it may be 15 % or a different unit).
- For lightweight B-flute, T 839 values exceed T 811 values; the data do not support T 811 for E-
  and F-flute [S3].
- **Naming conflict — VERIFY:** one supplier labels T 811 the "short column" method [S7], others
  label T 839 the short-column test [S8][S9]. Check the current TAPPI titles.

Practical rule: always record the ECT method with the value; never compare or certify across
methods without a correlation study.

## ECT estimation from component papers (Maltenfort-type equation)

```
ECT = k · (RCT_L1 + RCT_L2 + α · RCT_M)       # ring crush form
ECT = k' · (SCT_L1 + SCT_L2 + α · SCT_M)      # short-span (SCT) form
```

| Symbol | Meaning | SI unit | US unit |
|---|---|---|---|
| ECT | predicted edge crush of the combined board | kN/m | lbf/in |
| RCT_L1, RCT_L2 | ring crush (or SCT) of each liner, CD, per unit width | kN/m | lbf/in |
| RCT_M | ring crush (or SCT) of the medium, CD, per unit width | kN/m | lbf/in |
| α | take-up factor (length of medium per length of board) | – | – |
| k, k' | empirical fit factor | – | – |

- Form: sum of liner and medium strengths, medium weighted by take-up factor, scaled by a fitted k
  [S4][S10]. Double/triple wall: add every liner and every medium term [S4].
- One board-specific fit gave k = 1.028 (RCT form) and k' = 0.6982 (SCT form) [S4].
- Popil's empirical regressions (US units, additive constant so **not** unit-independent) [S5]:
  - ECT = 0.8 · (RCT1 + RCT2 + α·RCT_M) + 12, for linerboards above 42 lb/msf
  - ECT = 1.27 · (RCT1 + RCT2 + α·RCT_M) − 6, for linerboards below 42 lb/msf
  - **VERIFY** the RCT units these regressions expect (lbf/in vs lbf per 6-in strip) from the
    original slides.
- Take-up factor α: B-flute 1.35, C-flute 1.45 [S6]; C-flute ≈ 1.42 [S5]. Values vary with
  corrugator and flute profile — replace with supplier/house data in `company/`.
- RCT measures only about 50 % of the intrinsic compressive strength of paperboard [S10], which is
  one reason SCT-based forms and different k values exist.

### Validity range

Single- and multi-wall board within the paper grades used to fit k [S4][S5]; Popil warns of ECT
problems at very low or very high basis weights and recommends checking predictions against
measured ECT [S5].

### Worked example

Illustrative inputs (not typical values): each liner RCT = 14 lbf/in (2.452 kN/m); medium
RCT = 7 lbf/in (1.226 kN/m); C-flute α = 1.45 [S6]; k = 1.028 [S4].

SI: ECT = 1.028 × (2.452 + 2.452 + 1.45 × 1.226) = 1.028 × 6.681 = **6.87 kN/m**

US: ECT = 1.028 × (14 + 14 + 1.45 × 7) = 1.028 × 38.15 = **39.2 lbf/in** (= 6.87 kN/m)

Popil "above 42 lb/msf" regression (US only): 0.8 × 38.15 + 12 = **42.5 lbf/in** (7.45 kN/m).
The 8 % gap between the two estimates shows the fit-dependence of k.

### Limitations

Ignores bond quality, flute crush (caliper loss), washboarding and moisture. k is mill/plant
specific — calibrate against your own measured ECT and store the fit in `company/`.

## Burst (Mullen) test

Burst strength is the pressure (kPa [psi]) needed to rupture the board under a diaphragm. It is
dominated by liner tensile strength and stretch rather than by edgewise compression, which is why
burst correlates poorly with stacking strength and why ECT grades exist alongside burst grades
(see `kb.standards.rule41-item222`). **VERIFY — no published burst-vs-liner formula was retrieved
in this session; do not estimate burst from liner data without a sourced relation.**

## Flat crush (FCT) and pin adhesion (PAT)

- **FCT** — compression perpendicular to the board surface; indicates medium strength and flute
  resistance to crushing during converting. Low FCT means caliper loss on the converting line,
  which lowers BCT (see caliper section).
- **PAT** — force to separate liner and medium at the glue lines; indicates bond quality.
- **VERIFY — test-method numbers, specimen details and typical values were not retrieved;** see
  the TAPPI test-method index (T 808 / T 821 commonly cited) in `kb.testing.*` once sourced.

## Bending stiffness (four-point)

Four-point bending gives flexural stiffness per unit width in MD (Dx) and CD (Dy), the inputs to
the full McKee formula (geometric mean sqrt(Dx·Dy)) [S5]. Units: N·m [lbf·in] per unit width.
TAPPI T 820 is the commonly cited four-point method — **VERIFY** method details against the
current TAPPI standard (not retrieved).

## Caliper and caliper loss

Caliper (combined board thickness) is measured with a defined-pressure micrometer (TAPPI T 411 /
ISO 3034 — **VERIFY** current method titles and pressures; not retrieved). Caliper enters McKee
as sqrt(h) (see `kb.performance.box-compression`) [S12].

### Formula — BCT retained after caliper loss (derived from McKee)

```
BCT_crushed / BCT_original = sqrt(h_crushed / h_original)        # ECT held constant
```

| Symbol | Meaning | SI | US |
|---|---|---|---|
| h_original, h_crushed | caliper before / after crushing | mm | in |

Validity: same as simplified McKee; assumes ECT is unchanged.

Worked example: C-flute caliper 4.0 mm (0.1575 in) crushed to 3.6 mm (0.1417 in), i.e. 10 % loss.
- SI: sqrt(3.6 / 4.0) = sqrt(0.90) = 0.949 → ≈ 5.1 % BCT loss
- US: sqrt(0.1417 / 0.1575) = sqrt(0.90) = 0.949 → same
- 20 % caliper loss → sqrt(0.80) = 0.894 → ≈ 10.6 % BCT loss

Limitations: real flute crushing also reduces ECT and bending stiffness (damaged medium), so the
true BCT loss is larger than the sqrt(h) term alone — **VERIFY** with BCT tests; magnitude not
sourced.

## Unit conversions (exact, derived)

Derived from the exact definitions 1 lbf = 4.4482216152605 N and 1 in = 0.0254 m (no external
source consulted; confidence: derived).

| From | To | Multiply by |
|---|---|---|
| ECT lbf/in | kN/m (= N/mm) | 0.175127 |
| ECT kN/m | lbf/in | 5.71015 |
| Burst psi | kPa | 6.894757 |
| Burst kPa | psi | 0.145038 |
| Bending stiffness lbf·in (per in width) | N·m (per m width) | 0.112985 |
| Force lbf | N | 4.448222 |

Examples: 32 ECT = 32 × 0.175127 = 5.60 kN/m; 44 ECT = 7.71 kN/m; 200 psi burst =
200 × 6.894757 = 1379 kPa; 275 psi = 1896 kPa.

Note: grade names "32 ECT" and "200#" are certificate grades in lbf/in and psi — keep the US
grade name alongside the SI value when communicating with US carriers.
