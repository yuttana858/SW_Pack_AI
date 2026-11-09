"""Golden tests: each test reproduces a worked example published in corpus/.

If a corpus example changes, the matching test must change in the same commit, so the
calculation library and the assistant's reference text can never disagree.
"""
import math

import pytest

from packcalc import board, compression as bct, dimensions as dim, stacking, units as u

# Shared example box: 400 x 300 mm RSC, C flute 4.0 mm, 32 ECT  (kb.performance.box-compression)
L, W = 400.0, 300.0
ECT32 = u.ect_us_to_si(32)           # 5.604 N/mm
DX_US, DY_US = 60.0, 30.0            # lbf·in, illustrative in the corpus
LBF_IN_TO_N_MM = u.LBF_TO_N * u.IN_TO_MM


def test_unit_constants():
    assert u.ect_us_to_si(1) == pytest.approx(0.175127, rel=1e-5)
    assert u.PSI_TO_KPA == pytest.approx(6.894757, rel=1e-6)
    assert u.LB_PER_MSF_TO_GSM == pytest.approx(4.882428, rel=1e-6)
    assert u.lbf_to_n(1) == pytest.approx(4.448222, rel=1e-6)


class TestMcKee:
    def test_simple_si(self):  # box-compression.md "Worked example — simplified McKee"
        r = bct.mckee_simple(ECT32, 4.0, L, W)
        assert r.value == pytest.approx(2462, abs=1)
        assert r.detail["perimeter_mm"] == 1400

    def test_simple_us(self):
        r = 5.87 * 32 * math.sqrt(0.1575 * 55.12)    # same homogeneous formula in US units
        assert r == pytest.approx(553, abs=1)
        assert u.n_to_lbf(bct.mckee_simple(ECT32, 4.0, L, W).value) == pytest.approx(553, abs=1)

    def test_tops_us(self):
        r = bct.mckee_tops(ECT32, 4.0, L, W)
        assert u.n_to_lbf(r.value) == pytest.approx(529, abs=1.5)

    def test_full_si_and_us(self):  # "Worked example — full McKee": 501 lbf / 2230 N
        r = bct.mckee_full(ECT32, DX_US * LBF_IN_TO_N_MM, DY_US * LBF_IN_TO_N_MM, L, W)
        assert r.value == pytest.approx(2230, abs=3)
        assert u.n_to_lbf(r.value) == pytest.approx(501, abs=1)

    def test_urbanik_frank(self):  # Urbanik–Frank refit: 466.5 lbf / 2075 N
        r = bct.urbanik_frank(ECT32, DX_US * LBF_IN_TO_N_MM, DY_US * LBF_IN_TO_N_MM, L, W)
        assert r.value == pytest.approx(2075, abs=3)
        assert u.n_to_lbf(r.value) == pytest.approx(466.5, abs=0.6)

    def test_short_box_warning(self):
        r = bct.mckee_simple(ECT32, 4.0, L, W, depth_mm=150)    # Z/7 = 200 mm
        assert any("short box" in w for w in r.warnings)

    def test_crushed_ratio(self):  # 4.0 -> 3.6 mm caliper
        assert bct.crushed_bct_ratio(4.0, 3.6).value == pytest.approx(math.sqrt(0.9))


class TestStacking:  # kb.performance.stacking-load-calc worked examples
    def test_column(self):
        assert stacking.top_load_column(6, 12).value == pytest.approx(588.4, abs=0.1)
        assert 5 * 26.46 == pytest.approx(132.3, abs=0.01)

    def test_pallets(self):
        r = stacking.top_load_pallets(layers=5, boxes_per_layer=8, pallets_high=2, box_mass_kg=12, pallet_mass_kg=25)
        assert r.value == pytest.approx(1089.8, abs=0.1)
        assert u.n_to_lbf(r.value) == pytest.approx(245.0, abs=0.1)

    def test_required_bct(self):
        r = stacking.bct_required(1089.8, multipliers=(0.55, 0.68))
        assert r.value == pytest.approx(2914, abs=1)
        r2 = stacking.bct_required(1089.8, multipliers=(0.55, 0.68, 0.80))
        assert r2.value == pytest.approx(3642, abs=1)

    def test_required_ect(self):
        r = bct.ect_required(2914, 4.0, L, W)
        assert r.value == pytest.approx(6.63, abs=0.01)
        assert u.ect_si_to_us(r.value) == pytest.approx(37.9, abs=0.1)

    def test_max_boxes_high(self):
        assert stacking.max_boxes_high(2462, 12, (0.55, 0.68)).value == 8

    def test_max_pallets_high(self):
        r = stacking.max_pallets_high(2462, 5, 8, 12, 25, (0.55, 0.68))
        assert r.value == 1

    def test_factors_and_sf_exclusive(self):
        with pytest.raises(ValueError):
            stacking.bct_required(100, multipliers=(0.5,), safety_factor=4)


class TestDimensions:  # kb.dimensional.* worked examples
    def test_basis_conversion(self):
        s = dim.convert_dims((400, 300, 250), "inside", "score", 4.0).value
        o = dim.convert_dims((400, 300, 250), "inside", "outside", 4.0).value
        assert s == (404, 304, 258) and o == (408, 308, 266)
        back = dim.convert_dims(o, "outside", "inside", 4.0).value
        assert back == (400, 300, 250)

    def test_rsc_blank_si(self):
        r = dim.rsc_blank((400, 300, 250), 4.0, 35).value
        assert r["blank_length_mm"] == pytest.approx(1451.0)
        assert r["blank_width_mm"] == pytest.approx(562.0)
        assert r["area_m2"] == pytest.approx(0.8155, abs=1e-4)

    def test_rsc_blank_us(self):  # inputs in inches, formula is unit-agnostic
        r = dim.rsc_blank((16, 12, 10), 5 / 32, 1.25).value
        assert r["blank_length_mm"] == pytest.approx(57.875)
        assert r["blank_width_mm"] == pytest.approx(22.469, abs=1e-3)

    def test_joint_warning(self):
        assert dim.rsc_blank((400, 300, 250), 4.0, 25).warnings


class TestBoard:
    def test_ect_from_sct_linear(self):
        r = board.ect_from_sct([3.0, 3.0], [2.0], [1.43])
        assert r.value == pytest.approx(0.7 * (6.0 + 1.43 * 2.0))

    def test_combined_grammage(self):
        assert board.combined_grammage([125, 125], [112], [1.43], 10).value == pytest.approx(420.16)
