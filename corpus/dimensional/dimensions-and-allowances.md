---
id: kb.dimensional.dimensions-and-allowances
title: Inside, outside and score-to-score dimensions and caliper allowances
domain: dimensional
tags: [inside-dimensions, outside-dimensions, score-to-score, manufacturers-dimensions, allowance, caliper, flute, rsc, fefco-0201, astm-d2658, tappi-t827, fefco-r101, auto3d]
applies_to: [corrugated]
confidence: industry-typical
status: draft
last_reviewed: 2026-11-09
reviewer: unreviewed
supersedes: []
sources:
  - id: S1
    title: FEFCO Code of Designs (international fibreboard case code)
    publisher: FEFCO / ESBO
    url: https://www.fefco.org/sites/default/files/documents/FEFCO_Codes_of_Designs.pdf
    accessed: 2026-11-09
  - id: S2
    title: FEFCO Code, 2022 edition (copy distributed by Kindermann Wellpappen)
    publisher: FEFCO (copy hosted by Kindermann)
    url: https://www.kindermann-wellpappen.de/downloads/2022-04-21_FEFCO%20Code_WEB_unprotected.pdf
    accessed: 2026-11-09
  - id: S3
    title: ASTM D2658-18 (2023) Standard Test Method for Determining Dimensions of Fiberboard Boxes (preview)
    publisher: ASTM International (preview via iTeh)
    url: https://standards.iteh.ai/catalog/standards/astm/6481867e-0d78-4355-bafe-17e3c1349c36/astm-d2658-18-2023
    accessed: 2026-11-09
  - id: S4
    title: Fibre Box Association Glossary
    publisher: Fibre Box Association (hosted by IoPP)
    url: https://www.iopp.org/files/Fibrebox_Association_Glossary.pdf
    accessed: 2026-11-09
  - id: S5
    title: Corporate General Specification RD-160.2, Corporate Package Engineering
    publisher: 3M
    url: https://multimedia.3m.com/mws/media/296992O/cgs160-pkg-spec.pdf
    accessed: 2026-11-09
  - id: S6
    title: B155 TR2-2 Tolerances for Scored and Slotted Corrugated Sheets and Trays (2018 edition)
    publisher: Fibre Box Association / PMMI
    url: https://www.fibrebox.org/assets/2025/07/B155_TR2-2_Scored_and_Slotted_Sheets_2018_Edition.pdf
    accessed: 2026-11-09
  - id: S7
    title: Testing methods / recommendations (FEFCO Recommendation 101 listing)
    publisher: FEFCO
    url: https://www.fefco.org/technical-information/fefco-testing-methods-recommendations
    accessed: 2026-11-09
  - id: S8
    title: Box blank dimensioning, Test Method TAPPI/ANSI T 827 om-24
    publisher: TAPPI
    url: https://imisrise.tappi.org/TAPPI/Products/01/T/0104T827.aspx
    accessed: 2026-11-09
  - id: S9
    title: Corrugated fiberboard (flute designations and thickness table)
    publisher: Wikipedia
    url: https://en.wikipedia.org/wiki/Corrugated_fiberboard
    accessed: 2026-11-09
  - id: S10
    title: How to Measure a Corrugated Box (RSC score-allowance table)
    publisher: Atlantic Packaging
    url: https://www.atlanticpkg.com/wp-content/uploads/2025/12/How-to-Measure-a-Corrugated-Box.pdf
    accessed: 2026-11-09
  - id: S11
    title: The Ultimate Guide to Corrugated Boxes
    publisher: Shorr Packaging
    url: https://www.shorr.com/resources/blog/ultimate-guide-corrugated-boxes/
    accessed: 2026-11-09
  - id: S12
    title: Corrugated Box Size & Weight Calculator (RSC blank, 3/5/7 ply)
    publisher: Balaji Internationals
    url: https://balajiinternationals.in/packaging-calculator/corrugated-box-blank-size-calculator
    accessed: 2026-11-09
  - id: S13
    title: Standard for Corrugated Box Construction CS19.0.5
    publisher: Snap-on Inc.
    url: https://www.snapon.com/Snap-on-Files/Suppliers/Packaging-and-Labeling-Guidelines/StandardforCorrugatedBoxConstruction.pdf
    accessed: 2026-11-09
  - id: S14
    title: Expert Guide to Flutes in Corrugated Boxes
    publisher: Colorwing
    url: https://colorwing.com/blogs/guide-to-flutes-in-corrugated-boxes
    accessed: 2026-11-09
  - id: S15
    title: What is a FEFCO code and how do I choose the right box?
    publisher: Raja Group
    url: https://blog-contentcenter.raja-group.com/?p=168613
    accessed: 2026-11-09
