"""
Tests for UI modules, styles, tabs, and visualizer integration.
"""
import pytest
from src.ui.styles import CUSTOM_CSS, inject_custom_styles
from src.ui.tabs import (
    render_tab1_connectome,
    render_tab2_archetypes,
    render_tab3_phenomena,
    render_tab4_society_setup,
    render_tab5_calibration,
    render_tab6_whitepaper,
    render_tab7_future,
    render_tab8_spatial_equity,
)
from src.visualization import DrosophilaConnectomeVisualizer
from src.ai import get_avatar_b64, inject_fly_engineer_floating_widget

def test_custom_styles_defined():
    """Confirms custom CSS rules contain core dashboard classes."""
    assert ".main-header" in CUSTOM_CSS
    assert ".intro-banner" in CUSTOM_CSS
    assert ".character-card" in CUSTOM_CSS
    assert callable(inject_custom_styles)

def test_tab_renderers_callable():
    """Confirms all 8 decomposed tab renderers are callable functions."""
    tabs = [
        render_tab1_connectome,
        render_tab2_archetypes,
        render_tab3_phenomena,
        render_tab4_society_setup,
        render_tab5_calibration,
        render_tab6_whitepaper,
        render_tab7_future,
        render_tab8_spatial_equity,
    ]
    for tab_fn in tabs:
        assert callable(tab_fn)

def test_visualizer_creation():
    """Confirms DrosophilaConnectomeVisualizer creates 3D Plotly figure."""
    viz = DrosophilaConnectomeVisualizer()
    fig = viz.create_3d_connectome_figure()
    assert fig is not None
    assert hasattr(fig, "data")
    assert len(fig.data) > 0

def test_ai_assistant_functions():
    """Confirms AI assistant functions are available."""
    assert callable(get_avatar_b64)
    assert callable(inject_fly_engineer_floating_widget)
