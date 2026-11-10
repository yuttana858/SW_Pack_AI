"""Result object returned by every packcalc formula.

The assistant reports `value`, `unit`, the `formula` id, the inputs, and every warning.
Warnings flag inputs outside a formula's validity range; they never block the calculation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Result:
    value: Any
    unit: str
    formula: str                      # formula registry id, e.g. "lib.formula.mckee-simple"
    inputs: dict[str, Any]
    warnings: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()     # corpus refs, e.g. "kb.performance.box-compression"
    detail: dict[str, Any] = field(default_factory=dict)

    def __float__(self) -> float:
        return float(self.value)
