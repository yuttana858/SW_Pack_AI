---
id: kb.performance.stacking-load-calc
title: Stacking Load Calculation — Top Load, Required BCT, Maximum Stack Height
domain: performance
tags: [stacking, top-load, bct-required, safety-factor, pallet-stacking, warehouse, max-stack-height, ect-selection, column-stacking]
applies_to: [corrugated, pallet]
confidence: derived
status: draft
last_reviewed: 2026-11-09
reviewer: unreviewed
supersedes: []
sources:
  - id: S1
    title: Is Your Corrugated Stored Correctly? (multipliers attributed to Fibre Box Association data)
    publisher: Accurate Box Company
    url: https://www.accbox.com/blog/is-your-corrugated-stored-correctly/
    accessed: 2026-11-09
  - id: S2
    title: How-To Guide – Measuring Boxes (compression loss multipliers)
    publisher: IPS Packaging (ipack.com)
    url: https://www.ipack.com/blog/how-to-guide-measuring-boxes
    accessed: 2026-11-09
  - id: S3
    title: The Tech Box – July 2021 (revised stacking-pattern loss)
    publisher: Fibre Box Association
    url: https://www.fibrebox.org/news/the-tech-box-july-2021
    accessed: 2026-11-09
  - id: S4
    title: Predicting Box Compression Strength (slides)
    publisher: Georgia Tech Renewable Bioproducts Institute (R. Popil)
    url: https://research.gatech.edu/sites/default/files/rbi/pdfs/Predicting%20Box%20Compression%20Strength_3.pdf
    accessed: 2026-11-09
  - id: S5
    title: Box compression analysis of world-wide data spanning 46 years (Urbanik & Frank 2006)
    publisher: USDA Forest Service Treesearch
    url: https://research.fs.usda.gov/treesearch/25180
    accessed: 2026-11-09
  - id: S6
    title: Michigan State University thesis on long-term storage (cites Hanlon 1984)
    publisher: Michigan State University Libraries
    url: https://d.lib.msu.edu/etd/32960/FULL_TEXT/view
    accessed: 2026-11-09
  - id: S7
    title: More About Compression (pallet overhang losses)
    publisher: Pkg Solutions
    url: http://pkgsolutions.co.uk/boxcomp/bcHelp/Compression.html
    accessed: 2026-11-09
---

# Stacking Load Calculation

> Derived procedure built on `kb.performance.box-compression` (McKee) and
> `kb.performance.environmental-factors` (multipliers). Multipliers are *industry-typical — replace
> with supplier/house data in `company/`*. Box and pallet masses and caliper in the examples are
> illustrative inputs. g = 9.80665 m/s².

## Step-by-step method

1. Gross mass per box m (product + inner packing + box), kg [lb].
2. Stack geometry: boxes high n (warehouse), or layers per pallet L, boxes per layer k, pallets
   high P, pallet mass m_p.
3. Static top load on the most-loaded (bottom) box, F_top (formulas below).
4. Environmental multipliers m_i for storage time, RH, stacking pattern, pallet, handling,
   cut-outs [S1][S2][S3][S7].
5. BCT_required = F_top / (m1·m2·…·mn), or F_top × SF (Hanlon's SF = 4 for long-term storage
   [S6], attribution VERIFY).
6. Required ECT from reverse McKee: ECT = BCT_required / (5.87·sqrt(h·Z)) [S4]; choose the next
   standard grade up, then recompute with that grade's real caliper.
7. Confirm with a BCT test; McKee tends to over-predict [S5].

## Top load on the bottom box — single warehouse stack

```
F_top = (n − 1) · m · g
```

| Symbol | Meaning | SI | US |
|---|---|---|---|
| n | boxes in the column, including the bottom box | – | – |
| m | gross mass of one box | kg | lb (use F = (n−1)·W with W in lbf) |
| g | 9.80665 | m/s² | – |
| F_top | load on the bottom box | N | lbf |

Validity: column-aligned, full-face contact, no load sharing with neighbouring stacks, no
product support (load carried by the box only).

Worked example: 12 kg (26.46 lb) box, 6 high.
- SI: F = 5 × 12 × 9.80665 = **588.4 N**
- US: F = 5 × 26.46 = **132.3 lbf** (= 588.4 N)

Limitations: ignores dynamic loads and uneven load distribution.

## Top load on the bottom box — pallets stacked P high

```
F_top = [ (L − 1) · m  +  (P − 1) · (L · k · m + m_p) / k ] · g
```

| Symbol | Meaning | SI | US |
|---|---|---|---|
| L | layers per pallet | – | – |
| k | boxes per layer | – | – |
| P | pallets high (including the bottom one) | – | – |
| m | gross mass per box | kg | lb |
| m_p | mass of one pallet (+ any top sheet/cap) | kg | lb |
| F_top | load on a bottom-layer box of the bottom pallet | N | lbf |

Validity: every upper pallet's weight is spread evenly over the k boxes of the top layer below
(rigid deck, no deckboard-gap concentration, no overhang); column-stacked layers.

