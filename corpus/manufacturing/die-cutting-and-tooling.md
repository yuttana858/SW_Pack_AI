---
id: kb.manufacturing.die-cutting-and-tooling
title: Die cutting and tooling – rules, creasing matrices, nicks, ejection, CAD line types and exchange formats
domain: manufacturing
tags: [die-cutting, flatbed, rotary, steel-rule, cutting-rule, creasing-rule, perforating-rule, rule-height, point-size, creasing-matrix, channel-width, nicks, ejection-rubber, shore-a, make-ready, cf2, cff2, ddes, dxf, ard, score-profile, point-to-point, point-to-flat]
applies_to: [corrugated, folding-carton]
confidence: industry-typical
status: draft
last_reviewed: 2026-11-09
reviewer: unreviewed
supersedes: []
sources:
  - id: S1
    title: Rotary vs flatbed die cutting
    publisher: Plitek
    url: https://www.plitek.com/resources/technical-resources/rotary-vs-flatbed-die-cutting/
    accessed: 2026-11-09
  - id: S2
    title: How to choose the best corrugated box die cut machine (buying guide)
    publisher: Alibaba SmartBuy
    url: https://smartbuy.alibaba.com/buyingguides/corrugated-box-die-cut-machine
    accessed: 2026-11-09
  - id: S3
    title: Rotary die cutting vs flatbed die cutting use
    publisher: CGR Products
    url: https://www.cgrproducts.com/rotary-die-cutting-vs-flatbed-die-cutting-use/
    accessed: 2026-11-09
  - id: S4
    title: Scandie steel rules (2024 product sheet)
    publisher: voestalpine Precision Strip
    url: https://voestalpine.com/precision-strip/files/2024_scandie_steel_rules_engl_2page.pdf
    accessed: 2026-11-09
  - id: S5
    title: Cutting and scoring (matrix scoring with 2 pt .918 rule; packing)
    publisher: NA Graphics
    url: https://nagraph.com/cutting-scoring.html
    accessed: 2026-11-09
  - id: S6
    title: "Cito's die-cutting and creasing lesson III: basics for selecting the cutting die and the creasing matrix"
    publisher: PrintWeek India / CITO
    url: https://www.printweek.in/Features/citosdiecuttingcreasinglessoniiibasicsselectingcuttingdiecreasingmatrix-23185
    accessed: 2026-11-09
  - id: S7
    title: "Cito's die-cutting and creasing lesson IV: tips for corrugated board"
    publisher: PrintWeek India / CITO
    url: https://www.printweek.in/features/citos-die-cutting-creasing-lesson-iv-tips-corrugated-board-23267?amp=1
    accessed: 2026-11-09
  - id: S8
    title: CITO Abacus – creasing matrix calculation aid, corrugated board
    publisher: CITO-System GmbH
    url: https://cito.de/en/AE/boxline/rillzurichtungen/cito-abakus_online/wellpappe
    accessed: 2026-11-09
  - id: S9
    title: CITO Abacus – creasing matrix calculation aid, cartonboard
    publisher: CITO-System GmbH
    url: https://cito.de/en/BR/boxline/rillzurichtungen/cito-abakus_online/karton
    accessed: 2026-11-09
  - id: S10
    title: Die cutting complex shapes in paperboard (Paper Academy)
    publisher: Holmen
    url: https://www.holmen.com/en/board-and-paper/insights/paper-academy/die-cutting-complex-shapes-in-paperboard/
    accessed: 2026-11-09
  - id: S11
    title: CITO FAST Rubber – C-profile for solid and corrugated board
    publisher: CITO-System GmbH
    url: https://cito.de/en/IR/fast-rubber
    accessed: 2026-11-09
  - id: S12
    title: CITO D/5 Peak profile for corrugated board
    publisher: CITO-System GmbH
    url: https://www.cito.de/en/US/ejection-material/flatbed-corrugated-board/cito-d5-peak/
    accessed: 2026-11-09
  - id: S13
    title: CITO manual nick grinder
    publisher: CITO-System GmbH
    url: https://www.cito.de/en/BG/boxline/diecutting/manual_nick_grinder/
    accessed: 2026-11-09
  - id: S14
    title: CFF2 line types (Figure 1)
    publisher: Kodak workflow help
    url: https://workflowhelp.kodak.com/x/cYZaEg
    accessed: 2026-11-09
  - id: S15
    title: ArtiosCAD Module Description (April 2010, US)
    publisher: Esko (copy hosted by grafika.map.sk)
    url: https://grafika.map.sk/wp-content/uploads/2020/05/ArtiosCAD_Module_Description_apr10_us.pdf
    accessed: 2026-11-09
  - id: S16
    title: .CF2 file extension
    publisher: FileInfo
    url: https://fileinfo.com/extension/cf2
    accessed: 2026-11-09
  - id: S17
    title: CF2 series DXF support FAQ
    publisher: Mimaki
    url: https://mimaki.com/support/faq/operation/entry-58872.html
    accessed: 2026-11-09
  - id: S18
    title: Corrugator tooling article (Sep/Oct 2014) – point-to-point vs point-to-flat
    publisher: Sauer System
    url: https://www.sauersystem.com/cmss_files/attachmentlibrary/PDF-Downloads/Corrugator-Tooling-SepOct14.pdf
    accessed: 2026-11-09
  - id: S19
    title: Scoring tools catalogue
    publisher: Sauer System
    url: https://www.sauersystem.com/scoring-tools.html
    accessed: 2026-11-09
  - id: S20
    title: Slit scored sheets and pads
    publisher: Independent Corrugator Inc.
    url: https://corrugated-sheets.com/speciality-corrugated-board/slit-scored-sheets-pads/
    accessed: 2026-11-09
  - id: S21
    title: US6682468B2 Rotating scoring head with curvilinear nib
    publisher: Google Patents
    url: https://patents.google.com/patent/US6682468
    accessed: 2026-11-09
  - id: S22
    title: Die specification form (perforation cut/nick values)
    publisher: Jotform (die maker form)
    url: https://www.jotform.com/form/261062552540045
    accessed: 2026-11-09
