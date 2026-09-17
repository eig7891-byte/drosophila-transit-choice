"""
Tests for Brisbane transit corridors, demographic simulation, and policy comparisons.
"""
import pytest
import pandas as pd
from src.simulation import BrisbaneTransitSimulator, BRISBANE_CORRIDORS

def test_brisbane_corridors_configured():
    """Confirms all key Brisbane corridors are defined with physical parameters."""
    assert len(BRISBANE_CORRIDORS) >= 7
    names = [c.name for c in BRISBANE_CORRIDORS]
    assert any("Springwood" in n for n in names)
    assert any("Chermside" in n for n in names)
    assert any("Indooroopilly" in n for n in names)

    for c in BRISBANE_CORRIDORS:
        assert c.car_travel_time_min > 0
        assert c.transit_travel_time_min > 0
        assert c.distance_to_transit_m >= 0

def test_population_generation():
    """Generates synthetic population with ABS demographic distributions and vehicle ownership gating."""
    sim = BrisbaneTransitSimulator(seed=42)
    pop = sim.generate_population(n_commuters=1000)

    assert isinstance(pop, pd.DataFrame)
    assert len(pop) == 1000
    for col in ["npf", "octopamine", "serotonin", "pdf", "has_car", "has_bike", "has_scooter", "corridor_name"]:
        assert col in pop.columns

    # Check vehicle ownership bounds
    assert 0.0 < pop["has_car"].mean() < 1.0
    # Values bounded between 0 and 1
    assert pop["npf"].between(0.0, 1.0).all()
    assert pop["pdf"].between(0.0, 1.0).all()

def test_comparative_policy_study():
    """Verifies that running comparative policy study returns required policy scenario keys."""
    sim = BrisbaneTransitSimulator(seed=42)
    study = sim.run_comparative_policy_study(n_commuters=500)

    assert "scenarios" in study
    assert "Policy_1_Current_50c" in study["scenarios"]
    assert "Policy_2_Fare_Rollback_Old_Tariff" in study["scenarios"]
    assert "Policy_3_50c_Plus_Brisbane_Metro" in study["scenarios"]
    assert "Policy_4_Green_Mobility_All_In" in study["scenarios"]

    # 50c policy should produce higher transit share than old fare tariff
    pt_50c = study["scenarios"]["Policy_1_Current_50c"]["mode_shares"]["Transit"]
    pt_old = study["scenarios"]["Policy_2_Fare_Rollback_Old_Tariff"]["mode_shares"]["Transit"]
    assert pt_50c > pt_old
