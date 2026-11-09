---
id: kb.performance.environmental-factors
title: BCT Reduction Factors — Humidity, Storage Time, Stacking Pattern, Pallet, Cut-outs, Print, Safety Factors
domain: performance
tags: [bct, reduction-factor, multiplier, humidity, moisture, creep, storage-time, stacking-pattern, column-stack, interlock, pallet-overhang, deckboard-gap, handhole, vent-hole, print, safety-factor]
applies_to: [corrugated]
confidence: industry-typical
status: draft
last_reviewed: 2026-11-09
reviewer: unreviewed
supersedes: []
sources:
  - id: S1
    title: Is Your Corrugated Stored Correctly? (environmental multiplier table attributed to Fibre Box Association data)
    publisher: Accurate Box Company
    url: https://www.accbox.com/blog/is-your-corrugated-stored-correctly/
    accessed: 2026-11-09
  - id: S2
    title: How-To Guide – Measuring Boxes (compression loss multipliers table)
    publisher: IPS Packaging (ipack.com)
    url: https://www.ipack.com/blog/how-to-guide-measuring-boxes
    accessed: 2026-11-09
  - id: S3
    title: The Tech Box – July 2021 (revised stacking-pattern compression loss)
    publisher: Fibre Box Association
    url: https://www.fibrebox.org/news/the-tech-box-july-2021
    accessed: 2026-11-09
  - id: S4
    title: More About Compression (BoxComp help – pallet overhang losses)
    publisher: Pkg Solutions
    url: http://pkgsolutions.co.uk/boxcomp/bcHelp/Compression.html
    accessed: 2026-11-09
  - id: S5
    title: Thesis on corrugated box stacking strength (cites Kellicutt 1963 and Moody & Skidmore 1966)
    publisher: core.ac.uk (university repository)
    url: https://core.ac.uk/download/287319875.pdf
    accessed: 2026-11-09
  - id: S6
    title: Pallet Overhang Phase 2 (cites Kim et al. 2023 and Fibre Box Handbook)
    publisher: Fibre Box Association
    url: https://www.fibrebox.org/assets/2025/07/Pallet_Overhang_Phase_2.pdf
    accessed: 2026-11-09
  - id: S7
    title: Why Corrugated Boxes May Look Usable in Storage but Fail During Packing or Shipping
    publisher: PaperIndex Academy
    url: https://www.paperindex.com/academy/why-corrugated-boxes-may-look-usable-in-storage-but-fail-during-packing-or-shipping/
    accessed: 2026-11-09
  - id: S8
    title: Michigan State University thesis on long-term storage of corrugated boxes (retention factors; cites Hanlon 1984)
    publisher: Michigan State University Libraries
    url: https://d.lib.msu.edu/etd/32960/FULL_TEXT/view
    accessed: 2026-11-09
  - id: S9
    title: Frozen to Fortified – Strengthening Corrugated Packaging Against Cold Weather Conditions
    publisher: AICC
    url: https://now.aiccbox.org/frozen-to-fortified-strengthening-corrugated-packaging-against-cold-weather-conditions/
    accessed: 2026-11-09
  - id: S10
    title: Compression Strength Estimation of Corrugated Board Boxes for a Reduction in Sidewall Surface Cutouts
    publisher: MDPI Materials 16(2):597
    url: https://www.mdpi.com/1996-1944/16/2/597
    accessed: 2026-11-09
  - id: S11
    title: Compressive Strength of Corrugated Paperboard Packages with Low and High Cutout Rates
    publisher: MDPI Materials 16(6):2360
    url: https://www.mdpi.com/1996-1944/16/6/2360
    accessed: 2026-11-09
  - id: S12
    title: Estimation of the Compressive Strength of Cardboard Boxes Including Packaging Overhanging on the Pallet
    publisher: MDPI Applied Sciences 14(2):819
    url: https://www.mdpi.com/2076-3417/14/2/819
    accessed: 2026-11-09
---

# BCT Reduction (Environmental) Factors