---

# Die cutting and tooling

> Confidence: **industry-typical**. Many values come from tooling-vendor literature. Replace with die-maker and house data in `company/`.
> Source note: sources were consulted through search-indexed extracts, and vendor pages (CITO, voestalpine, Sauer) were not opened in full. Confirm formulas with the matrix or rule supplier's current chart.

## Flatbed vs rotary die cutting

| Aspect | Flatbed (platen) | Rotary |
|---|---|---|
| Motion | stop–start stamping of each sheet [S1] | continuous, cylinder against anvil [S1] |
| Typical speed (vendor figures) | 2000–5000 sheets/h [S2] | 8000–12000 sheets/h [S2] |
| Accuracy | sources conflict: one rates flatbed "high", others rate rotary tighter (**VERIFY**) [S2][S3] | vendors claim ±0.05 mm [±0.002 in] or better on dies (**VERIFY**) [S3] |
| Material | suits thick and sheet-fed stock, including corrugated sheets [S3] | high volume. Thinner web stock in labels. Rotary die cutters for corrugated are sheet-fed |
| Tooling | flat plywood die (cheaper) | curved die, more costly to make [S3] |
| Best for | short runs, complex or precise die-cut cartons, litho-laminated work | long runs, RSC-like die-cuts, in-line flexo print |

Engineering notes:

- Rotary corrugated die cutting cuts against a urethane anvil. This tends to crush board more and gives slightly lower dimensional accuracy than flatbed. Flatbed is preferred for tight registration to litho print. These are general practice statements with no source seen (**VERIFY** with house capability studies).
- Get machine-specific tolerances from the OEM. Vendor accuracy claims are marketing figures [S2][S3].

## Steel rule types, heights and point sizes

### Rule types

| Rule | Function | Notes |
|---|---|---|
| Cutting rule | cuts through | center bevel (CB) is the most common for board; long center bevel (LCB/CFB, facette) is for harder or thicker stock including corrugated [S4] |
| Creasing rule | makes a fold line | round-nosed; set lower than the cutting rule (see below). Use at least 3 pt for corrugated [S6] |
| Perforating rule | cut and nick pattern | defined by cut length and nick (tie) length. Micro-perforation has nicks under 0.8 mm; examples are 0.3 mm cut / 0.4 mm nick at 35 tpi and 0.2 / 0.3 mm at 50 tpi [S22] |
| Zipper (tear strip) rule | wavy or arrow perforation for tear-open strips | profile set by the rule maker (house data) |
| Cut-crease (perf-crease) rule | alternating cut and crease segments, used for folds on heavy or reverse-folded board | segment lengths are house data |
| Side-bevel rule | single-sided bevel for tight bends and flush finish | one source wrongly uses "side bevel" as an alias for center bevel (**VERIFY** terminology) [S4] |

### Rule height

- Standard cutting rule height: **23.8 mm [0.937 in]**, used in most countries. Some Asian markets use **23.6 mm [0.929 in]**, which shifts every creasing-rule height down [S4][S6].
- US letterpress height **0.918 in [23.32 mm]** is also used. One supplier notes that matrix scoring typically uses 2 pt rule at .918 in height [S5].
- 0.937 in × 25.4 = 23.80 mm; 0.918 in × 25.4 = 23.32 mm (checked in Python).

