import json

import pytest

from agent.tools import TOOLS, dispatch


def test_every_tool_has_a_handler_and_valid_schema():
    names = {t["name"] for t in TOOLS}
    for t in TOOLS:
        s = t["input_schema"]
        assert s["additionalProperties"] is False
        assert set(s["required"]) == set(s["properties"]), f"{t['name']}: strict tools need every property required"
        assert dispatch(t["name"], {}).get("error"), "missing args must return an error, not raise"
    assert len(names) == len(TOOLS)


def test_box_compression_tool_matches_golden():
    out = dispatch("box_compression", {"model": "mckee_simple", "ect_n_per_mm": 5.604, "length_mm": 400, "width_mm": 300,
                                       "depth_mm": 300, "caliper_mm": 4.0, "dx_n_mm": None, "dy_n_mm": None})
    assert out["value"] == pytest.approx(2462, abs=1) and out["formula"] == "lib.formula.mckee-simple"
    json.dumps(out)


def test_stacking_tool_chain():
    out = dispatch("stacking_requirement", {"box_mass_kg": 12, "boxes_high": None, "layers": 5, "boxes_per_layer": 8,
                                            "pallets_high": 2, "pallet_mass_kg": 25, "multipliers": [0.55, 0.68],
                                            "caliper_mm": 4.0, "length_mm": 400, "width_mm": 300})
    assert out["bct_required"]["value"] == pytest.approx(2914, abs=1)
    assert out["ect_required"]["value"] == pytest.approx(6.63, abs=0.01)


def test_units_and_lookup():
    assert dispatch("convert_units", {"kind": "ect", "value": 32, "to": "si"})["value"] == pytest.approx(5.604, abs=1e-3)
    out = dispatch("lookup_record", {"record_type": "formula", "filter_key": "id", "filter_value": "lib.formula.rsc-blank",
                                     "plant": None, "machine": None, "approved_only": False})
    assert out["found"] and "warning" in out
