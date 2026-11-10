---
id: kb.reference.units-and-conversions
title: Units and conversions for packaging engineering (exact factors and quick-reference tables)
domain: reference
tags: [units, conversion, si, us-customary, lb-msf, gsm, basis-weight, grammage, ect, kn-m, burst, psi, kpa, kgf, lbf, newton, caliper, points, mils, micron, msf, density, pcf, temperature, moisture, psd, grms, g-acceleration]
applies_to: [corrugated, folding-carton, rigid, flexible, cushioning, pallet]
confidence: derived
status: draft
last_reviewed: 2026-11-09
reviewer: unreviewed
supersedes: []
sources:
  - id: S1
    title: "Pint 0.24.4 unit definitions file (default_en.txt): international yard 0.9144 m (since July 1959), grain 64.79891 mg, pound = 7000 grain, ton = 2000 lb, force_pound = g_0 × pound, kgf = g_0 × kg, psi = lbf/in², temperature offsets"
    publisher: Pint project (hgrecco/pint)
    url: https://github.com/hgrecco/pint/blob/0.24.4/pint/default_en.txt
    accessed: 2026-11-09
  - id: S2
    title: "Pint 0.24.4 constants file (constants_en.txt): standard_gravity = 9.80665 m/s² (since 1901)"
    publisher: Pint project (hgrecco/pint)
    url: https://github.com/hgrecco/pint/blob/0.24.4/pint/constants_en.txt
    accessed: 2026-11-09
  - id: S3
    title: "Paperboard (section Caliper/thickness: US caliper in thousandths of an inch or points; 0.024 in = 24 points)"
    publisher: Wikipedia
    url: https://en.wikipedia.org/wiki/Paperboard
    accessed: 2026-11-09
---

# Units and conversions

All factors are **derived** from the exact definitions below, which were read from the Pint 0.24.4 unit-definition files [S1][S2]. The arithmetic was checked in Python (IEEE double precision) and is shown to at least 6 significant figures. Pint takes these definitions from the international yard-and-pound agreement and the CGPM value of standard gravity. For legal metrology, cross-check against NIST SP 811 Appendix B (not consulted in this draft, so VERIFY if a regulator asks).

## Exact base definitions

| Quantity | Definition | Source |
|---|---|---|
| inch | 1 in = 1/36 yd = **25.4 mm exactly** (yard = 0.9144 m) | [S1] |
| foot | 1 ft = 12 in = **0.3048 m exactly** | [S1] |
| pound (mass, avoirdupois) | 1 lb = 7000 grain × 64.79891 mg = **0.45359237 kg exactly** | [S1] |
| standard gravity | g_n = **9.80665 m/s² exactly** | [S2] |
| pound-force | 1 lbf = g_n × 1 lb = **4.4482216152605 N** (exact product) | [S1][S2] |
| kilogram-force | 1 kgf = g_n × 1 kg = **9.80665 N exactly** | [S1][S2] |
| psi | 1 psi = 1 lbf/in² = **6894.757293168 Pa** | [S1] |
| short ton | 1 ton (US) = 2000 lb = **907.18474 kg** | [S1] |
| metric tonne | 1 t = **1000 kg** | [S1] |
| mil / thou / point | 1 mil = 1 thou = 0.001 in = **25.4 µm**. "Point" (caliper) is used the same way in paperboard: 1 pt = 0.001 in (a 0.024 in board is 24 points) | [S1] (mil, thou); [S3] (point) |
| °C / °F | T(°F) = T(°C) × 9/5 + 32; T(K) = T(°C) + 273.15 | [S1] |

## Basis weight (grammage): lb/MSF and g/m²

```
1 lb/MSF = 0.45359237 kg × 1000 g/kg / (1000 × 0.09290304 m²) = 4.882428 g/m²
1 g/m²   = 0.2048161 lb/MSF
```

- MSF = 1000 ft² = **92.90304 m²**. 1 ft² = 0.09290304 m². 1 m² = 10.76391 ft².
- Worked example, SI → US: a 200 g/m² liner = 200 × 0.2048161 = **40.96 lb/MSF**.
- Worked example, US → SI: a 26 lb/MSF medium = 26 × 4.882428 = **126.94 g/m²**.
- Other units: 1 g/m² = 0.02949352 oz/yd².
- Limitation: some mills use "lb per 1000 ft²" and some use "lb per 3000 ft² ream" (paper). Confirm the ream basis before converting.

