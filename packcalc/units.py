"""Exact unit conversion constants (see corpus/reference/units-and-conversions.md).

packcalc works in SI internally: mm, N, N/mm (= kN/m), kPa, kg, g/m².
Convert at the edges with these constants.
"""
G = 9.80665                      # m/s², standard gravity (exact)
IN_TO_MM = 25.4                  # exact
LBF_TO_N = 4.4482216152605       # exact (international avoirdupois pound × g)
LB_TO_KG = 0.45359237            # exact
LBF_PER_IN_TO_N_PER_MM = LBF_TO_N / IN_TO_MM       # 0.17512684... (ECT lbf/in -> kN/m)
PSI_TO_KPA = LBF_TO_N / (IN_TO_MM ** 2) * 1000     # 6.894757...
LB_PER_MSF_TO_GSM = LB_TO_KG * 1000 / (1000 * (0.3048 ** 2))  # 4.882428...
POINT_TO_MM = 0.0254             # 1 caliper point = 0.001 in


def in_to_mm(x: float) -> float:
    return x * IN_TO_MM


def mm_to_in(x: float) -> float:
    return x / IN_TO_MM


def lbf_to_n(x: float) -> float:
    return x * LBF_TO_N


def n_to_lbf(x: float) -> float:
    return x / LBF_TO_N


def ect_us_to_si(lbf_per_in: float) -> float:
    """ECT lbf/in -> N/mm (= kN/m)."""
    return lbf_per_in * LBF_PER_IN_TO_N_PER_MM


def ect_si_to_us(n_per_mm: float) -> float:
    return n_per_mm / LBF_PER_IN_TO_N_PER_MM