---

# Inside, outside and score-to-score dimensions and caliper allowances

> Values marked *industry-typical* or *derived*: replace with supplier/house data in `company/`.
> Source note: the primary standards (FEFCO Code, ASTM D2658, TAPPI T 827, FEFCO R 101, FBA B155) were consulted only through search-indexed extracts while writing this file; their full text was not opened. Anything normative must be checked in the standard itself.

## Three dimension bases: inside, outside, manufacturer's (score-to-score)

A corrugated box has three common ways of being sized, and every CAD, quoting and quality conversation must say which one it uses.

- **Inside dimensions (ID)**: the distance between the inner surfaces of the erected box. This is the basis that guarantees product fit, and it is the default basis for ordering and specifying boxes in both the US and Europe [S1][S4][S15]. ASTM D2658 defines depth as the distance between the innermost surfaces measured perpendicular to length and width [S3].
- **Outside dimensions (OD)**: the distance between outer surfaces. OD controls pallet patterns, cube and carrier classification [S4].
- **Manufacturer's or score-to-score dimensions**: the distance between score-line centres on the flat blank (the scored and slotted sheet). The panel score-to-score size is larger than the inside size because some board is used up going around each corner. Several specifications state it as *score-to-score = inside dimension + scoring allowance* [S5]. The FEFCO Code measures flat-blank dimensions from the centre of the crease, taking the thickness of the material into account [S2].

Measurement methods:

- ASTM D2658 says the interior size can be **estimated** from score-to-score measurements once the scoring allowance is known (its Appendix X2), or **measured directly** with a box gauge. The tape method needs a tape that reads to at least 1/16 in (1.6 mm) [S3].
- TAPPI T 827 (current edition om-24) gives the method for measuring the score-to-score dimensions of a box blank. It covers all solid and corrugated fibreboard box designs, both die-cut and scored-and-slotted [S8].
- FEFCO Recommendation 101 is the European procedure for finding the internal dimensions of flap-type (one-piece) cases. FEFCO lists it as equivalent to TAPPI T 827 [S7].

## Dimension order: L × W × D (or H)