| lb/MSF | g/m² |  | g/m² | lb/MSF |
|---|---|---|---|---|
| 26 | 126.9 |  | 80 | 16.39 |
| 33 | 161.1 |  | 100 | 20.48 |
| 35 | 170.9 |  | 112 | 22.94 |
| 36 | 175.8 |  | 125 | 25.60 |
| 40 | 195.3 |  | 140 | 28.67 |
| 42 | 205.1 |  | 150 | 30.72 |
| 56 | 273.4 |  | 175 | 35.84 |
| 69 | 336.9 |  | 200 | 40.96 |
| 90 | 439.4 |  | 250 | 51.20 |
|  |  |  | 300 | 61.44 |
|  |  |  | 440 | 90.12 |

The values in the table are conversion inputs, not grade definitions. Grade tables live in `materials/`.

## Edge crush and line load: lb/in, kN/m, kgf/cm

```
1 lbf/in = 4.4482216 N / 0.0254 m = 175.1268 N/m = 0.1751268 kN/m
1 kN/m   = 5.710147 lbf/in
1 kgf/cm = 0.980665 kN/m;  1 kN/m = 1.019716 kgf/cm;  1 lbf/in = 0.1785797 kgf/cm
```

Worked example, US → SI: 32 lbf/in × 0.1751268 = **5.604 kN/m**. SI → US: 7.0 kN/m × 5.710147 = **39.97 lbf/in**.

| ECT (lbf/in) | kN/m | kgf/cm |  | kN/m | lbf/in |
|---|---|---|---|---|---|
| 23 | 4.028 | 4.107 |  | 3 | 17.13 |
| 26 | 4.553 | 4.643 |  | 4 | 22.84 |
| 29 | 5.079 | 5.179 |  | 5 | 28.55 |
| 32 | 5.604 | 5.715 |  | 6 | 34.26 |
| 40 | 7.005 | 7.143 |  | 7 | 39.97 |
| 44 | 7.706 | 7.858 |  | 8 | 45.68 |
| 48 | 8.406 | 8.572 |  | 9 | 51.39 |
| 51 | 8.931 | 9.108 |  | 10 | 57.10 |
| 55 | 9.632 | 9.822 |  | 12 | 68.52 |
| 61 | 10.683 | 10.893 |  | 15 | 85.65 |
| 71 | 12.434 | 12.679 |  |  |  |
| 82 | 14.360 | 14.644 |  |  |  |
| 112 | 19.614 | 20.001 |  |  |  |

Limitation: this converts units only. ECT values from different test methods (for example TAPPI T 811 versus ISO 3037 specimen preparation) are not interchangeable even after conversion. See `testing/`.

## Pressure and stress (burst, compression stress): psi, kPa, kgf/cm², bar

```
1 psi     = 6.894757 kPa          1 kPa = 0.1450377 psi
1 kgf/cm² = 98.0665 kPa           1 kPa = 0.01019716 kgf/cm²
1 psi     = 0.07030696 kgf/cm²    1 kgf/cm² = 14.22334 psi
1 bar     = 100 kPa = 14.50377 psi;  1 MPa = 145.0377 psi
```

Worked example, US → SI: 200 psi burst = 200 × 6.894757 = **1379.0 kPa** (14.061 kgf/cm²). SI → US: 1000 kPa = **145.0 psi**.

| psi | kPa | kgf/cm² |  | kPa | psi | kgf/cm² |
|---|---|---|---|---|---|---|
| 125 | 861.8 | 8.788 |  | 500 | 72.5 | 5.099 |
| 150 | 1034.2 | 10.546 |  | 750 | 108.8 | 7.648 |
| 175 | 1206.6 | 12.304 |  | 1000 | 145.0 | 10.197 |
| 200 | 1379.0 | 14.061 |  | 1250 | 181.3 | 12.746 |
| 250 | 1723.7 | 17.577 |  | 1500 | 217.6 | 15.296 |
| 275 | 1896.1 | 19.334 |  | 2000 | 290.1 | 20.394 |
| 350 | 2413.2 | 24.607 |  |  |  |  |
| 500 | 3447.4 | 35.153 |  |  |  |  |

## Force and mass: lbf, N, kgf, lb, kg

```
1 lbf = 4.448222 N = 0.4535924 kgf      1 N   = 0.2248089 lbf = 0.1019716 kgf
1 kgf = 9.80665 N  = 2.204623 lbf       1 kN  = 224.8089 lbf
1 lb  = 0.45359237 kg                   1 kg  = 2.204623 lb
1 oz  = 28.34952 g;  1 ozf = 0.2780139 N
```