### Point size (rule thickness)

| Point | mm [in] | Source |
|---|---|---|
| 2 pt | 0.71 [0.028] | [S4] |
| 3 pt | 1.05 [0.041]; one source gives 1.07 [0.042] (**VERIFY**) | [S4] |
| 4 pt | 1.42 [0.056] | [S4] |

1 point ≈ 0.353 mm (1/72 in) [S4]. The nominal value differs slightly from the exact multiple (3 × 0.353 = 1.058 mm).

## Creasing rule height and creasing matrix (channel) width

### Equation (CITO method)

```
Creasing rule height:   h = H_cut − c            (cartonboard; c = board caliper)
                        h = H_cut − e            (corrugated;  e = compressed board thickness)
                        (additional ≈0.1 mm reduction when the matrix has a metal base — VERIFY)
Channel (groove) width: B = 1.5·c + d            (cartonboard)
                        B = 2.0·e + d            (corrugated)
Channel depth (corrugated) ≈ e
```

### Variables

- `H_cut`: cutting rule height, mm [in] (23.80 or 23.60 mm)
- `c`: cartonboard caliper, mm [in]
- `e`: compressed thickness of corrugated board (the board is compressed before the calculation, because only the remaining height counts), mm [in]
- `d`: creasing rule width (point size), mm [in]
- `h`: creasing rule height, mm [in]
- `B`: channel width, mm [in]

Sources: [S6][S7][S8][S9].

- In practice the matrix (channel plus its base) makes up the height difference. PrintWeek's example pairs a 23.4 mm creasing rule with a 0.4 mm matrix [S6].
- **VERIFY**: the brief's "≈ rule width + 1.5 × caliper" holds for **cartonboard only** [S9]. Corrugated uses 2 × compressed thickness [S8]. The PrintWeek examples are internally inconsistent [S6], and a lower-authority guide gives "caliper + 0.3–0.5 mm" for carton. Confirm with the matrix supplier's chart.

### Validity

- Flatbed die cutting with a pre-made creasing matrix.
- Grain direction, board type (FBB, SBS, recycled, E/B/C flute) and fold direction (normal or reverse) all shift the optimum. Matrix makers give corrections.

### Worked example: corrugated (SI)

e = 1.0 mm (compressed E-flute, example), d = 1.05 mm (3 pt), H_cut = 23.80 mm.

- B = 2.0 × 1.0 + 1.05 = **3.05 mm** [0.120 in]. CITO's own example, with a 1 mm rule, gives a 3.0 mm channel, i.e. a 1.0 × 3.0 mm matrix [S7].
- h = 23.80 − 1.0 = **22.80 mm** [0.898 in]

### Worked example: corrugated (US)

e = 0.039 in, d = 0.041 in, H_cut = 0.937 in.

- B = 2 × 0.039 + 0.041 = **0.119 in** [3.02 mm]
- h = 0.937 − 0.039 = **0.898 in** [22.81 mm]

### Worked example: cartonboard (SI and US)

c = 0.50 mm [0.020 in], d = 0.71 mm [0.028 in] (2 pt).

- B = 1.5 × 0.50 + 0.71 = **1.46 mm** [US: 1.5 × 0.020 + 0.028 = 0.058 in]
- h = 23.80 − 0.50 = **23.30 mm** (23.20 mm with the 0.1 mm metal-base reduction, **VERIFY**) [US: 0.937 − 0.020 = 0.917 in]

### Limitations

These are empirical starting values. Trial crease and fold tests (crease bending stiffness, visual cracking) decide the final setting. When a matrix is used, NA Graphics advises reducing the packing under the top sheet by about 0.010 in [0.25 mm] to allow for the matrix thickness [S5].

## Nicks (ties)

- **Purpose**: nicks are small uncut gaps ground into the cutting rule. They hold blanks in the sheet through delivery and stripping.
- **Strength vs grain**: nicks running in the machine (fibre) direction are about twice as strong as nicks across it [S10].
- **Rubber and nicks**: ejection rubber is generally set 1.0–2.0 mm [0.04–0.08 in] from the cutting rule to keep nicks from breaking [S10].
- **During a run**: nicks often have to be added or widened as the run progresses because of displacement forces. Nick grinders and manual nick tools are used to make and extend them [S10][S13].
- **Placement (practice)**: put nicks on waste-side edges, away from visible print and glue areas, and space them evenly. Use wider or more nicks on corrugated than on carton. No source seen gives numeric nick widths for corrugated, so use die-maker standards (**VERIFY**: house data).

