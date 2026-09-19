# Consistency Verification Tests
import os
import re
import json
import pytest
from src.simulation.corridors import BRISBANE_CORRIDORS
from src.core import get_calibration_provenance

def test_corridor_counts_and_attributes():
    assert len(BRISBANE_CORRIDORS) == 7
    for c in BRISBANE_CORRIDORS:
        assert c.distance_km > 0
        assert c.car_travel_time_min > 0
        assert c.transit_travel_time_min > 0
        assert c.distance_to_transit_m >= 0

def test_calibration_targets_alignment():
    prov = get_calibration_provenance()
    assert prov['rmse_after'] <= 2.05
    assert prov['calibrated_loss'] < 35.0

    targets = {t['Metric']: t for t in prov.get('targets_comparison', [])}
    assert any('Springwood' in k for k in targets)
    assert any('Logan' in k for k in targets)
    assert any('SEQ' in k for k in targets)

def test_statistical_report_scenarios():
    path = os.path.join('data', 'parameters', 'brisbane_transit_statistical_report.json')
    if not os.path.exists(path):
        path = os.path.join('brisbane_transit_statistical_report.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert data['total_commuters_simulated'] == 10000
    scenarios = data['scenarios']

    p1 = scenarios['Policy_1_Current_50c']
    assert abs(p1['mode_shares']['Car'] - 51.38) < 0.1
    assert abs(p1['mode_shares']['Transit'] - 36.01) < 0.1
    assert abs(p1['mode_shares']['Bicycle'] - 12.61) < 0.1

    p3 = scenarios['Policy_3_50c_Plus_Brisbane_Metro']
    assert abs(p3['mode_shares']['Transit'] - 43.51) < 0.1
    assert abs(p3['mode_shares']['Car'] - 45.57) < 0.1

def test_zero_emojis_in_source_code():
    emoji_pattern = re.compile(r'[𐀀-􏿿‍✀-➿]')
    for root, dirs, files in os.walk('src'):
        for f in files:
            if f.endswith('.py'):
                filepath = os.path.join(root, f)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                    matches = emoji_pattern.findall(content)
                    assert len(matches) == 0, f'Found emojis in {filepath}: {matches}'
