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
    title: Box compression analysis of world-wide data spanning 46 years (Urbanik & Frank, Wood and Fiber Science 38(3):399–416, 2006; full PDF read in wave 3)
    publisher: USDA Forest Service / Forest Products Laboratory (Treesearch)
    url: https://research.fs.usda.gov/download/treesearch/25180.pdf
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
  - id: S10
    title: Edge crush test
    publisher: Wikipedia
    url: https://en.wikipedia.org/wiki/Edge_crush_test
    accessed: 2026-11-09
  - id: S11
    title: World standards - comparison of testing methods FEFCO / EN / ISO / TAPPI (revision October 2018)
    publisher: FEFCO Standards Committee
    url: https://www.fefco.org/download/file/fid/2395
    accessed: 2026-11-09
  - id: S12
    title: Effects of Moisture Content on Box Compression Strength - FBA BCT Loss Factors (R. Popil, 2018, updated 2019)
    publisher: Georgia Tech Renewable Bioproducts Institute
    url: https://research.gatech.edu/sites/default/files/2021-06/effects-of-moisture-content-on-box-compression-strength.pdf
    accessed: 2026-11-09
  - id: S13
    title: "Basic design data for the use of fiberboard in shipping containers; box strength calculator (FPL Report 1911-A; Kellicutt, Landt, Setterholm), repository record (PDF not opened: TLS failure in this session)"
    publisher: Oregon State University ScholarsArchive (USDA Forest Products Laboratory report)
    url: https://ir.library.oregonstate.edu/concern/file_sets/2r36v282x
    accessed: 2026-11-09
---

# Box Compression Strength (BCT) Prediction

> **Source access note (2026-11-09, wave 1 update):** Popil's slides [S1] and his RBI papers
> [S6][S12] were downloaded and read in full. They confirm the McKee constants, the units and the
> Z/7 limit. The Urbanik & Frank paper [S2] was read in full in wave 3 (research.fs.usda.gov).
> The TOPS note [S3] and the MDPI papers [S5][S7][S8] were still only seen through search
> extracts: the hosts were blocked or the FPL server was down.

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

- Constant 5.87 and the form are given in [S1][S3][S4][S12]. Wikipedia quotes 5.876 [S10]. Z = 2·(L+W) [S4][S12].
- **Units — resolved (2026-11-09):** Popil states the equation in US customary units: BCT in lb,
  ECT in lb/in, Z and caliper in inches [S1][S12]. That is the "customary-unit fit" wording. The
  equation is still dimensionally homogeneous: ECT is force per length and sqrt(h·Z) is a length,
  so 5.87 has no units. It works unchanged with N/mm and mm (giving N), and [S4] uses it that way
  (derived). The worked example below gives the same answer in both unit systems.
- Popil derives the simplified form from the full form. He approximates bending stiffness as
  proportional to ECT·h² and takes the exponent b ≈ 3/4 [S1]. The simplified form therefore loses
  accuracy when board is crushed: crushed board recovers its caliper but not its bending stiffness
  [S1].
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
  (**VERIFY** with tests). Popil reports one heavy single-wall cold-storage set (12 % moisture,
  4 °C / 80 %RH) that followed McKee within experimental agreement. He says multi-wall boards need
  their own experimental confirmation [S12].

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
- Not a substitute for a BCT test (e.g. TAPPI T 804 / ISO 12048) on real boxes. Test method
  matters. TAPPI T 804 fixes the flaps of empty boxes, and FEFCO TM 50 tests the box simply erected.
  FEFCO reports T 804 results roughly 5 % lower. Test speeds also differ between the methods [S11].

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
- **Resolved (2026-11-09):** C = 1.87028 and b = 0.791213 are **not** an alternative published
  McKee constant. They are the result of Popil's worked spreadsheet example, which re-fits C and b
  (starting from 2.028 and 0.75) to one example set of boxes [S1]. Popil recommends fitting C and b to
  your own boxes. McKee's constants are empirical functions of panel rigidity and size, and McKee
  assumed a square footprint [S1].

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

Kellicutt and Landt proposed one of the first BCT predictors. It uses the ring crush (RCT) of the
component papers and a flute constant, together with the box perimeter and a box constant. The
panel is idealised with equal sides, so that panel width b = Z/4 [S5].

