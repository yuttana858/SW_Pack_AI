"""Combined-board property estimates (corpus/performance/board-tests-and-ect.md, materials/flutes.md)."""
from __future__ import annotations

from typing import Sequence

from .result import Result


def ect_from_sct(sct_liners_n_per_mm: Sequence[float], sct_mediums_n_per_mm: Sequence[float],
                 take_ups: Sequence[float], c: float = 0.7) -> Result:
    """ECT ≈ C · (Σ SCT_liner + Σ α_i · SCT_medium_i), CD values, N/mm. C ≈ 0.7 (fitted 0.695–0.766)."""
    if len(sct_mediums_n_per_mm) != len(take_ups):
        raise ValueError("one take-up factor per medium")
    s = sum(sct_liners_n_per_mm) + sum(a * m for a, m in zip(take_ups, sct_mediums_n_per_mm))
    w = ["empirical estimate; check against measured ECT (TAPPI T 839 / ISO 3037)"]
    if not 0.6 <= c <= 0.8:
        w.append("C outside the 0.695–0.766 range fitted in the literature")
    return Result(c * s, "N/mm", "lib.formula.ect-from-sct",
                  {"sct_liners": tuple(sct_liners_n_per_mm), "sct_mediums": tuple(sct_mediums_n_per_mm),
                   "take_ups": tuple(take_ups), "c": c}, tuple(w), ("kb.performance.board-tests-and-ect",))


def combined_grammage(liners_gsm: Sequence[float], mediums_gsm: Sequence[float], take_ups: Sequence[float],
                      adhesive_gsm: float = 0.0) -> Result:
    """Combined basis weight = Σ liners + Σ (medium × take-up) + adhesive."""
    if len(mediums_gsm) != len(take_ups):
        raise ValueError("one take-up factor per medium")
    g = sum(liners_gsm) + sum(m * a for m, a in zip(mediums_gsm, take_ups)) + adhesive_gsm
    return Result(g, "g/m2", "lib.formula.combined-grammage",
                  {"liners_gsm": tuple(liners_gsm), "mediums_gsm": tuple(mediums_gsm), "take_ups": tuple(take_ups),
                   "adhesive_gsm": adhesive_gsm}, (), ("kb.materials.flutes",))