Worked example: BCT 1000 lbf = **4448.2 N** (4.4482 kN; 453.59 kgf). 5 kN = **1124.0 lbf** (509.9 kgf).

| lbf | N | kN | kgf |  | kN | lbf | kgf |
|---|---|---|---|---|---|---|---|
| 100 | 444.8 | 0.4448 | 45.36 |  | 1 | 224.8 | 102.0 |
| 250 | 1112.1 | 1.1121 | 113.40 |  | 2 | 449.6 | 203.9 |
| 500 | 2224.1 | 2.2241 | 226.80 |  | 5 | 1124.0 | 509.9 |
| 750 | 3336.2 | 3.3362 | 340.19 |  | 10 | 2248.1 | 1019.7 |
| 1000 | 4448.2 | 4.4482 | 453.59 |  | 20 | 4496.2 | 2039.4 |
| 1500 | 6672.3 | 6.6723 | 680.39 |  |  |  |  |
| 2000 | 8896.4 | 8.8964 | 907.18 |  |  |  |  |

Mass: 1 kg = 2.205 lb; 10 kg = 22.046 lb; 25 kg = 55.116 lb; 50 kg = 110.231 lb; 1000 kg = 2204.623 lb. Tons: 1 short ton = 0.9071847 t; 1 t = 1.102311 short ton = 2204.623 lb.

Limitation: kgf and lbf depend on standard gravity. A "kg" reading on a compression tester is kgf. Report N in SI.

## Length, caliper and thickness

```
1 in = 25.4 mm;  1 mm = 0.03937008 in
1 ft = 0.3048 m;  1 m = 3.280840 ft
1 mil = 1 thou = 1 pt = 0.001 in = 0.0254 mm = 25.4 µm
```

| Caliper (pt / mil) | mm | µm |  | mm | in |
|---|---|---|---|---|---|
| 10 | 0.2540 | 254.0 |  | 1 | 0.0394 |
| 12 | 0.3048 | 304.8 |  | 3 | 0.1181 |
| 14 | 0.3556 | 355.6 |  | 6.35 | 0.2500 |
| 16 | 0.4064 | 406.4 |  | 10 | 0.3937 |
| 18 | 0.4572 | 457.2 |  | 50 | 1.9685 |
| 20 | 0.5080 | 508.0 |  | 100 | 3.9370 |
| 24 | 0.6096 | 609.6 |  | 300 | 11.8110 |
| 30 | 0.7620 | 762.0 |  | 1000 | 39.3701 |

Drop heights (exact): 12 in = 304.8 mm; 18 in = 457.2 mm; 24 in = 609.6 mm; 30 in = 762.0 mm; 36 in = 914.4 mm; 42 in = 1066.8 mm; 48 in = 1219.2 mm.

## Area and volume

```
1 ft² = 0.09290304 m²     1 m² = 10.76391 ft²
1 MSF = 92.90304 m²       1000 m² = 10.76391 MSF
1 in³ = 16.387064 cm³     1 ft³ = 0.02831685 m³ = 28.31685 L    1 m³ = 35.31467 ft³
```

Worked example: 25 000 m² of board = 25 000 × 0.01076391 = **269.10 MSF**. Box inside 16 × 12 × 8 in = 1536 in³ = **25.17 L**.

## Density (cushioning foams, bulk materials): pcf and kg/m³

```
1 lb/ft³ (pcf) = 16.01846 kg/m³      1 kg/m³ = 0.06242796 pcf
```

| pcf | kg/m³ |  | kg/m³ | pcf |
|---|---|---|---|---|
| 1.0 | 16.02 |  | 15 | 0.936 |
| 1.2 | 19.22 |  | 20 | 1.249 |
| 1.5 | 24.03 |  | 25 | 1.561 |
| 1.7 | 27.23 |  | 30 | 1.873 |
| 2.0 | 32.04 |  | 35 | 2.185 |
| 2.2 | 35.24 |  | 45 | 2.809 |
| 3.0 | 48.06 |  | 60 | 3.746 |
| 4.0 | 64.07 |  |  |  |
| 6.0 | 96.11 |  |  |  |

The values are conversion inputs, not foam grades. Foam data lives in `cushioning/`.

## Temperature

```
T_F = T_C × 9/5 + 32         T_C = (T_F − 32) × 5/9         T_K = T_C + 273.15
```

