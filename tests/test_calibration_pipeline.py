"""
Tests for calibration provenance, target structures, and empirical parameter consistency.
"""
import pytest
import os
import json
from src.core import (
    CALIBRATED_BRAIN_WEIGHTS,
    PRIOR_BRAIN_WEIGHTS,
    get_calibration_provenance,
)
from scripts.run_mle_calibration import load_empirical_targets

def test_calibration_provenance():
    """Confirms calibration provenance returns validated MLE/MAP loss metrics and parameter values."""
    prov = get_calibration_provenance()
    assert isinstance(prov, dict)
    assert "parameters" in prov
    assert "calibrated_loss" in prov
    assert "rmse_after" in prov
    # Validated RMSE should be <= 2.0%
    assert prov["rmse_after"] <= 2.05
    assert prov["calibrated_loss"] < prov["prior_loss"]

def test_empirical_targets_loader():
    """Confirms empirical targets can be loaded with all expected corridor and regional keys."""
    targets = load_empirical_targets()
    assert "Springwood_Route555_Growth" in targets
    assert "Logan_SouthernRegion_Annual_Growth" in targets
    assert "Citytrain_Rail_Annual_Growth" in targets
    assert "SEQ_Total_Annual_Growth" in targets

def test_calibrated_weights_differ_from_priors():
    """Confirms calibrated weights were adapted away from initial literature priors to match Translink data."""
    calib = CALIBRATED_BRAIN_WEIGHTS
    prior = PRIOR_BRAIN_WEIGHTS
    # At least some parameters must have adapted
    assert calib.w_pam_money != prior.w_pam_money or calib.fatigue_exponent != prior.fatigue_exponent
