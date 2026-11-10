"""Stacking loads and required BCT (corpus/performance/stacking-load-calc.md). SI: kg, N."""
from __future__ import annotations

import math
from typing import Sequence

from .result import Result
from .units import G

SRC = ("kb.performance.stacking-load-calc",)


def top_load_column(boxes_high: int, box_mass_kg: float) -> Result:
    """F_top = (n − 1) · m · g on the bottom box of a single column."""
    if boxes_high < 1:
        raise ValueError("boxes_high must be >= 1")
    f = (boxes_high - 1) * box_mass_kg * G
    return Result(f, "N", "lib.formula.top-load-column", {"boxes_high": boxes_high, "box_mass_kg": box_mass_kg},
                  ("static load only; no dynamic, no load sharing, box carries all load",), SRC)


def top_load_pallets(layers: int, boxes_per_layer: int, pallets_high: int, box_mass_kg: float,
                     pallet_mass_kg: float) -> Result:
    """F_top = [(L−1)·m + (P−1)·(L·k·m + m_p)/k] · g on a bottom-layer box of the bottom pallet."""
    own = (layers - 1) * box_mass_kg
    per_upper = (layers * boxes_per_layer * box_mass_kg + pallet_mass_kg) / boxes_per_layer
    f = (own + (pallets_high - 1) * per_upper) * G
    return Result(f, "N", "lib.formula.top-load-pallets",
                  {"layers": layers, "boxes_per_layer": boxes_per_layer, "pallets_high": pallets_high,
                   "box_mass_kg": box_mass_kg, "pallet_mass_kg": pallet_mass_kg},
                  ("assumes rigid deck, no deckboard-gap concentration, no overhang, column-stacked layers",),
                  SRC, {"own_pallet_kg": own, "per_upper_pallet_kg": per_upper})


def bct_required(top_load_n: float, multipliers: Sequence[float] = (), safety_factor: float | None = None) -> Result:
    """BCT_required = F_top / Π m_i  (or F_top × SF when a single safety factor is used instead)."""
    if multipliers and safety_factor:
        raise ValueError("use either environmental multipliers or a safety factor, not both")
    if safety_factor:
        req, product = top_load_n * safety_factor, None
    else:
        product = math.prod(multipliers) if multipliers else 1.0
        if not 0 < product <= 1:
            raise ValueError("product of multipliers must be in (0, 1]")
        req = top_load_n / product
    w = [] if (multipliers or safety_factor) else ["no environmental factors or safety factor applied"]
    return Result(req, "N", "lib.formula.bct-required",
                  {"top_load_n": top_load_n, "multipliers": tuple(multipliers), "safety_factor": safety_factor},
                  tuple(w), SRC, {"multiplier_product": product})


def max_boxes_high(bct_n: float, box_mass_kg: float, multipliers: Sequence[float] = ()) -> Result:
    """n_max = floor(BCT·Πm / (m·g)) + 1, rounded down."""
    allowable = bct_n * (math.prod(multipliers) if multipliers else 1.0)
    n = math.floor(allowable / (box_mass_kg * G)) + 1
    return Result(n, "boxes", "lib.formula.max-boxes-high",
                  {"bct_n": bct_n, "box_mass_kg": box_mass_kg, "multipliers": tuple(multipliers)},
                  ("confirm by test; McKee BCT tends to over-predict",), SRC, {"allowable_load_n": allowable})


def max_pallets_high(bct_n: float, layers: int, boxes_per_layer: int, box_mass_kg: float,
                     pallet_mass_kg: float, multipliers: Sequence[float] = ()) -> Result:
    """P_max = floor((BCT·Πm − (L−1)·m·g) / ((L·k·m + m_p)·g/k)) + 1; 0 means one pallet already overloads."""
    allowable = bct_n * (math.prod(multipliers) if multipliers else 1.0)
    own = (layers - 1) * box_mass_kg * G
    per_upper = (layers * boxes_per_layer * box_mass_kg + pallet_mass_kg) * G / boxes_per_layer
    w = ["confirm by test; McKee BCT tends to over-predict"]
    if allowable < own:
        p = 0
        w.insert(0, "a single pallet already exceeds the allowable load on the bottom box")
    else:
        p = math.floor((allowable - own) / per_upper) + 1
    return Result(p, "pallets", "lib.formula.max-pallets-high",
                  {"bct_n": bct_n, "layers": layers, "boxes_per_layer": boxes_per_layer, "box_mass_kg": box_mass_kg,
                   "pallet_mass_kg": pallet_mass_kg, "multipliers": tuple(multipliers)},
                  tuple(w), SRC, {"allowable_load_n": allowable, "own_pallet_load_n": own, "per_upper_pallet_n": per_upper})