What the primary literature confirms (wave 3, read in full in [S2]):
- **Citation and date.** Urbanik & Frank cite it as Kellicutt, K. Q. and Landt, E. F. (1951),
  "Basic design data for use of fiberboard in shipping containers", *Fibre Containers* 36(12):62–80
  [S2]. The Forest Products Laboratory (FPL) report version with the box strength calculator is FPL
  Report 1911 / R1911-A (Kellicutt, Landt and Setterholm). Library catalogues date it 1951, 1952
  and 1958 (reprints) [S13].
- **Basis.** The paper summarised FPL box work from before World War II as correlations between
  material compression strength and panel buckling strength [S2].
- **Flute factors.** Kellicutt and Landt used empirical flute-adjustment factors [S2].
- **Later revision.** A "new Kellicutt equation" was published by Kawabata (1997), *J. Korea
  TAPPI* 29(4):73–85 [S2].

**VERIFY: the equation and its constants (including the often-quoted 2/3 exponent) are still not
confirmed.** The FPL R1911-A PDF is in the Oregon State repository [S13], but this session could not
open it (TLS chain to a root CA missing from the session's trust store). This file gives no worked
example until a reviewer copies the equation from R1911-A. Use McKee or the Urbanik–Frank refit
below for design estimates.

## Urbanik–Frank (2006) model and refit of McKee to world-wide data

Urbanik & Frank went back to the panel-buckling theory behind McKee. They wrote a general
post-buckling formula and fitted it to 19 data sources from 1943 to 2004. That covers 409
single-wall (SW) RSC boxes plus double-wall (DW) boxes and tubes [S2].

**General model (description only).** Each side panel and end panel is treated as a plate. Its
strength ratio P_f/P_y (panel load over crush load, with P_y = edge crush P_m) depends on the panel's
critical buckling load P_cr. The fitted prefactor is α, the exponent β, and γ is an empirical
correction for panel aspect ratio. Box strength is P = 2·(P_fl·l + P_fw·w), with the load shared
iteratively between panels [S2]. Each of four McKee constraints can be removed:
- square box (S) or rectangular box (R);
- infinitely deep box (I) or finite depth (F);
- elastic buckling only (E) or elastic plus inelastic buckling (EI, when slenderness U = √(P_y/P_cr) ≤ 1);
- with or without γ.

Inelastic buckling (the panel crushes evenly along the loading edge without bulging) is typical
of short or narrow panels and thick board. Elastic buckling (the panel bulges and crushing starts
at the corners) is typical of large panels [S2]. The full model needs an iterative spreadsheet
solution. Use the equations in [S2] directly; they are not reproduced here.

**Closed form: the S I E refit (the McKee form with world-wide constants).** With all of McKee's
constraints applied (S, I, E, γ = 0, and default twisting inputs ĉ = 1, ν = 0), the model reduces
exactly to the McKee equation, with α = a·(64π²)^(b−1) and β = 1 − b [S2]. Fitted to all SW data:
α = 0.376 and β = 0.273 [S2]. That gives:

```
BCT = a · ECT^b · (sqrt(Dx · Dy))^(1−b) · Z^(2b−1)
a = α · (64π²)^β = 0.376 × 631.655^0.273 = 2.186      (derived)
b = 1 − β = 0.727                                    (derived)
```

| Symbol | Meaning | SI unit | US unit |
|---|---|---|---|
| BCT | predicted top-to-bottom compression strength | N | lbf |
| ECT | edge crush strength of the combined board (P_m) | N/m | lbf/in |
| Dx, Dy | MD and CD flexural stiffness per unit width | N·m | lbf·in |
| Z | box perimeter 2·(L + W) | m | in |
| a, b | dimensionless constants (force exponent b + (1 − b) = 1; length exponent −b + (1 − b) + (2b − 1) = 0) | – | – |

Check (derived): McKee's own constants a = 2.028, b = 0.746 transform to α = 0.394, β = 0.254.

Validity: single-wall RSCs within the range of the world-wide data set. The fit covers several ECT
methods (TAPPI T 811 waxed and T 839 clamped) and several labs [S2]. The constraints are the same as
for McKee: square, tall boxes buckling elastically. Not validated for double wall or tubes, where
the fitted prefactor differs a lot [S2].

Worked example (derived; same box as the full-McKee example above: 400 × 300 mm, Z = 1400 mm =
55.12 in, ECT 32 lbf/in, illustrative Dx = 60 lbf·in and Dy = 30 lbf·in):
- US: sqrt(60 × 30) = 42.43 lbf·in. BCT = 2.186 × 32^0.727 × 42.43^0.273 × 55.12^0.454 =
  **466.5 lbf**.
- SI: ECT = 5604 N/m, sqrt(Dx·Dy) = 4.794 N·m, Z = 1.400 m. BCT = 2.186 × 5604^0.727 ×
  4.794^0.273 × 1.400^0.454 = **2075 N** (= 466.5 lbf).
- Full McKee for the same inputs gives 501 lbf (2230 N), so the refit is 6.9 % lower. That matches
  the mean McKee bias in [S2].

**Accuracy, as reported in [S2] (Table 4 there):**

| Model and data | Average absolute error | Mean error (bias) | Standard deviation |
|---|---|---|---|
| Inter-laboratory round robin (Miles 1966), the floor for any model | – | 0 | 7.74 % |
| McKee constants, McKee's own data | 6.09 % | +0.29 % | 7.75 % |
| McKee constants, all SW data | 11.1 % | **+7.64 %** (over-prediction) | 11.9 % |
| S I E refit, all SW data | 8.99 % | +0.62 % | 11.1 % |
| R F EI γ (all constraints removed; α = 0.391, β = 0.312, γ = 0.359), SW data with l, w, d | 8.48 % | +0.56 % | 10.6 % |

Example from [S2]: for a box whose true strength is 1000 lb (454 kg), McKee averages 1076 lb and
can be up to about 19 % high at 1 sigma. The R F EI γ model averages 1006 lb.

Limitations:
- Linear material law only.
- Score-line effects are not modelled. Urbanik & Frank found that the prefactor α is consistently
  lower for boxes than for tubes, and interpret this as strength lost at the flap score [S2].
- DW fits vary widely: some DW data sets beat the McKee estimate, others fall short [S2].
- Even a perfect model cannot beat the about 7.7 % inter-laboratory scatter [S2]. Confirm by test.

## Maltenfort, Allerby, Batelka and FEA approaches

- **Maltenfort** relates board ECT to component ring crush (see
  `kb.performance.board-tests-and-ect`). Popil recommends using the Maltenfort ECT as the McKee
  input, checked against measured ECT [S1].
- **Other re-fits of the McKee constants (confirmed in [S2]).** Published exponents b vary:
  0.746 (McKee 1963), 0.75 (Wolf 1972), 0.724 (Shick & Chari 1965, DW boxes) and 0.778
  (Buchanan et al. 1964). Buchanan et al. and Shick & Chari found the McKee form also fits DW
  boxes [S2]. On SW boxes with more than 20 samples, a best-fit prefactor a ranges from 0.4 to 4.0
  once b is also free. The constants trade off against each other, so a lone "a" has no physical
  meaning [S2].
- **Geometry terms: Wolf (1972), Batelka & Smith (1993), Challas et al. (1994).** Each adds
  box-geometry terms to the McKee form, but the approaches do not agree with each other [S2].
  Sources, from the reference list of [S2]:
  - Wolf, M. (1972), *Package Engineering*, March, 66–67.
  - Batelka, J. J. and Smith, C. N. (1993), *Package compression model*, IPST Project 3746 final
    report.
  - Challas, J., Schaepe, M. and Smith, C. N. (1994), *Predicting package compression strength:
    geometry effect*, IPST Project 3806 final report.

  In the Urbanik & Frank data set the Batelka data are 108 SW **tube** samples, not boxes [S2].
  **VERIFY: the Batelka & Smith equation itself is in an unpublished IPST report; not retrieved.**
- **Allerby et al. (1985) and "Allerheiligen".** Review papers (seen only as search extracts,
  hosts blocked) credit Allerby et al. (1985) with modifying McKee's constants and exponents for
  C-flute board. No author "Allerheiligen" appears in the reference list of [S2] or in any source
  found in waves 1–3. Treat "Allerheiligen" as a **mis-citation of Allerby** and do not cite it.
  **VERIFY: Allerby et al. (1985) constants not retrieved.**
- **Buckling-based and FEA models.** Recent work combines the critical buckling load of each panel
  with post-buckling and numerical (FEM) models. This covers boxes with sidewall cut-outs [S5][S8]
  and pallet overhang [S7]. These models handle geometry that McKee cannot: cut-outs, overhang and
  panel aspect ratio. The Urbanik & Frank R/F/EI model above is the analytical version of the same
  idea [S2].
- **Whitsitt / Maltenfort ECT input:** see `kb.performance.board-tests-and-ect`. Popil's version
  is ECT ≈ 0.7·(2·SCT_liner + α·SCT_medium), with α ≈ 1.42–1.43 for C flute [S1][S12].

## When McKee breaks down (geometry limits)

- **Short boxes:** below D ≈ Z/7 panels do not buckle before crushing, violating the McKee
  assumption [S1]. For that case Popil gives the crush-limited form BCT ≈ C′·ECT·Z, which has no
  caliper or stiffness term [S1]. C′ is not given. The size and direction of McKee's error for short
  boxes are not quantified in [S1] — **VERIFY** with tests.
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

## Research log

**Wave 1 (2026-11-09).** Searches were shared across five files (12 in total).

Resolved this wave:
- Units of 5.87: the source states US customary units, and the equation is dimensionally
  homogeneous [S1][S12].
- Popil's C = 1.87 / b = 0.79 is a spreadsheet re-fit example, not a published constant [S1].
- Short-box alternative form BCT ≈ C′·ECT·Z [S1]. Differences between the T 804 and FEFCO 50 BCT
  test methods [S11].

Still open, with the best lead for each:
- Kellicutt equation and constants. Lead: FPL Report R1911-A, PDF at
  https://ir.library.oregonstate.edu/concern/file_sets/2r36v282x (blocked); Urbanik & Frank (2006)
  at https://wfs.swst.org/index.php/wfs/article/download/437/437 or
  https://research.fs.usda.gov/download/treesearch/25180.pdf (both blocked; www.fpl.fs.usda.gov
  returned HTTP 502 all session).
