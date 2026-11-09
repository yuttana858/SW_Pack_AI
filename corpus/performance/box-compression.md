---
id: kb.performance.box-compression
title: Box Compression Strength (BCT) Prediction — McKee and Related Models
domain: performance
tags: [bct, box-compression, mckee, ect, caliper, perimeter, bending-stiffness, kellicutt, urbanik, stacking]
applies_to: [corrugated]
confidence: reference
status: draft
last_reviewed: 2026-11-09
reviewer: unreviewed
supersedes: []
sources:
  - id: S1
    title: Predicting Box Compression Strength (slides)
    publisher: Georgia Tech Renewable Bioproducts Institute (R. Popil)
    url: https://research.gatech.edu/sites/default/files/rbi/pdfs/Predicting%20Box%20Compression%20Strength_3.pdf
    accessed: 2026-11-09
  - id: S2
    title: Box compression analysis of world-wide data spanning 46 years (Urbanik & Frank, Wood and Fiber Science 2006)
    publisher: USDA Forest Service / Forest Products Laboratory (Treesearch)
    url: https://research.fs.usda.gov/treesearch/25180
    accessed: 2026-11-09
  - id: S3
    title: TOPS – Stacking Strength (technical note)
    publisher: TOPS Software Corporation
    url: https://topseng.com/Documents/Tech/TOPS/TOPS%20-%20Stacking%20Strength.pdf
    accessed: 2026-11-09
  - id: S4
    title: Box Compression Strength Calculator (McKee Formula, BCT and Safe Stacking)
    publisher: opscalculators.com
    url: https://opscalculators.com/packaging-engineering/box-compression-calculator/
    accessed: 2026-11-09
  - id: S5
    title: The Role of Buckling in the Estimation of Compressive Strength of Corrugated Cardboard Boxes
    publisher: MDPI Materials 13(20):4578
    url: https://www.mdpi.com/1996-1944/13/20/4578
    accessed: 2026-11-09
  - id: S6
    title: Box Compression for Copy Paper Boxes – Applying McKee's Formula
    publisher: Georgia Tech RBI (R. Popil)
    url: https://research.gatech.edu/sites/default/files/rbi/pdfs/The%20Box%20Compression%20for%20Copy%20Paper%20Boxes%20-%20edited%202020.pdf
    accessed: 2026-11-09
  - id: S7
    title: Estimation of the Compressive Strength of Cardboard Boxes Including Packaging Overhanging on the Pallet
    publisher: MDPI Applied Sciences 14(2):819
    url: https://www.mdpi.com/2076-3417/14/2/819
    accessed: 2026-11-09
  - id: S8
    title: Compression Strength Estimation of Corrugated Board Boxes for a Reduction in Sidewall Surface Cutouts
    publisher: MDPI Materials 16(2):597
    url: https://www.mdpi.com/1996-1944/16/2/597
    accessed: 2026-11-09
  - id: S9
    title: Understanding the McKee Formula for Corrugated Box (IPPTA)
    publisher: IPPTA
    url: https://ippta.co/wp-content/uploads/2024/12/114-117.pdf
    accessed: 2026-11-09
---

# Box Compression Strength (BCT) Prediction

> **Source access note (2026-11-09):** the sources above were consulted through web-search
> extracts; the full PDFs could not be downloaded in the drafting session (network restriction).
> Constants below match across several extracts, but a reviewer should check them against the
> original papers before this file moves to `reviewed`.

## What BCT is and why it is predicted

Box compression strength (BCT, also "box compression test" value) is the peak top-to-bottom load
an empty, closed box carries in a platen compression test. Engineers predict it from board
properties during design, then confirm by test. The McKee (1963) equation is the industry
reference for this prediction [S2]. All BCT formulas are averages: individual boxes vary above and
below the predicted value, and they do not account for rough handling, transport, die-cuts,
or adhesives [S3]. The engineer stays responsible for physical testing [S3].

## Simplified McKee formula

```
BCT = 5.87 · ECT · sqrt(h · Z)
Z   = 2 · (L + W)
```

| Symbol | Meaning | SI unit | US unit |
|---|---|---|---|
| BCT | predicted top-load compression strength of the empty box | N | lbf |
| ECT | edge crush (edgewise compression) strength of the combined board | N/mm (= kN/m) | lbf/in |
| h | combined board caliper | mm | in |
| Z | box perimeter, 2·(L + W) | mm | in |
| L, W | box length and width | mm | in |

- Constant 5.87 and the form are given in [S1][S3][S4]. Z = 2·(L+W) [S4].
- **Units handling (derived):** ECT has units of force/length and sqrt(h·Z) has units of length, so
  the equation is dimensionally homogeneous and 5.87 is dimensionless. It can be used unchanged with
  N/mm + mm (gives N) or lbf/in + in (gives lbf). One calculator page [S4] uses exactly
  BCT (N) = 5.87 × ECT (N/mm) × √(mm × mm), while a search extract described 5.87 as a
  "customary-unit fit". **VERIFY** — the dimensional check above (and the worked example below,
  which gives identical answers in both unit systems) shows no unit conversion is hidden in 5.87.
