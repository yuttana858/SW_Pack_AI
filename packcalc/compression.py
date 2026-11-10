"""Box compression strength (BCT) models (corpus/performance/box-compression.md).

All models are dimensionally homogeneous, so the constants are unit-free; inputs must be a
consistent set. These functions take SI: ECT in N/mm (= kN/m), lengths in mm, bending stiffness
in N·mm (= N·mm²/mm). Results in N.
"""
from __future__ import annotations

import math

from .result import Result

SRC = ("kb.performance.box-compression",)


def perimeter_mm(length_mm: float, width_mm: float) -> float:
    return 2 * (length_mm + width_mm)


def _geometry_warnings(length_mm, width_mm, depth_mm) -> list[str]:
    w = []
    z = perimeter_mm(length_mm, width_mm)
    if depth_mm is not None and depth_mm < z / 7:
        w.append("short box: depth < Z/7, McKee is outside its validity (short-box form BCT ≈ C'·ECT·Z applies)")
    if width_mm > 0 and length_mm / width_mm > 2:
        w.append("length/width > 2: McKee assumes a near-square footprint; expect larger error")
    return w


def mckee_simple(ect_n_per_mm: float, caliper_mm: float, length_mm: float, width_mm: float,
                 depth_mm: float | None = None) -> Result:
    """BCT = 5.87 · ECT · sqrt(h · Z)."""
    z = perimeter_mm(length_mm, width_mm)
    bct = 5.87 * ect_n_per_mm * math.sqrt(caliper_mm * z)
    w = _geometry_warnings(length_mm, width_mm, depth_mm)
    w.append("McKee over-predicts single-wall BCT by about 7.6 % on average (Urbanik & Frank 2006); confirm by ASTM D642 / ISO 12048 test")
    return Result(bct, "N", "lib.formula.mckee-simple",
                  {"ect_n_per_mm": ect_n_per_mm, "caliper_mm": caliper_mm, "length_mm": length_mm,
                   "width_mm": width_mm, "depth_mm": depth_mm}, tuple(w), SRC, {"perimeter_mm": z})


def mckee_tops(ect_n_per_mm: float, caliper_mm: float, length_mm: float, width_mm: float,
               depth_mm: float | None = None) -> Result:
    """TOPS variant: BCT = 5.87 · ECT · Z^0.4924 · h^0.5076."""
    z = perimeter_mm(length_mm, width_mm)
    bct = 5.87 * ect_n_per_mm * z ** 0.4924 * caliper_mm ** 0.5076
    return Result(bct, "N", "lib.formula.mckee-tops",
                  {"ect_n_per_mm": ect_n_per_mm, "caliper_mm": caliper_mm, "length_mm": length_mm,
                   "width_mm": width_mm, "depth_mm": depth_mm},
                  tuple(_geometry_warnings(length_mm, width_mm, depth_mm)), SRC, {"perimeter_mm": z})


def _stiffness_model(a: float, b: float, ect_n_per_mm: float, dx_n_mm: float, dy_n_mm: float, z_mm: float) -> float:
    return a * ect_n_per_mm ** b * math.sqrt(dx_n_mm * dy_n_mm) ** (1 - b) * z_mm ** (2 * b - 1)


def mckee_full(ect_n_per_mm: float, dx_n_mm: float, dy_n_mm: float, length_mm: float, width_mm: float,
               depth_mm: float | None = None) -> Result:
    """BCT = 2.028 · ECT^0.746 · sqrt(Dx·Dy)^0.254 · Z^0.492 (Dx, Dy bending stiffness per width, N·mm)."""
    z = perimeter_mm(length_mm, width_mm)
    bct = _stiffness_model(2.028, 0.746, ect_n_per_mm, dx_n_mm, dy_n_mm, z)
    return Result(bct, "N", "lib.formula.mckee-full",
                  {"ect_n_per_mm": ect_n_per_mm, "dx_n_mm": dx_n_mm, "dy_n_mm": dy_n_mm,
                   "length_mm": length_mm, "width_mm": width_mm, "depth_mm": depth_mm},
                  tuple(_geometry_warnings(length_mm, width_mm, depth_mm)), SRC, {"perimeter_mm": z})


def urbanik_frank(ect_n_per_mm: float, dx_n_mm: float, dy_n_mm: float, length_mm: float, width_mm: float,
                  depth_mm: float | None = None, wall: str = "single") -> Result:
    """Urbanik & Frank (2006) refit of the McKee form: a = 2.186, b = 0.727."""
    z = perimeter_mm(length_mm, width_mm)
    bct = _stiffness_model(2.186, 0.727, ect_n_per_mm, dx_n_mm, dy_n_mm, z)
    w = _geometry_warnings(length_mm, width_mm, depth_mm)
    if wall != "single":
        w.append("Urbanik–Frank refit is fitted to single-wall RSCs only; not validated for double wall")
    return Result(bct, "N", "lib.formula.urbanik-frank",
                  {"ect_n_per_mm": ect_n_per_mm, "dx_n_mm": dx_n_mm, "dy_n_mm": dy_n_mm,
                   "length_mm": length_mm, "width_mm": width_mm, "depth_mm": depth_mm, "wall": wall},
                  tuple(w), SRC, {"perimeter_mm": z})


def ect_required(bct_required_n: float, caliper_mm: float, length_mm: float, width_mm: float) -> Result:
    """Reverse simplified McKee: ECT = BCT / (5.87 · sqrt(h · Z)). Result in N/mm (= kN/m)."""
    z = perimeter_mm(length_mm, width_mm)
    ect = bct_required_n / (5.87 * math.sqrt(caliper_mm * z))
    return Result(ect, "N/mm", "lib.formula.ect-required",
                  {"bct_required_n": bct_required_n, "caliper_mm": caliper_mm,
                   "length_mm": length_mm, "width_mm": width_mm},
                  ("BCT_required must already include environmental factors / safety factor",
                   "choose the next standard grade up, then re-check with that grade's real caliper"),
                  SRC, {"perimeter_mm": z})


def crushed_bct_ratio(caliper_original_mm: float, caliper_crushed_mm: float) -> Result:
    """BCT_crushed / BCT_original = sqrt(h_crushed / h_original), ECT held constant."""
    r = math.sqrt(caliper_crushed_mm / caliper_original_mm)
    return Result(r, "-", "lib.formula.crushed-bct-ratio",
                  {"caliper_original_mm": caliper_original_mm, "caliper_crushed_mm": caliper_crushed_mm},
                  ("assumes ECT unchanged; crushing usually also lowers bending stiffness",),
                  ("kb.performance.board-tests-and-ect",))