- Urbanik & Frank general formula: resolved in wave 3 (see the Urbanik–Frank section).
- Allerby et al. (1985) and Batelka & Smith (1993). Lead: MDPI Materials 13(20):4578 literature
  review, https://www.mdpi.com/1996-1944/13/20/4578 (blocked). Also check whether "Allerheiligen"
  is a mis-citation of Allerby.
- Direction of McKee's error for short boxes (D < Z/7), and validity for double wall: needs tests or
  Urbanik & Frank (2006).


**Wave 3 (2026-11-09).** This agent used 21 searches in total, shared across six files. Scope: the
Kellicutt, Urbanik–Frank and newer-model sections only.

Resolved this wave:
- Urbanik & Frank (2006) was read in full from the FPL Treesearch PDF [S2]. Added:
  - the model structure (S/R, I/F, E/EI, γ);
  - the exact reduction to McKee (α = a·(64π²)^(b−1), β = 1 − b);
  - the all-SW S I E refit (a = 2.186, b = 0.727, derived) with SI and US worked examples, checked
    in Python;
  - the accuracy table: McKee bias +7.64 % and average error 11.1 % on 409 SW boxes; R F EI γ
    average error 8.48 %;
  - the McKee-exponent spread (0.724–0.778) and the score-line interpretation of α.