> *Industry-typical values — replace with supplier/house data in `company/`.*
>
> **Source access note (2026-11-09):** values were taken from web-search extracts of the sources
> listed; the Fibre Box Handbook itself was not consulted. Most multiplier tables in circulation
> are secondary reproductions of FBA data and **disagree in places (marked VERIFY)**. Where an
> extract cited a value to a document in a list of results, the attribution is marked VERIFY.

## How reduction factors are used

Lab BCT is measured on empty boxes at standard conditioning (23 °C, 50 %RH). In service, the box
loses strength from moisture, time under load (creep), stacking pattern, pallet geometry, cut-outs,
print and handling. The common method multiplies lab BCT by one multiplier per condition:

```
BCT_service = BCT_lab · m1 · m2 · ... · mn
```

| Symbol | Meaning | Unit |
|---|---|---|
| BCT_lab | measured (or McKee-predicted) BCT at 23 °C / 50 %RH | N [lbf] |
| m_i | multiplier for condition i (= 1 − fractional loss) | – |
| BCT_service | estimated strength under the combined conditions | N [lbf] |

Validity: factors are empirical and assumed independent; multiplying them is convention, not
physics. One MSU study found published strength-retention factors greatly **overestimate** box
endurance in long-term storage [S8] (attribution VERIFY) — i.e. the product may be non-conservative.

Worked example: BCT_lab = 2462 N (553 lbf); 90 days storage (0.55 [S1][S2]) and 80 %RH
(0.68 [S1][S2]):
- SI: 2462 × 0.55 × 0.68 = 2462 × 0.374 = **921 N**
- US: 553 × 0.374 = **207 lbf** (= 921 N)

Limitations: interactions (e.g. humidity accelerates creep) are not captured; the multipliers are
generic, not board-specific.

## Relative humidity / moisture content

| Condition (equilibrium, under load) | Loss | Multiplier | Source |
|---|---|---|---|
| 50 %RH | 0 % (reference) | 1.00 | [S1][S2] |
| 60 %RH | 10 % | 0.90 | [S1][S2] |
| 80 %RH | 32 % | 0.68 | [S2] |
| 90 %RH | 52 % | 0.48 | [S1][S2] |
| 100 %RH | 85 % | 0.15 | [S2] |
| Cyclic RH | loss increases (no single value) | – | [S1] |

- Secondary statement: about 50 % loss when RH rises from 50 % to 90 % [S7] — consistent with
  the 52 % table value.
- Michigan State work found strength declines as a second-order polynomial with RH and that rising
  board moisture content lowers both dynamic and constant-load compression strength [S8]
  (attribution VERIFY).
- Intermediate RH (e.g. 70 %RH) — not retrieved; do not interpolate without a source. **VERIFY**.

## Storage time under load (creep)

| Time under load | Loss | Multiplier | Source |
|---|---|---|---|
| 10 days | 37 % | 0.63 | [S1][S2] |
| 30 days | 40 % | 0.60 | [S1][S2] |
| 90 days | 45 % | 0.55 | [S1][S2] |
| 180 days | 50 % | 0.50 | [S1][S2] |

- Moody & Skidmore (1966): containers retained only 55 % of original yield force after three
  months of storage [S5] (attribution VERIFY) — consistent with the 90-day value.
- AICC: boxes may lose nearly 45 % of compression strength after 90 days in humid storage [S9].
- The time factors already include the loss to time-under-load at standard conditions; they are
  usually multiplied with the RH factor. Whether the published time factors embed some humidity is
  **VERIFY** (original FBA table not consulted).
- Kellicutt & Landt's time-to-failure relation (log-time) was not retrieved — **VERIFY**.

## Stacking pattern

| Pattern | Loss | Multiplier (best / worst) | Source |
|---|---|---|---|
| Columnar, aligned | negligible | ~1.0 | [S2] |
| Columnar, aligned (original FBA) | 0–8 % | 1.00–0.92 | [S3] |
| Columnar, aligned (FBA newer data, 2021) | 12–20 % | 0.88–0.80 | [S3] |
| Columnar, aligned, 3 high (Kellicutt 1963) | 23 % | 0.77 | [S5] (attribution VERIFY) |
| Misaligned columns | up to 50 % | ≥ 0.50 | [S5] (attribution VERIFY) |
| Interlocked (ipack table) | 40–60 % | 0.80 / 0.60 — **VERIFY** (multipliers do not match the stated loss) | [S2] |
| Interlocked (Accurate Box / FBA) | 40–60 % | 0.60 / 0.40 | [S1] |
| Interlocked (FBA newer data, 2021) | 49–54 % | 0.51–0.46 | [S3] |

