"""
System Integration & End-to-End Regression Suite.
Verifies data loading across all subdirectories, lack of stray files,
and complete headless rendering of all 8 tabs in both languages.
"""
import os
import sys
import json
import pytest
from unittest.mock import MagicMock, patch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.core import (
    DrosophilaCommuteBrain,
    CommuteOption,
    InternalNeuromodulatorState,
    BrainWeights,
    CALIBRATED_BRAIN_WEIGHTS,
    get_calibration_provenance
)
from src.simulation import BrisbaneTransitSimulator, BRISBANE_CORRIDORS
from src.visualization import DrosophilaConnectomeVisualizer
from src.ui.tabs import (
    render_tab1_connectome,
    render_tab2_archetypes,
    render_tab3_phenomena,
    render_tab4_society_setup,
    render_tab5_calibration,
    render_tab6_whitepaper,
    render_tab7_future,
    render_tab8_spatial_equity
)

def test_data_subdirectories_exist():
    """Verify all subdirectories exist and contain expected files."""
    expected_files = [
        os.path.join(ROOT, "data", "connectome", "MBON01_Approach_10013.json"),
        os.path.join(ROOT, "data", "connectome", "MBON11_Avoidance_11402.json"),
        os.path.join(ROOT, "data", "connectome", "PPL101_Aversive_DAN_11900.json"),
        os.path.join(ROOT, "data", "empirical", "empirical_calibration_targets.json"),
        os.path.join(ROOT, "data", "empirical", "pt-performance-accessibility_q2_2025_26.xlsx"),
        os.path.join(ROOT, "data", "metadata", "flywire_brain_architecture_metrics.json"),
        os.path.join(ROOT, "data", "metadata", "flywire_transit_neuron_catalog.csv"),
        os.path.join(ROOT, "data", "metadata", "flywire_transit_neuron_catalog.json"),
        os.path.join(ROOT, "data", "parameters", "calibrated_brain_parameters.json"),
        os.path.join(ROOT, "data", "parameters", "brisbane_transit_statistical_report.json"),
        os.path.join(ROOT, "data", "parameters", "brisbane_future_simulation_data.json"),
        os.path.join(ROOT, "reports", "brisbane_transit_report.md"),
        os.path.join(ROOT, "assets", "doomfly_arena.html"),
        os.path.join(ROOT, "LICENSE"),
        os.path.join(ROOT, "CITATION.cff"),
        os.path.join(ROOT, ".gitattributes"),
        os.path.join(ROOT, ".gitignore"),
        os.path.join(ROOT, "requirements.txt"),
        os.path.join(ROOT, "README.md"),
        os.path.join(ROOT, "app.py"),
    ]
    for f in expected_files:
        assert os.path.exists(f), f"Missing required file: {f}"

def test_no_stray_data_files_in_root():
    """Verify root directory does NOT contain any loose raw data files."""
    disallowed_root_files = [
        "brisbane_future_simulation_data.json",
        "brisbane_transit_report.md",
        "brisbane_transit_statistical_report.json",
        "calibrated_brain_parameters.json",
        "pt-performance-accessibility_q2_2025_26.xlsx",
        "app_drosophila_transit.py",
        "brisbane_transit_simulator.py",
        "drosophila_brain_engine.py",
        "drosophila_visualizer.py",
        "fly_engineer_ai.py",
    ]
    for f in disallowed_root_files:
        p = os.path.join(ROOT, f)
        assert not os.path.exists(p), f"Stray file still found in root: {f}"

def test_connectome_visualizer_data_loading():
    """Verify visualizer correctly loads neuron morphology from data/connectome/."""
    viz = DrosophilaConnectomeVisualizer()
    neurons = viz.neurons
    assert len(neurons) == 3, "Expected 3 key functional neurons"
    for name, coords in neurons.items():
        assert len(coords) > 100, f"Neuron {name} has insufficient nodes"
    fig = viz.create_3d_connectome_figure()
    assert fig is not None

@patch("streamlit.markdown")
@patch("streamlit.columns")
@patch("streamlit.dataframe")
@patch("streamlit.table")
@patch("streamlit.plotly_chart")
@patch("streamlit.metric")
@patch("streamlit.expander")
@patch("streamlit.info")
@patch("streamlit.success")
@patch("streamlit.warning")
@patch("streamlit.slider")
@patch("streamlit.selectbox")
@patch("streamlit.radio")
@patch("streamlit.components.v1.html")
def test_render_all_tabs_headless(mock_html, mock_radio, mock_select, mock_slider,
                                   mock_warn, mock_succ, mock_info, mock_exp, mock_met,
                                   mock_chart, mock_tbl, mock_df, mock_cols, mock_md):
    """Simulate rendering all 8 tabs in both English and Chinese without errors."""
    mock_cols.side_effect = lambda n: [MagicMock() for _ in range(n if isinstance(n, int) else len(n))]
    mock_slider.return_value = 0.5
    mock_select.side_effect = lambda label, options, *args, **kwargs: options[kwargs.get('index', 0)] if options else None
    mock_radio.return_value = "Current 50-Cent Policy (50c PT)"
    
    viz = DrosophilaConnectomeVisualizer()
    report_path = os.path.join(ROOT, "data", "parameters", "brisbane_transit_statistical_report.json")
    with open(report_path, "r", encoding="utf-8") as f:
        report_data = json.load(f)

    for is_en in [True, False]:
        render_tab1_connectome(viz, None, is_en)
        render_tab2_archetypes(is_en)
        render_tab3_phenomena(is_en)
        render_tab4_society_setup(report_data, is_en)
        render_tab5_calibration(report_data, is_en)
        render_tab6_whitepaper(is_en)
        render_tab7_future(is_en)
        render_tab8_spatial_equity(is_en)