| °C | °F |  | °C | °F |
|---|---|---|---|---|
| −40 | −40.0 |  | 23 | 73.4 |
| −29 | −20.2 |  | 25 | 77.0 |
| −18 | −0.4 |  | 30 | 86.0 |
| 0 | 32.0 |  | 35 | 95.0 |
| 4 | 39.2 |  | 38 | 100.4 |
| 5 | 41.0 |  | 40 | 104.0 |
| 10 | 50.0 |  | 50 | 122.0 |
| 20 | 68.0 |  | 60 | 140.0 |

A temperature *difference* converts with ×9/5 only (a 10 K difference is an 18 °F difference). Do not add 32.

## Relative humidity and moisture content

- **Relative humidity (%RH)** is the same number in SI and US; there is nothing to convert. Always report it **with temperature** (for example 23 °C / 50 %RH), because RH alone does not fix the moisture in the air. Conditioning atmospheres are in `testing/`.
- **Moisture content (MC) of paper and board**: mills normally report the wet basis. Check which basis is used.

```
MC_wet = m_water / m_wet × 100 %
MC_dry = m_water / m_dry × 100 %
MC_dry = MC_wet / (1 − MC_wet)        MC_wet = MC_dry / (1 + MC_dry)
```

- `m_water`: mass of water (g) [oz]; `m_wet`: specimen mass before drying; `m_dry`: oven-dry mass.

Worked example: MC_wet = 7.0 % gives MC_dry = 0.07/0.93 = **7.527 %**. MC_wet = 10.0 % gives MC_dry = 11.11 %. MC_dry = 8.0 % gives MC_wet = 7.407 %. These ratios have no units, so SI and US are the same; in mass terms, a 100 g [3.527 oz] wet sample at 7.0 % wet basis holds 7.0 g [0.2469 oz] water. Limitation: equilibrium MC against RH depends on the furnish and the hysteresis direction. See `performance/` environmental factors.

## Acceleration, PSD and Grms (vibration)

```
1 g_n = 9.80665 m/s² = 386.0886 in/s² = 32.17405 ft/s²
1 g²/Hz = 96.17038 (m/s²)²/Hz
Grms = sqrt( ∫ PSD(f) df )          [g]
```

Segment area for a PSD line that is straight on log-log axes from (f1, P1) to (f2, P2):

```
m = ln(P2/P1) / ln(f2/f1)
A = P1 × f1 / (m + 1) × [ (f2/f1)^(m+1) − 1 ]      for m ≠ −1
A = P1 × f1 × ln(f2/f1)                             for m = −1
slope (dB/octave) = 10 × log10(2) × m = 3.0103 × m
```

- `f`: frequency (Hz); `PSD`, `P`: acceleration power spectral density (g²/Hz) [same in US practice]; `A`: area (g²); `Grms`: root-mean-square acceleration (g).

Worked example (illustrative profile, not a standard test profile): 0.001 g²/Hz at 10 Hz rising to 0.01 g²/Hz at 100 Hz (+3.01 dB/oct), flat 0.01 g²/Hz to 300 Hz, then falling to 0.001 g²/Hz at 500 Hz (−13.57 dB/oct).
- Segment areas: 0.495 + 2.000 + 0.7127 = 3.2077 g².
- Grms = √3.2077 = **1.791 g** = 17.56 m/s² (SI) = 691.5 in/s² (US).
- Check: a flat 0.01 g²/Hz from 10 to 500 Hz gives Grms = √(0.01 × 490) = 2.214 g (21.71 m/s²).

Limitations: Grms alone does not describe a vibration test, because profiles with the same Grms can damage packages differently. Use the PSD breakpoints of the standard (ISTA or ASTM D4169) itself. Take segment slopes from the actual profile.

## Conversion rules for the assistant

- Convert with the exact factors in this file. Round **only the final answer**, normally to 3–4 significant figures, or to the resolution of the source data.
- Give SI first with US in brackets, for example "5.60 kN/m [32.0 lbf/in]".
- State whether a value is a converted nominal (for example "32 ECT" means 32 lbf/in nominal) or a measured value.
- Never convert a test result between different *methods* (for example Mullen burst versus ISO 2759) as if the methods were equivalent.

## Research log

**Wave 3 (2026-11-09).** This agent used 21 searches, shared across six files.

Done this wave:
- The caliper "point" is now sourced: in US practice, caliper is given in thousandths of an inch
  or points [S3]. That matches `kb.materials.paperboard-carton` and the glossary.

Still open:
- Cross-check against NIST SP 811 Appendix B. nvlpubs.nist.gov, physics.nist.gov and www.nist.gov
  were all unreachable from this session. The factors themselves are exact by definition (1959
  yard-and-pound agreement and the CGPM value of g_n), so this only matters for a legal-metrology
  citation.
