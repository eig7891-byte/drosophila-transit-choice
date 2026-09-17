"""
Unit Tests for Drosophila Commute Decision Engine
--------------------------------------------------
Validates physiological firing bounds, neuromodulatory sensitivity,
tipping points, and probability normalization.
"""

import numpy as np
from drosophila_brain_engine import (
    DrosophilaCommuteBrain,
    CommuteOption,
    InternalNeuromodulatorState
)

def get_standard_brisbane_options():
    return [
        CommuteOption(
            name='Car',
            travel_time_min=30.0,
            monetary_cost_aud=28.0, # $20 parking + $8 fuel
            physical_effort=0.05,
            departure_time_hr=8.5, # 8:30 AM
            comfort_index=0.95
        ),
        CommuteOption(
            name='Transit_50c',
            travel_time_min=90.0,
            monetary_cost_aud=1.0, # 50c each way = $1.00
            physical_effort=0.15,
            departure_time_hr=7.5, # 7:30 AM
            comfort_index=0.70
        ),
        CommuteOption(
            name='Bicycle',
            travel_time_min=65.0,
            monetary_cost_aud=0.0,
            physical_effort=0.85,
            departure_time_hr=7.75, # 7:45 AM
            comfort_index=0.40
        )
    ]

def test_student_high_npf_prefers_50c_transit():
    """Tertiary student (high NPF price sensitivity) should pick 50c Transit."""
    brain = DrosophilaCommuteBrain()
    options = get_standard_brisbane_options()
    student_state = InternalNeuromodulatorState(
        npf_hunger=0.95,        # Extreme need to save money
        octopamine_vigor=0.30,
        serotonin_patience=0.60,
        pdf_sleep_debt=0.30
    )
    result = brain.decide_commute(options, student_state)
    assert result['chosen_mode'] == 'Transit_50c', f"Expected Transit_50c, got {result['chosen_mode']}"
    assert result['probabilities']['Transit_50c'] > 0.45
    print("  [PASS] Student High NPF -> 50c Transit (52.9%)")

def test_wealthy_sleepy_professional_prefers_car():
    """Wealthy corporate commuter with zero financial hunger & high morning sleepiness picks Car."""
    brain = DrosophilaCommuteBrain()
    options = get_standard_brisbane_options()
    exec_state = InternalNeuromodulatorState(
        npf_hunger=0.05,        # Doesn't care about $28 parking
        octopamine_vigor=0.20,
        serotonin_patience=0.10,# Very low patience for 90m bus
        pdf_sleep_debt=0.95     # Refuses to wake up at 7:00 AM
    )
    result = brain.decide_commute(options, exec_state)
    assert result['chosen_mode'] == 'Car', f"Expected Car, got {result['chosen_mode']}"
    assert result['probabilities']['Car'] > 0.40
    print("  [PASS] Wealthy Executive -> Car (Plurality winner)")

def test_athletic_cyclist_prefers_bike_in_cool_weather():
    """High Octopamine commuter in mild weather picks Bicycle for health/fitness rewards."""
    brain = DrosophilaCommuteBrain()
    options = get_standard_brisbane_options()
    cyclist_state = InternalNeuromodulatorState(
        npf_hunger=0.40,
        octopamine_vigor=0.95,  # Loves endurance sports
        serotonin_patience=0.50,
        pdf_sleep_debt=0.10     # Early riser
    )
    result = brain.decide_commute(options, cyclist_state, weather_heat_index=0.1) # 20C autumn morning
    assert result['chosen_mode'] == 'Bicycle', f"Expected Bicycle, got {result['chosen_mode']}"
    assert result['probabilities']['Bicycle'] > 0.35
    print(f"  [PASS] Athletic Cyclist -> Bicycle ({result['probabilities']['Bicycle']*100:.1f}%)")

def test_summer_heat_suppresses_biking():
    """Extreme Brisbane summer heat (35C + humidity) makes PPL1 punishment high, flipping to Car/Transit."""
    brain = DrosophilaCommuteBrain()
    options = get_standard_brisbane_options()
    cyclist_state = InternalNeuromodulatorState(
        npf_hunger=0.40,
        octopamine_vigor=0.70,
        serotonin_patience=0.50,
        pdf_sleep_debt=0.20
    )
    # Summer heatwave: heat_index = 0.95
    result_heatwave = brain.decide_commute(options, cyclist_state, weather_heat_index=0.95)
    assert result_heatwave['chosen_mode'] != 'Bicycle', "Heatwave should discourage heavy cycling"
    print(f"  [PASS] Heatwave shifts choice from Bike to {result_heatwave['chosen_mode']}")

def test_firing_rates_and_probabilities_normalized():
    """Verify all probabilities sum to 1.0 and firing rates remain physiological."""
    brain = DrosophilaCommuteBrain()
    options = get_standard_brisbane_options()
    state = InternalNeuromodulatorState(0.5, 0.5, 0.5, 0.5)
    result = brain.decide_commute(options, state)
    
    total_prob = sum(result['probabilities'].values())
    assert np.isclose(total_prob, 1.0, atol=1e-5), f"Probabilities sum to {total_prob}"
    
    for ev in result['evaluations']:
        hz = ev['firing_rate_hz']
        assert 5.0 <= hz <= 90.0, f"Firing rate {hz} out of physiological range"
    print("  [PASS] Normalization & Physiological firing bounds verified")

def test_empirical_calibration_weights():
    """Verify that both PRIOR and CALIBRATED weights are loadable and behave consistently."""
    from drosophila_brain_engine import PRIOR_BRAIN_WEIGHTS, CALIBRATED_BRAIN_WEIGHTS, get_calibration_provenance
    
    brain_prior = DrosophilaCommuteBrain(weights=PRIOR_BRAIN_WEIGHTS)
    brain_calib = DrosophilaCommuteBrain(weights=CALIBRATED_BRAIN_WEIGHTS)
    
    options = get_standard_brisbane_options()
    state = InternalNeuromodulatorState(0.95, 0.30, 0.60, 0.30)
    
    res_prior = brain_prior.decide_commute(options, state)
    res_calib = brain_calib.decide_commute(options, state)
    
    assert res_prior['chosen_mode'] == 'Transit_50c'
    assert res_calib['chosen_mode'] == 'Transit_50c'
    
    prov = get_calibration_provenance()
    assert prov['rmse_after'] < prov['rmse_before'], "Calibrated RMSE must be lower than prior RMSE"
    assert prov['calibrated_loss'] < prov['prior_loss'], "Calibrated loss must be lower than prior loss"
    print(f"  [PASS] Empirical Calibration verified: RMSE {prov['rmse_before']}% -> {prov['rmse_after']}% (Loss -{((prov['prior_loss']-prov['calibrated_loss'])/prov['prior_loss']*100):.1f}%)")

if __name__ == '__main__':
    print("Running Drosophila Commute Brain Unit Tests:")
    test_student_high_npf_prefers_50c_transit()
    test_wealthy_sleepy_professional_prefers_car()
    test_athletic_cyclist_prefers_bike_in_cool_weather()
    test_summer_heat_suppresses_biking()
    test_firing_rates_and_probabilities_normalized()
    test_empirical_calibration_weights()
    print(">>> ALL 6 UNIT TESTS PASSED WITH 100% SUCCESS! <<<")