- **FEFCO**: dimensions are internal and written as length × width × height, in millimetres. *Length* is the longer side of the opening, *width* the shorter side, and *height* runs from the top opening to the bottom [S1][S15]. Inches or centimetres are used only in exceptional cases [S15].
- **US practice (FBA / ASTM)**: boxes are measured from the inside and stated as length × width × depth. Length and width describe the opening of the assembled box: length is the longer side and width the shorter [S3][S11]. A typical US customer specification reads "inside dimensions, length × width × height" [S13].
- **Flat blank (FEFCO)**: blank sizes give the dimension along the glue/crease lines first and the dimension across them second [S2]. Check this with the plant, because corrugator practice may instead put the dimension along the flutes first.
- **Rule for the assistant**: when a user gives three numbers without a basis, ask for the basis (ID, OD or manufacturer's) and the order. Never assume that "depth" means the dimension parallel to the flutes.

## Why allowances depend on flute, caliper and score

The panels of a flat scored-and-slotted sheet are larger than the inside dimensions of the erected box because the board's thickness is used up in the corners. The size of the allowance depends on:

- flute size,
- the basis weights of the liners and medium,
- the scoring pattern (score profile) [S6].

So the allowances below are tied to one board and one score profile. A plant's own table, measured on its own scoring heads, overrides them [S6][S10].

### Nominal caliper by flute, used as the base for allowance factors

| Flute | Nominal thickness, mm [in] | Flutes per metre (approx.) | Source |
|---|---|---|---|
| E | 1.6 [1/16] | ~295 | [S9] |
| B | 3.2 [1/8] | ~154 | [S9] |
| C | 4.0 [5/32] | ~128 | [S9] |
| A | 4.8 [3/16] | ~108 | [S9] |
| BC (double wall) | ~6–7 [~1/4] | n/a | [S14] |

**VERIFY**: other sources give different flute heights (see `materials/` flute files). Measured combined-board caliper (TAPPI T 411 / ISO 3034) is the correct input, never the nominal flute height. For BC, the sum of B + C nominal values (7.2 mm) is higher than the 6–7 mm in [S14]. Use measured caliper.

## Allowance model: allowance factor × caliper

### Equation

```
Score-to-score (manufacturer's) panel size:   S_i = I_i + k_s,i × t
Outside size:                                  O_i = I_i + k_o,i × t
Factor arrays, RSC (FEFCO 0201), order [L, W, H]:
   k_s = [1, 1, 2]      (inside → score)
   k_o = [2, 2, 4]      (inside → outside)
```

### Variables

- `I_i`: inside dimension along axis i (L, W or H), mm [in]
- `S_i`: score-to-score panel dimension on the flat blank, mm [in]
- `O_i`: outside dimension of the erected box, mm [in]
- `t`: measured combined-board caliper, mm [in]
- `k_s,i`, `k_o,i`: dimensionless allowance factors (multiples of caliper)

### Where the factors come from (geometry, confidence: derived)

- **Length and width, k_s = 1**: a 90° fold uses roughly half a caliper at each of the panel's two score lines (½ t + ½ t). For outside size, each wall adds a full caliper on each side, so k_o = 2.
- **Depth (height), k_s = 2**: the outer flaps fold over the inner flaps, so the panel carrying them must be taller by about one flap thickness at the top and one at the bottom. This is the "two flap thicknesses" rule. For outside depth, there are two flap layers at the top and two at the bottom, so k_o = 4.
- Supporting evidence: the published consensus is that score-to-score = inside + scoring allowance [S5]. Converters report about 1/8 in (3 mm) per side between inside and outside on single wall, about 1/4 in (6 mm) overall [S11][S12], which matches k_o = 2 with B/C flute. One converter calculator lists about +14 mm overall inside→outside for 5-ply (double wall) [S12], which matches k_o = 2 with t ≈ 7 mm.

**VERIFY**: an Atlantic Packaging RSC score-allowance table gives separate L/W/D deductions per flute (E, B, C), with values of 1/16, 1/8 and 3/16 in appearing in it. The extract was garbled, so the flute-by-dimension pairing could not be confirmed [S10]. The panel next to the manufacturer's joint, and the joint itself, often use a different (smaller) allowance in practice. The FBA/PMMI document notes that allowances depend on the score pattern [S6]. Treat k_s = [1, 1, 2] as a starting default only.

### Validity

- RSC (FEFCO 0201) and other slotted styles whose outer flaps fold over the inner flaps, with 90° folds on corrugator or slotter scores.
- Single wall E to A and double wall BC.
- Not valid for die-cut styles with tuck-in, rolled-edge or multi-layer walls (02xx variants, 04xx). For those, count the layers that sit inside each wall: each layer adds about 1 t to k_o on that axis.

### Limitations

- Caliper loss from crushing in the printer and die cutter reduces the true t (see `manufacturing/corrugator-and-converting.md`).
- Score profile changes the allowance. Point-to-flat and point-to-point scores fold at different positions.
- The factors give nominal values. Tolerances are covered in `dimensional/tolerances.md`.

### Worked example (SI): C-flute RSC, ID 400 × 300 × 250 mm, t = 4.0 mm

- Score-to-score: S = [400 + 1×4.0, 300 + 1×4.0, 250 + 2×4.0] = **[404.0, 304.0, 258.0] mm** [15.906, 11.969, 10.157 in]
- Outside: O = [400 + 8.0, 300 + 8.0, 250 + 16.0] = **[408.0, 308.0, 266.0] mm** [16.063, 12.126, 10.472 in]
- Reverse, from OD back to ID: 408 − 8 = 400; 308 − 8 = 300; 266 − 16 = 250 mm ✓

### Worked example (US): C-flute RSC, ID 16 × 12 × 10 in, t = 5/32 in (0.15625 in)

- Score-to-score: S = [16.15625, 12.15625, 10.3125] in, about **16 5/32 × 12 5/32 × 10 5/16 in** [410.4, 308.8, 261.9 mm]
- Outside: O = [16.3125, 12.3125, 10.625] in = **16 5/16 × 12 5/16 × 10 5/8 in** [414.3, 312.7, 269.9 mm]

(Arithmetic checked in Python.)

## Allowance table per flute (RSC, derived from the factor model)

These are nominal values from the factor model and the nominal calipers above (confidence: derived / industry-typical). Replace them with supplier/house data in `company/`.

| Flute | t mm [in] | Inside→score, L and W panel, mm [in] | Inside→score, depth, mm [in] | Inside→outside, L and W, mm [in] | Inside→outside, depth, mm [in] |
|---|---|---|---|---|---|
| E | 1.6 [0.063] | +1.6 [0.063] | +3.2 [0.126] | +3.2 [0.126] | +6.4 [0.252] |
| B | 3.2 [0.126] | +3.2 [0.126] | +6.4 [0.252] | +6.4 [0.252] | +12.8 [0.504] |
| C | 4.0 [0.157] | +4.0 [0.157] | +8.0 [0.315] | +8.0 [0.315] | +16.0 [0.630] |
| A | 4.8 [0.189] | +4.8 [0.189] | +9.6 [0.378] | +9.6 [0.378] | +19.2 [0.756] |
| BC | 7.2 [0.283] | +7.2 [0.283] | +14.4 [0.567] | +14.4 [0.567] | +28.8 [1.134] |

Calipers are from [S9] (single wall). The BC row uses the B + C sum, which conflicts with the ~6–7 mm in [S14] (**VERIFY**). The fixed values are the factor model applied to nominal caliper. US plants often round them to the nearest 1/16 in. The Atlantic table [S10] uses fractions of this size (1/16, 1/8, 3/16 in), but its pairing with each flute is unconfirmed (**VERIFY**).

## Allowance factors for other styles (layer counting)

Use the same rule for every style: **count the board layers on each axis.**

| Style (FEFCO) | k_s [L, W, H] | k_o [L, W, H] | Reasoning (derived) |
|---|---|---|---|
| 0200 HSC (half slotted, one flap set) | [1, 1, 1] | [2, 2, 2] | flaps on one end only, so one flap layer |
| 0201 RSC | [1, 1, 2] | [2, 2, 4] | outer flaps over inner flaps at both ends |
| 0202 OSC | [1, 1, 2] | [2, 2, 4]; up to 6 in H where the outer flaps overlap | the overlap zone has a third layer |
| 0203 FOL | [1, 1, 2] | [2, 2, 6] | the outer flaps overlap completely: three layers per end |
| 0300/0301 telescope (lid over base) | per tray [1, 1, 1] | lid inside = base outside + clearance | two separate trays |

**VERIFY**: these are geometric derivations, not values from a standard. Confirm them against plant measurements made per TAPPI T 827 / FEFCO R 101 [S7][S8].

## Mapping to Auto3D factor arrays

Auto3D works with a dimension basis (inside, outside or score), a caliper `t`, and allowance factors per axis `[L, W, H]`. Use this mapping:

```
basis = "inside":  I given  →  S = I + k_s ⊙ t ;  O = I + k_o ⊙ t
basis = "score":   S given  →  I = S − k_s ⊙ t ;  O = S + (k_o − k_s) ⊙ t
basis = "outside": O given  →  I = O − k_o ⊙ t ;  S = O − (k_o − k_s) ⊙ t
(⊙ = element-wise multiply over [L, W, H])
```

- RSC defaults: `k_s = [1, 1, 2]`, `k_o = [2, 2, 4]`, so `k_o − k_s = [1, 1, 2]`.
- Store the factors per style **and** per score profile in `company/` (house allowance tables). The agent must state which table it used.
- If the house table gives fixed allowances in mm or in rather than factors, the factor is that fixed allowance divided by the caliper of the board the table was measured on. Do not carry a fixed allowance across to a different flute.
- Worked check, SI example above: `basis=inside`, I = [400, 300, 250], t = 4.0 gives S = [404, 304, 258] and O = [408, 308, 266] mm.

## Common errors

- Quoting the OD to a carrier or palletiser while giving the ID to the converter, or the other way round, without labelling which is which [S4].
- Using nominal flute height instead of measured caliper (see the caliper table caveat above).
- Treating score-to-score as the inside dimension. ASTM D2658 says the inside size can only be **estimated** from score-to-score once the allowance is known [S3].
- Using one allowance table for every flute. Allowances depend on flute, basis weights and score pattern [S6].