**VERIFY — conflict:** the 2021 FBA data [S3] show columnar-aligned loss is larger (12–20 %) than
the "negligible / 0–8 %" in older tables [S2][S3]. For new designs use the 2021 values or your
own tests.

## Pallet overhang and deckboard gaps

| Condition | Loss | Multiplier | Source |
|---|---|---|---|
| Overhang 25 mm (1 in) on one side | 14–34 % | 0.86–0.66 | [S4] |
| Overhang 50 mm (2 in) on one side and one end | 34–46 % | 0.66–0.54 | [S4] |
| Overhang, current Fibre Box Handbook estimate | 20–40 % | 0.80–0.60 | [S6] (attribution VERIFY) |
| Overhang, Kim et al. 2023 | 0–40 % | 1.00–0.60 | [S6] (attribution VERIFY) |
| Pallet deckboard gap | 10–25 % | 0.90 / 0.75 | [S2] |

- Any overhang removes support under the box's strongest region (corners and panel edges);
  avoid it rather than compensate for it. FEM-based estimation of overhang effect: [S12].

## Handling

| Condition | Loss | Multiplier | Source |
|---|---|---|---|
| Excessive handling | 10–40 % | 0.90 / 0.60 | [S2] |

## Handholes, vent holes and other cut-outs

Sidewall cut-outs reduce BCT; the loss depends on cut-out area, shape and position (near
corners and vertical edges is worst). Experimental and FEM models for low and high cut-out rates:
[S10][S11]. **VERIFY — no generic multiplier was retrieved; use [S10][S11] or a BCT test.**

## Print coverage / flexo crush

Heavy flexo print (high coverage, high impression) crushes flutes, reducing caliper and therefore
BCT (see caliper-loss formula in `kb.performance.board-tests-and-ect`). **VERIFY — no published
multiplier was retrieved in this session.**

## Temperature and cold-chain cycling

Cold storage, condensation and thawing raise board moisture; an MSU frozen-storage study found
thawing of frozen boxes reduced compression strength, and AICC discusses cold-weather strength
loss [S8][S9] (attribution of the MSU finding VERIFY). Treat as a humidity case (use the high-RH
multiplier) unless tested. **VERIFY — no temperature multiplier retrieved.**

## Dynamic / transit loads

Vibration and impacts in transit add load above the static stack weight and accelerate fatigue.
No sourced dynamic factor was retrieved — cover this with the safety factor or ISTA/ASTM testing
(see `kb.testing.*`). **VERIFY.**

## Safety-factor method

```
BCT_required = F_top · SF
SF ≥ 1 / (m1 · m2 · ... · mn)
```

| Symbol | Meaning | Unit |
|---|---|---|
| F_top | static top load on the bottom box | N [lbf] |
| SF | overall safety factor | – |

- Rule of thumb: Hanlon (1984) suggests using one-fourth of the box compressive strength as the
  safe load for long-term storage, i.e. SF = 4 [S8] (attribution VERIFY).
- The commonly quoted range SF 3–5+ is not directly sourced in this file — **VERIFY**; derive SF
  from the multipliers above and add margin for dynamic loads.

Worked example: F_top = 1090 N (245 lbf).
- Multiplier route: 90 days (0.55) × 80 %RH (0.68) = 0.374 → SF = 1/0.374 = 2.67 →
  BCT_required = 1090 × 2.67 = **2914 N** (655 lbf).
- With FBA-2021 columnar factor 0.80 [S3]: product 0.299 → SF = 3.34 → **3642 N** (819 lbf).
- Hanlon SF = 4 [S8]: 1090 × 4 = **4360 N** (980 lbf).

Limitations: the multiplier route can be non-conservative [S8]; neither route covers transit
dynamics. Full stacking procedure: `kb.performance.stacking-load-calc`.
