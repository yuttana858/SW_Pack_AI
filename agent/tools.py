"""Tool definitions that expose packcalc and the data resolver to Claude.

`TOOLS` is a list of Messages-API tool definitions (name, description, input_schema, strict).
`dispatch(name, args)` runs a tool and returns a JSON-serialisable dict, including the formula
id, inputs, validity warnings and sources, so the assistant can show its working.

All lengths are mm, forces N, ECT N/mm (= kN/m), masses kg. The assistant converts US inputs
with the `convert_units` tool before calling a calculator.
"""
from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any, Callable

from packcalc import board, compression, dimensions, stacking, units
from swdata import Store

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _obj(props: dict, required: list[str]) -> dict:
    return {"type": "object", "properties": props, "required": required, "additionalProperties": False}


NUM = {"type": "number"}
DIMS = {"type": "array", "items": NUM, "minItems": 3, "maxItems": 3, "description": "[L, W, H] in mm"}
FACTORS = {"type": "array", "items": NUM, "description": "Environmental multipliers (each 0–1) from lib.factors.* records"}
OPT_NUM = {"type": ["number", "null"]}

TOOLS: list[dict[str, Any]] = [
    {"name": "convert_units", "strict": True,
     "description": "Convert a value between US and SI packaging units. kinds: length (in<->mm), force (lbf<->N), "
                    "ect (lbf/in<->N/mm), burst (psi<->kPa), basis_weight (lb/MSF<->g/m2), mass (lb<->kg).",
     "input_schema": _obj({"kind": {"type": "string", "enum": ["length", "force", "ect", "burst", "basis_weight", "mass"]},
                           "value": NUM, "to": {"type": "string", "enum": ["si", "us"]}}, ["kind", "value", "to"])},
    {"name": "convert_dimensions", "strict": True,
     "description": "Convert box dimensions [L, W, H] between inside, score and outside bases using caliper and "
                    "allowance factors. Omit factors (null) to use the resolved allowance table for the style.",
     "input_schema": _obj({"dims_mm": DIMS, "from_basis": {"type": "string", "enum": ["inside", "score", "outside"]},
                           "to_basis": {"type": "string", "enum": ["inside", "score", "outside"]}, "caliper_mm": NUM,
                           "k_s": {"type": ["array", "null"], "items": NUM}, "k_o": {"type": ["array", "null"], "items": NUM}},
                          ["dims_mm", "from_basis", "to_basis", "caliper_mm", "k_s", "k_o"])},
    {"name": "rsc_blank_size", "strict": True,
     "description": "FEFCO 0201 RSC blank length/width, flap length, score dimensions and board area from inside dimensions.",
     "input_schema": _obj({"inside_mm": DIMS, "caliper_mm": NUM, "joint_mm": NUM}, ["inside_mm", "caliper_mm", "joint_mm"])},
    {"name": "box_compression", "strict": True,
     "description": "Predict box compression strength (N). model: mckee_simple (needs caliper) or mckee_full / "
                    "urbanik_frank (need dx_n_mm, dy_n_mm bending stiffness). Returns validity warnings.",
     "input_schema": _obj({"model": {"type": "string", "enum": ["mckee_simple", "mckee_tops", "mckee_full", "urbanik_frank"]},
                           "ect_n_per_mm": NUM, "length_mm": NUM, "width_mm": NUM, "depth_mm": OPT_NUM,
                           "caliper_mm": OPT_NUM, "dx_n_mm": OPT_NUM, "dy_n_mm": OPT_NUM},
                          ["model", "ect_n_per_mm", "length_mm", "width_mm", "depth_mm", "caliper_mm", "dx_n_mm", "dy_n_mm"])},
    {"name": "stacking_requirement", "strict": True,
     "description": "Top load on the bottom box (single column or pallets stacked), required BCT after environmental "
                    "multipliers, and required ECT for a given caliper and footprint.",
     "input_schema": _obj({"box_mass_kg": NUM, "boxes_high": {"type": ["integer", "null"]},
                           "layers": {"type": ["integer", "null"]}, "boxes_per_layer": {"type": ["integer", "null"]},
                           "pallets_high": {"type": ["integer", "null"]}, "pallet_mass_kg": OPT_NUM,
                           "multipliers": FACTORS, "caliper_mm": NUM, "length_mm": NUM, "width_mm": NUM},
                          ["box_mass_kg", "boxes_high", "layers", "boxes_per_layer", "pallets_high", "pallet_mass_kg",
                           "multipliers", "caliper_mm", "length_mm", "width_mm"])},
    {"name": "ect_from_papers", "strict": True,
     "description": "Estimate combined-board ECT (N/mm) from liner and medium SCT (CD, N/mm) and take-up factors.",
     "input_schema": _obj({"sct_liners": {"type": "array", "items": NUM}, "sct_mediums": {"type": "array", "items": NUM},
                           "take_ups": {"type": "array", "items": NUM}}, ["sct_liners", "sct_mediums", "take_ups"])},
    {"name": "lookup_record", "strict": True,
     "description": "Find the governing data record (most specific approved scope wins: machine > plant > company > library) "
                    "for a record type, optionally filtered by a field value. Returns the record and why it was chosen.",
     "input_schema": _obj({"record_type": {"type": "string", "enum": ["allowance_table", "board_material", "flute_profile", "grade_table",
                                                    "factor_set", "formula", "box_style", "tolerance_spec", "machine_spec", "plant"]},
                           "filter_key": {"type": ["string", "null"], "description": "dotted path, e.g. flute.code or factors.kind"},
                           "filter_value": {"type": ["string", "null"]},
                           "plant": {"type": ["string", "null"]}, "machine": {"type": ["string", "null"]},
                           "approved_only": {"type": "boolean"}},
                          ["record_type", "filter_key", "filter_value", "plant", "machine", "approved_only"])},
]


