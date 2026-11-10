"""Dimension bases and blank sizes (corpus/dimensional/*).

Convention (matches Auto3D board records and data/library/allowances):
    score   = inside + k_s * t
    outside = inside + k_o * t
per axis [L, W, H], t = combined board caliper. RSC defaults k_s = [1, 1, 2], k_o = [2, 2, 4].
"""
from __future__ import annotations

from typing import Sequence

from .result import Result

RSC_K_S = (1.0, 1.0, 2.0)
RSC_K_O = (2.0, 2.0, 4.0)
BASES = ("inside", "score", "outside")
SRC = ("kb.dimensional.dimensions-and-allowances",)


def convert_dims(
    dims: Sequence[float],
    from_basis: str,
    to_basis: str,
    caliper_mm: float,
    k_s: Sequence[float] = RSC_K_S,
    k_o: Sequence[float] = RSC_K_O,
) -> Result:
    """Convert [L, W, H] between inside, score and outside bases."""
    if from_basis not in BASES or to_basis not in BASES:
        raise ValueError(f"basis must be one of {BASES}")
    if len(dims) != 3 or len(k_s) != 3 or len(k_o) != 3:
        raise ValueError("dims, k_s and k_o must each have 3 values [L, W, H]")
    if caliper_mm <= 0:
        raise ValueError("caliper_mm must be > 0")
    if any(o < s for s, o in zip(k_s, k_o)):
        raise ValueError("k_o must be >= k_s on every axis")
    offset = {"inside": (0.0, 0.0, 0.0), "score": tuple(k_s), "outside": tuple(k_o)}
    out = [d - offset[from_basis][i] * caliper_mm + offset[to_basis][i] * caliper_mm for i, d in enumerate(dims)]
    warnings = []
    if min(out) <= 0:
        warnings.append("result has a non-positive dimension; check inputs and basis")
    return Result(
        value=tuple(round(x, 6) for x in out),
        unit="mm",
        formula="lib.formula.dimension-basis",
        inputs={"dims": tuple(dims), "from": from_basis, "to": to_basis, "caliper_mm": caliper_mm, "k_s": tuple(k_s), "k_o": tuple(k_o)},
        warnings=tuple(warnings),
        sources=SRC,
    )


def rsc_blank(
    inside_mm: Sequence[float],
    caliper_mm: float,
    joint_mm: float,
    k_s: Sequence[float] = RSC_K_S,
    flap_allowance_mm: float = 0.0,
) -> Result:
    """FEFCO 0201 RSC blank: BL = 2Ls + 2Ws + J, BW = Hs + 2F, F = Ws/2 + a."""
    L, W, H = inside_mm
    Ls, Ws, Hs = (d + k * caliper_mm for d, k in zip((L, W, H), k_s))
    F = Ws / 2 + flap_allowance_mm
    BL = 2 * Ls + 2 * Ws + joint_mm
    BW = Hs + 2 * F
    warnings = []
    if joint_mm < 32:
        warnings.append("manufacturer's joint below the 32 mm (1 1/4 in) minimum for single/double wall")
    if L < W:
        warnings.append("FEFCO convention: length should be >= width")
    return Result(
        value={"blank_length_mm": BL, "blank_width_mm": BW, "flap_mm": F,
               "score_mm": (Ls, Ws, Hs), "area_m2": BL * BW / 1e6},
        unit="mm",
        formula="lib.formula.rsc-blank",
        inputs={"inside_mm": tuple(inside_mm), "caliper_mm": caliper_mm, "joint_mm": joint_mm,
                "k_s": tuple(k_s), "flap_allowance_mm": flap_allowance_mm},
        warnings=tuple(warnings),
        sources=("kb.dimensional.blank-size-formulas",),
    )
