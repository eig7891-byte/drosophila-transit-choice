"""
Pytest configuration and fixtures for Drosophila Transit Choice test suite.
"""
import pytest
import numpy as np
import os
import sys

# Ensure repository root is on sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.core import (
    DrosophilaCommuteBrain,
    CommuteOption,
    InternalNeuromodulatorState,
    BrainWeights,
    PRIOR_BRAIN_WEIGHTS,
    CALIBRATED_BRAIN_WEIGHTS,
)
from src.simulation import BrisbaneTransitSimulator, BRISBANE_CORRIDORS

@pytest.fixture
def baseline_state():
    """Returns a neutral neuromodulator state (0.5 across all axes)."""
    return InternalNeuromodulatorState(
        npf_hunger=0.5,
        octopamine_vigor=0.5,
        serotonin_patience=0.5,
        pdf_sleep_debt=0.5
    )

@pytest.fixture
def student_state():
    """Returns a student archetype neuromodulator state (high hunger/budget pressure)."""
    return InternalNeuromodulatorState(
        npf_hunger=0.95,
        octopamine_vigor=0.30,
        serotonin_patience=0.65,
        pdf_sleep_debt=0.40
    )

@pytest.fixture
def executive_state():
    """Returns an executive archetype neuromodulator state (low hunger, high sleep debt)."""
    return InternalNeuromodulatorState(
        npf_hunger=0.10,
        octopamine_vigor=0.25,
        serotonin_patience=0.20,
        pdf_sleep_debt=0.90
    )

@pytest.fixture
def standard_options():
    """Returns standard three-choice set (Car, Transit_50c, Bicycle)."""
    return [
        CommuteOption(
            name="Car",
            travel_time_min=35.0,
            monetary_cost_aud=28.0,
            physical_effort=0.05,
            departure_time_hr=8.41,
            comfort_index=0.95
        ),
        CommuteOption(
            name="Transit_50c",
            travel_time_min=45.0,
            monetary_cost_aud=1.0,
            physical_effort=0.15,
            departure_time_hr=8.25,
            comfort_index=0.75
        ),
        CommuteOption(
            name="Bicycle",
            travel_time_min=50.0,
            monetary_cost_aud=2.0,
            physical_effort=0.85,
            departure_time_hr=8.16,
            comfort_index=0.45
        )
    ]

@pytest.fixture
def brain():
    """Returns a calibrated DrosophilaCommuteBrain."""
    return DrosophilaCommuteBrain(target_arrival_hr=9.0)