def _res(r) -> dict:
    d = dataclasses.asdict(r)
    d["warnings"] = list(r.warnings)
    return d


def _convert_units(kind: str, value: float, to: str) -> dict:
    f = {"length": units.IN_TO_MM, "force": units.LBF_TO_N, "ect": units.LBF_PER_IN_TO_N_PER_MM,
         "burst": units.PSI_TO_KPA, "basis_weight": units.LB_PER_MSF_TO_GSM, "mass": units.LB_TO_KG}[kind]
    names = {"length": ("in", "mm"), "force": ("lbf", "N"), "ect": ("lbf/in", "N/mm"), "burst": ("psi", "kPa"),
             "basis_weight": ("lb/MSF", "g/m2"), "mass": ("lb", "kg")}[kind]
    return {"value": value * f if to == "si" else value / f, "unit": names[1] if to == "si" else names[0], "factor": f}


def _get(d: dict, path: str):
    for k in path.split("."):
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def _lookup(record_type, filter_key, filter_value, plant, machine, approved_only, store: Store | None = None) -> dict:
    store = store or Store.from_dir(DATA_DIR)
    match = (lambda r: str(_get(r, filter_key)) == str(filter_value)) if filter_key else (lambda r: True)
    r = store.resolve(record_type, match, plant=plant, machine=machine,
                      min_status="approved" if approved_only else "draft")
    out = {"found": r.found, "explanation": r.explain(), "record": r.record}
    if r.found and r.record["status"] != "approved":
        out["warning"] = "record is not approved; tell the engineer the value is unreviewed"
    return out


def _stacking(box_mass_kg, boxes_high, layers, boxes_per_layer, pallets_high, pallet_mass_kg, multipliers,
              caliper_mm, length_mm, width_mm) -> dict:
    if boxes_high:
        load = stacking.top_load_column(boxes_high, box_mass_kg)
    else:
        load = stacking.top_load_pallets(layers, boxes_per_layer, pallets_high, box_mass_kg, pallet_mass_kg or 0.0)
    req = stacking.bct_required(load.value, multipliers=tuple(multipliers))
    ect = compression.ect_required(req.value, caliper_mm, length_mm, width_mm)
    return {"top_load": _res(load), "bct_required": _res(req), "ect_required": _res(ect)}


HANDLERS: dict[str, Callable[..., dict]] = {
    "convert_units": _convert_units,
    "convert_dimensions": lambda dims_mm, from_basis, to_basis, caliper_mm, k_s, k_o: _res(dimensions.convert_dims(
        dims_mm, from_basis, to_basis, caliper_mm, k_s or dimensions.RSC_K_S, k_o or dimensions.RSC_K_O)),
    "rsc_blank_size": lambda inside_mm, caliper_mm, joint_mm: _res(dimensions.rsc_blank(inside_mm, caliper_mm, joint_mm)),
    "box_compression": lambda model, ect_n_per_mm, length_mm, width_mm, depth_mm, caliper_mm, dx_n_mm, dy_n_mm: _res(
        getattr(compression, model)(ect_n_per_mm, caliper_mm, length_mm, width_mm, depth_mm)
        if model in ("mckee_simple", "mckee_tops")
        else getattr(compression, model)(ect_n_per_mm, dx_n_mm, dy_n_mm, length_mm, width_mm, depth_mm)),
    "stacking_requirement": _stacking,
    "ect_from_papers": lambda sct_liners, sct_mediums, take_ups: _res(board.ect_from_sct(sct_liners, sct_mediums, take_ups)),
    "lookup_record": _lookup,
}


def dispatch(name: str, args: dict[str, Any]) -> dict:
    """Run a tool. Errors come back as {'error': ...} so the caller can return an is_error tool_result."""
    if name not in HANDLERS:
        return {"error": f"unknown tool {name}"}
    try:
        return HANDLERS[name](**args)
    except (TypeError, ValueError, KeyError) as e:
        return {"error": f"{type(e).__name__}: {e}"}