- Do **not** mix kN/m with mm unless you note that 1 kN/m = 1 N/mm.

### TOPS variant with unrounded exponents

TOPS documentation uses the less-rounded form [S3]:

```
BCT = 5.87 · ECT · Z^0.4924 · h^0.5076
```

Exponents sum to 1.0 so it is also dimensionally homogeneous (derived).

### Validity range

- Regular slotted containers (RSC) with top-to-bottom loading, panels failing by buckling
  then crushing at the corners. McKee assumes panel buckling, which requires box depth
  (height) D ≥ Z/7 [S1].
- McKee's ECT sample heights do not define E- and F-flute; newer small flutes are outside the
  original data set [S2].
- Single-wall RSCs in the original data; double-wall use is common practice but less validated
  (**VERIFY** with tests).

### Worked example — simplified McKee

Box 400 × 300 × 300 mm (15.75 × 11.81 × 11.81 in), 32 ECT C-flute board, caliper assumed 4.0 mm
(0.1575 in) — caliper is an illustrative input; use measured caliper.

SI:
- ECT = 32 lbf/in × 0.175127 = 5.604 kN/m = 5.604 N/mm
- Z = 2 × (400 + 300) = 1400 mm
- sqrt(4.0 × 1400) = sqrt(5600) = 74.83 mm
- BCT = 5.87 × 5.604 × 74.83 = **2462 N** (≈ 251 kgf)
- Validity check: D = 300 mm ≥ Z/7 = 200 mm → OK.

US:
- Z = 55.12 in, h = 0.1575 in, sqrt(0.1575 × 55.12) = 2.946 in
- BCT = 5.87 × 32 × 2.946 = **553 lbf** (= 2462 N, consistent with SI)

TOPS exponents: 5.87 × 32 × 55.12^0.4924 × 0.1575^0.5076 = **529 lbf (2355 N)**, about 4 % lower.

### Limitations

- Systematically **over-predicts** compression strength over a broad world-wide data set of
  single-wall boxes [S2]. Treat results as optimistic.
- Ignores box depth, panel aspect ratio, manufacturer's joint, print, cut-outs and handholes [S3][S8].
- Ignores humidity, storage time, stacking pattern and pallet overhang — apply those separately
  (see `kb.performance.environmental-factors`).
- Not a substitute for a BCT test (e.g. TAPPI T 804 / ISO 12048) on real boxes.

## Full McKee formula (with bending stiffness)

```
BCT = 2.028 · ECT^0.746 · (sqrt(Dx · Dy))^0.254 · Z^0.492
```

| Symbol | Meaning | SI unit | US unit |
|---|---|---|---|
| ECT | edge crush strength | N/m | lbf/in |
| Dx, Dy | flexural (bending) stiffness of the combined board per unit width, machine (MD) and cross direction (CD) | N·m (= N·m²/m) | lbf·in (= lbf·in²/in) |
| sqrt(Dx·Dy) | geometric mean bending stiffness | N·m | lbf·in |
| Z | perimeter | m | in |
| BCT | predicted compression strength | N | lbf |

- Constants 2.028, 0.746, 0.254 (on the geometric-mean stiffness) and 0.492 per [S1][S4]. The
  stiffness term is the geometric mean of MD and CD bending stiffness [S1]. IPPTA uses SI inputs
  (ECT kN/m, stiffness N·m, perimeter m) [S9].
- **Units (derived):** force exponents 0.746 + 0.254 = 1.000 and length exponents
  −0.746 + 0.254 + 0.492 = 0.000, so the equation is dimensionally homogeneous: 2.028 is
  dimensionless and applies in any *consistent* set (N/m, N·m, m → N; or lbf/in, lbf·in, in → lbf).
  A numerical conversion check from US to SI returns the same constant (2.028).
- **VERIFY:** one extract of Popil's slides quotes a different fitted constant (C ≈ 1.87,
  b ≈ 0.791) from a different data set [S1]; constants depend on the data set fitted.

### Validity range

As for the simplified form (RSC, D ≥ Z/7 [S1]). Requires measured Dx, Dy (four-point bending,
e.g. TAPPI T 820 — see `kb.performance.board-tests-and-ect`).

### Worked example — full McKee

Same box (Z = 1400 mm = 55.12 in), ECT 32 lbf/in. Bending stiffness **illustrative assumed
inputs** Dx = 60 lbf·in, Dy = 30 lbf·in (replace with measured values).

US:
- sqrt(60 × 30) = 42.43 lbf·in
- BCT = 2.028 × 32^0.746 × 42.43^0.254 × 55.12^0.492 = **501 lbf**

