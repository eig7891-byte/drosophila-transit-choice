"""
Tests for DrosophilaCommuteBrain and neuromodulator valence calculations.
"""
import pytest
import numpy as np
from src.core import (
    DrosophilaCommuteBrain,
    CommuteOption,
    InternalNeuromodulatorState,
    BrainWeights,
    CALIBRATED_BRAIN_WEIGHTS,
)

def test_brain_initialization(brain):
    """Brain initializes with valid weights and arrival target."""
    assert brain.target_arrival_hr == 9.0
    assert brain.weights.w_pam_money > 0.0
    assert brain.weights.w_ppl1_cost > 0.0
    assert brain.weights.fatigue_exponent > 1.0

def test_decision_structure(brain, standard_options, baseline_state):
    """Evaluation result contains valid options, probabilities, and winning choice."""
    res = brain.decide_commute(standard_options, baseline_state)
    assert "chosen_option" in res
    assert "chosen_mode" in res
    assert "probabilities" in res
    assert "evaluations" in res

    probs = res["probabilities"]
    assert len(probs) == len(standard_options)
    # Probabilities should sum to 1.0
    assert np.isclose(sum(probs.values()), 1.0, atol=1e-3)
    assert res["chosen_mode"] in probs

def test_student_prefers_transit(brain, standard_options, student_state):
    """High NPF (budget pressure) leads student archetype to strongly favor 50c transit over $28 car."""
    res = brain.decide_commute(standard_options, student_state)
    probs = res["probabilities"]
    assert probs["Transit_50c"] > probs["Car"]
    assert res["chosen_mode"] == "Transit_50c"

def test_executive_prefers_car(brain, executive_state):
    """Low NPF and high PDF (sleep debt) leads executive archetype to favor private driving when car is faster."""
    corridor_options = [
        CommuteOption("Car", travel_time_min=25.0, monetary_cost_aud=28.0, physical_effort=0.05, departure_time_hr=8.58, comfort_index=0.95),
        CommuteOption("Transit_50c", travel_time_min=45.0, monetary_cost_aud=1.0, physical_effort=0.15, departure_time_hr=8.25, comfort_index=0.75),
        CommuteOption("Bicycle", travel_time_min=50.0, monetary_cost_aud=2.0, physical_effort=0.85, departure_time_hr=8.16, comfort_index=0.45)
    ]
    res = brain.decide_commute(corridor_options, executive_state)
    probs = res["probabilities"]
    assert probs["Car"] > probs["Transit_50c"]
    assert res["chosen_mode"] == "Car"

def test_weather_heatwave_suppresses_cycling(brain, standard_options, baseline_state):
    """Severe heat index (0.90) increases physical fatigue aversion, lowering bicycle score."""
    res_cool = brain.decide_commute(standard_options, baseline_state, weather_heat_index=0.10)
    res_hot = brain.decide_commute(standard_options, baseline_state, weather_heat_index=0.90)

    eval_cool = {e["option_name"]: e for e in res_cool["evaluations"]}
    eval_hot = {e["option_name"]: e for e in res_hot["evaluations"]}

    bike_cool_valence = eval_cool["Bicycle"]["net_valence"]
    bike_hot_valence = eval_hot["Bicycle"]["net_valence"]

    assert bike_cool_valence > bike_hot_valence

def test_transit_productivity_boosts_transit(brain, standard_options, baseline_state):
    """Higher in-transit productivity increases positive reward for public transit."""
    res_low_prod = brain.decide_commute(standard_options, baseline_state, transit_productivity=0.1)
    res_high_prod = brain.decide_commute(standard_options, baseline_state, transit_productivity=0.9)

    eval_low = {e["option_name"]: e for e in res_low_prod["evaluations"]}
    eval_high = {e["option_name"]: e for e in res_high_prod["evaluations"]}

    pt_low = eval_low["Transit_50c"]["pam_reward_total"]
    pt_high = eval_high["Transit_50c"]["pam_reward_total"]

    assert pt_high > pt_low