Worked example: m = 12 kg (26.46 lb), k = 8, L = 5, P = 2, m_p = 25 kg (55.12 lb).
- Own pallet: (5 − 1) × 12 = 48 kg
- Upper pallet share: (5 × 8 × 12 + 25) / 8 = 505 / 8 = 63.125 kg
- SI: F = (48 + 63.125) × 9.80665 = 111.125 × 9.80665 = **1089.8 N**
- US: (4 × 26.46) + (40 × 26.46 + 55.12)/8 = 105.82 + 139.17 = **245.0 lbf** (= 1089.8 N)

Limitations: deckboard gaps concentrate the upper load (multiplier 0.90–0.75 [S2]); flexible
pallets and overhang reduce support further [S7].

## Required BCT with environmental factors

```
BCT_required = F_top / (m1 · m2 · ... · mn)
```

Worked example (continuing the pallet case, F_top = 1089.8 N = 245.0 lbf), 90 days storage
(0.55) and 80 %RH (0.68) [S1][S2]:
- Product = 0.374
- SI: BCT_required = 1089.8 / 0.374 = **2914 N**
- US: 245.0 / 0.374 = **655 lbf**
- Adding the FBA-2021 columnar-aligned loss (multiplier 0.80, upper end of 12–20 % loss [S3]):
  product 0.299 → **3642 N (819 lbf)**.

Required ECT for a 400 × 300 mm RSC (Z = 1400 mm = 55.12 in), caliper 4.0 mm (0.1575 in):
- Without stacking-pattern factor: 2914 / (5.87 × 74.83) = **6.63 kN/m = 37.9 lbf/in** → 40 ECT.
- With 0.80 factor: 3642 / 439.3 = **8.29 kN/m = 47.3 lbf/in** → needs a higher grade; a heavier
  single wall or double wall must be re-checked with its own (larger) caliper, which raises
  sqrt(h·Z) and lowers the ECT needed.

## Maximum stack height from BCT

```
n_max = floor( BCT · (m1 · m2 · ... · mn) / (m · g) ) + 1         # warehouse column
P_max = floor( (BCT·Πm − (L−1)·m·g) / ((L·k·m + m_p)·g / k) ) + 1   # pallets high
```

Variables as above; BCT is lab (or McKee) BCT in N [lbf]; for US units replace m·g by box
weight W in lbf. Validity as for the load formulas; the +1 counts the bottom box/pallet itself.

Worked example — warehouse: BCT = 2462 N (553.4 lbf, 32 ECT, 400 × 300 × 300 mm, McKee [S4]);
multipliers 0.374; m = 12 kg (26.46 lb).
- SI: allowable load = 2462 × 0.374 = 920.7 N; 920.7 / (12 × 9.80665) = 7.82 → n_max = 7 + 1 =
  **8 boxes high**
- US: 553.4 × 0.374 = 207.0 lbf; 207.0 / 26.46 = 7.82 → **8 boxes high**

Worked example — pallets (L = 5, k = 8, m_p = 25 kg / 55.12 lb):
- SI: own-pallet load 48 × 9.80665 = 470.7 N; each extra pallet adds 63.125 × 9.80665 = 619.0 N
  per box; (920.7 − 470.7)/619.0 = 0.727 → P_max = 0 + 1 = **1 (do not double-stack)**
- US: own 105.8 lbf; each extra pallet 139.2 lbf; (207.0 − 105.8)/139.2 = 0.727 → **1**

Limitations: McKee over-prediction [S5] and possible non-conservatism of multipliers [S6] mean
n_max should be confirmed by test; round down, never up.

## Decision checklist — when to upgrade

- **Use column stacking first.** Interlocking costs 40–60 % of BCT [S1][S2] (49–54 % in 2021 FBA
  data [S3]); switching to aligned columns is often cheaper than a board upgrade. Eliminate
  overhang (14–46 % loss [S7]) before upgrading board.
- **Required ECT within one grade of current:** upgrade liner/medium within the same flute (higher
  ECT grade), re-run McKee with new caliper.
- **Required ECT far above single-wall grades, or tall/large boxes:** move to a thicker flute or
  double wall — BCT rises with sqrt(caliper) [S4] as well as ECT.
- **Product can carry load (rigid, flat-topped, full-height):** product-supported loads reduce the
  load the box must carry — verify by test, the formulas above assume the box carries everything.
- **Large panels with no internal support / high stack:** add dividers, partitions or corner posts
  / inserts to carry vertical load; recompute or test (not covered by McKee).
- **High humidity, cold chain, long storage:** apply the 80–90 %RH and long-storage multipliers;
  consider moisture-resistant board — confirm by conditioned BCT test (e.g. 90 %RH).
- **Double-stacking pallets fails the P_max check:** use pallet racking, load caps/top frames, or
  reduce layers per pallet before upgrading every box.
- **Always:** confirm with BCT test at the target condition and, for transit, an ISTA/ASTM
  distribution test (see `kb.testing.*`).