- Batelka & Smith (1993), Wolf (1972) and Challas et al. (1994) confirmed as geometry-term models,
  with full citations from [S2]. Batelka data are SW tubes.
- "Allerheiligen" is not in any source found. Treated as a mis-citation of Allerby et al. (1985).
- Kellicutt & Landt confirmed as 1951, *Fibre Containers* 36(12):62–80, using empirical flute
  factors [S2]. Kawabata (1997) "new Kellicutt equation" lead.

Still open:
- Kellicutt equation and constants. FPL R1911-A on ir.library.oregonstate.edu fails TLS in this
  session: the server chains to the emSign Root CA - G1, which is not in the session trust store.
  www.fpl.fs.usda.gov returns 502. core.ac.uk, d.lib.msu.edu and wfs.swst.org are blocked, and so
  are the Japanese sources (gitec, Kobe) found by a Japanese-language search.
- Allerby et al. (1985) and the Batelka & Smith equations. Lead: MDPI Materials 13(20):4578.
  mdpi.com returns 403; the sparrow.up.poznan.pl, PMC and blob mirrors are blocked.
- Outside this agent's sections, for the file owner:
  - For the "Validity range" (double wall) and "When McKee breaks down" (short boxes) open markers
    markers, [S2] now gives evidence. DW prefactors vary widely, with some DW sets above McKee and
    others below.
  - Inelastic buckling (low l, low w or thick board) is modelled by u = 0 in [S2].
  - The source-access note at the top still says [S2] was seen only in extracts. That is out of
    date.