## Ejection rubber, counters and make-ready

- **Ejection rubber hardness**: CITO profiles for corrugated and solid board are rated 70 Shore A (±5) [S11][S12]. Softer grades for cartonboard and harder or profiled grades for multi-wall exist, but no source seen gives a general hardness table (**VERIFY**).
- **Profiles**: profiled rubbers (for example a pointed "peak" profile) reduce the contact area and denting near perforation and cut-crease rules [S12]. C-profile rubber helps stop the flute being crushed at the edges of tuck-in flaps [S11].
- **Counters / creasing matrices**: for cartonboard, use a pre-made matrix or a milled counter plate, sized per the creasing equation above. Corrugated may run without a counter, with a soft crease, or with a corrugated matrix.
- **Make-ready**: make-ready means levelling the die (patching or packing) so that every rule cuts or creases evenly at minimum pressure. Excess pressure crushes board and dulls rules. Packing is adjusted when a matrix is used [S5].

## Score types for corrugated and their effect on folding and cracking

- **Corrugator (slitter-scorer) scores**: a scoring head (male) runs against an anvil (female or flat) [S21].
- **Profiles available**:
  - industry-standard 3-point, offset point-to-point, and point-to-point
  - point-to-flat (male-to-flat)
  - band-print designs where a flat male bead presses into a polyurethane-covered anvil [S18][S19][S20]

| Profile | Fold behaviour | Trade-offs |
|---|---|---|
| 3-point / offset point-to-point | crisp fold line | distorts the outer liner, which can leave blank print areas where ink does not take [S18] |
| Point-to-flat (male-to-flat) | less outer-liner distortion | weaker score; folds less precisely [S18] |
| Band-print (flat bead into PU anvil) | definition comes mainly from the inner liner and medium | proprietary system [S18] |

- One scoring head rarely gives crisp scores on single-, double- and triple-wall board, so heads are often changed when caliper changes [S21].
- Typical defects are rolled scores and torn, cracked or cut liners [S21].
- Score cracking also depends on moisture (see `manufacturing/corrugator-and-converting.md`).

## CAD line types and exchange formats

### Line types

| Line type | Meaning | CFF2 code (Kodak listing) |
|---|---|---|
| Cut | through-cut | 1 [S14] |
| Crease | fold line (normal) | 2 [S14] |
| Perforation | cut/nick pattern | 3 [S14] |
| Score | partial-depth score | 4 [S14] |
| Reverse crease | crease from the opposite side (fold away) | system-specific |
| Half-cut (kiss/partial cut) | cuts the top layer only | system-specific |
| Bleed / print / annotation | non-tooling layers for artwork | system-specific |

**VERIFY**: CFF2 pointage and line-type mappings differ between CAD systems. Map them explicitly on every import and export [S14].

### Exchange formats

| Format | Use | Notes |
|---|---|---|
| CF2 / CFF2 (Common File Format 2) | die-making data exchange, CAD/CAM [S16] | ArtiosCAD imports and exports it [S15]. Only newer releases read the latest CF2 variants. Plotters and cutters accept it [S17] |
| DDES / DDES3 | die design exchange (older ANSI format) | supported for import and export in ArtiosCAD [S15]. DDES2 is not confirmed in the sources seen (**VERIFY**) |
| DXF | generic CAD | layer and line-type mapping is lost or needs a map. Dimension and projection lines may need removing [S17] |
| ARD | ArtiosCAD native single-design file [S15] | proprietary |
| HPGL, EPS, Elcede, CAPE CIF | plotting, artwork and palletising outputs [S15] | |

- **Rule for Auto3D**: keep a line-type map in `company/` (house layer → CF2 type and pointage → DXF layer) and apply it on every export.

## Design rules for die-cut corrugated (practice)

These are qualitative rules. Numeric minimum distances are die-maker house data, because no source seen gives them (**VERIFY**).

- Keep a minimum distance between parallel rules and between rules and the sheet edge. Very close rules weaken the plywood die and make stripping hard.
- Do not place a crease very close to a cut running parallel to it, because the flute collapses and cracks.
- Rule bend radius has a minimum per point size and bevel. Side-bevel rule bends tighter than center bevel [S4].
- Line up flaps and creases with the flute direction where possible. Creases across the flutes fold more cleanly than creases along them.
- Allow for caliper at every fold. Inside panel dimension = crease-to-crease minus the allowance (see `dimensional/dimensions-and-allowances.md`).
- Put nicks on waste edges and away from glue flaps and print [S10].