SI:
- ECT = 32 × 175.127 = 5604 N/m; Dx = 60 × 0.112985 = 6.779 N·m; Dy = 3.390 N·m;
  sqrt(Dx·Dy) = 4.794 N·m; Z = 1.400 m
- BCT = 2.028 × 5604^0.746 × 4.794^0.254 × 1.400^0.492 = **2230 N** (= 501 lbf)

### Limitations

Same as the simplified form; additionally needs bending stiffness data that are rarely on a
supplier's spec sheet. Its advantage is that it separates stiffness (which falls with caliper
loss) from ECT.

## Kellicutt (Kellicutt & Landt) formula

Kellicutt and Landt (1952) proposed one of the first BCT predictors, using the paper's ring crush
(RCT) and a flute constant together with the box perimeter and a box constant; the panel is
idealised with equal sides so that panel width b = Z/4 [S5].

**VERIFY — the exact equation and its constants (including the commonly quoted 2/3 exponent)
could not be confirmed in the sources consulted. No worked example is given until a reviewer
adds the equation from the original publication or [S2].** Use McKee for design estimates.

## Maltenfort, Urbanik, Allerheiligen, Batelka and FEA approaches

- **Maltenfort** relates board ECT to component ring crush (see
  `kb.performance.board-tests-and-ect`); Popil recommends using the Maltenfort ECT as the McKee
  input, checked against measured ECT [S1].
- **Urbanik & Frank (2006)** analysed 46 years of world-wide data and proposed a general formula
  that keeps McKee's underlying buckling theory but removes its constraints [S2]; a later study
  reports two of their criteria agree with a large data set [S2]. **VERIFY — formula not retrieved.**
- **Buckling-based / FEA models**: recent work combines critical-buckling load of each panel with
  post-buckling and numerical (FEM) models, including boxes with sidewall cut-outs [S5][S8] and
  pallet overhang [S7]. These handle geometry (cut-outs, overhang, panel aspect ratio) that McKee
  cannot.
- **Allerheiligen, Batelka:** **VERIFY — not retrieved in this drafting session**; do not quote
  until sourced.

## When McKee breaks down (geometry limits)

- **Short boxes:** below D ≈ Z/7 panels do not buckle before crushing, violating the McKee
  assumption [S1]. Prediction becomes unreliable (direction of error not established in the
  consulted sources — **VERIFY**).
- **Tall boxes / slender panels and high L/W ratio:** McKee contains no depth or L/W term, so the
  effect of panel slenderness and unequal panels is not captured [S2][S5]. Buckling-based models
  [S5] address this.
- **Small flutes (E, F):** outside the McKee data set [S2].
- **Over-prediction in general:** [S2] — McKee systematically overestimates for a broad set of
  single-wall boxes.

## Effect of panel dimensions (derived from McKee)

From BCT ∝ sqrt(h·Z):
- Doubling perimeter raises BCT by sqrt(2) = 1.41×, while the load the box must carry (product
  mass) usually rises faster — larger boxes need stronger board per unit of contents (derived).
- BCT ∝ sqrt(h): a thicker flute raises BCT at the same ECT, which is why small, thick boxes are
  stronger than large, thin ones in the same ECT grade [S4].
- Depth does not appear in McKee; real depth effects need test data or [S2][S5].

## Reverse calculation: required ECT from target BCT

```
ECT_required = BCT_required / (5.87 · sqrt(h · Z))
```

Units and validity as for the simplified McKee formula. BCT_required must already include
environmental factors and safety factor (see `kb.performance.stacking-load-calc`).

### Worked example

Target BCT_required = 3000 N (674.4 lbf); h = 4.0 mm (0.1575 in); Z = 1400 mm (55.12 in).

- SI: ECT = 3000 / (5.87 × 74.83) = **6.83 kN/m**
- US: ECT = 674.4 / (5.87 × 2.946) = **39.0 lbf/in** → choose the next grade up, e.g. 40 ECT
  (6.83 / 0.175127 = 39.0 lbf/in, consistent).

Limitations: inherits McKee's over-prediction [S2]; confirm by BCT test.

## Example table — simplified McKee, h = 4.0 mm (0.1575 in) (derived)

| Box L × W (mm) | Z mm (in) | 32 ECT (5.60 kN/m) | 44 ECT (7.71 kN/m) |
|---|---|---|---|
| 300 × 200 | 1000 (39.4) | 2081 N (468 lbf) | 2861 N (643 lbf) |
| 400 × 300 | 1400 (55.1) | 2462 N (553 lbf) | 3385 N (761 lbf) |
| 600 × 400 | 2000 (78.7) | 2942 N (661 lbf) | 4046 N (909 lbf) |

Arithmetic: BCT = 5.87 × ECT(N/mm) × sqrt(4 × Z). These are *uncorrected* lab values; apply
environmental multipliers before use.
