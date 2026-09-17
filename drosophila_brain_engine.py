"""
Legacy alias forwarding to src.core for backward compatibility.
"""
from src.core import (
    InternalNeuromodulatorState,
    BrainWeights,
    PRIOR_BRAIN_WEIGHTS,
    CALIBRATED_BRAIN_WEIGHTS,
    get_calibration_provenance,
    CommuteOption,
    DrosophilaCommuteBrain,
)

__all__ = [
    "InternalNeuromodulatorState",
    "BrainWeights",
    "PRIOR_BRAIN_WEIGHTS",
    "CALIBRATED_BRAIN_WEIGHTS",
    "get_calibration_provenance",
    "CommuteOption",
    "DrosophilaCommuteBrain",
]