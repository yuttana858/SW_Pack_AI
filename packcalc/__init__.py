"""packcalc: tested packaging-engineering calculations for SW Pack AI.

Every function returns a `Result` carrying the value, unit, formula id, inputs, validity
warnings and corpus sources. The assistant must call these instead of doing arithmetic itself.
"""
from . import board, compression, dimensions, stacking, units
from .result import Result

__all__ = ["Result", "board", "compression", "dimensions", "stacking", "units"]
__version__ = "0.1.0"
