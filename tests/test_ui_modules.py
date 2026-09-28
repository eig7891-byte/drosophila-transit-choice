"""
Tests for UI modules, styles, tabs, and visualizer integration.
"""
import pytest
from src.ui.styles import CUSTOM_CSS, inject_custom_styles
from src.ui.tabs import (
    render_tab1_showdown,
    render_tab2_calibration,
    render_tab3_sandbox,
    render_tab1_connectome,
    render_tab2_grounding,
    render_tab3_calibration_tmr,
    render_tab4_core_corridors,
    render_tab5_validation_routes,
    render_tab6_conclusions,
    render_tab7_database,
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
    """Confirms all chapter and legacy tab renderers are callable functions."""
    tabs = [
        render_tab1_showdown,
        render_tab2_calibration,
        render_tab3_sandbox,
        render_tab1_connectome,
        render_tab2_grounding,
        render_tab3_calibration_tmr,
        render_tab4_core_corridors,
        render_tab5_validation_routes,
        render_tab6_conclusions,
        render_tab7_database,
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


def test_english_mode_ui_purity():
    """Verifies that all 7 dashboard tabs emit zero Chinese characters when is_en=True."""
    import re
    import streamlit as st
    from src.ui.sidebar import render_sidebar

    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    leaks = []

    def check_val(ctx, val):
        if isinstance(val, str) and chinese_pattern.search(val):
            leaks.append((ctx, val))
        elif isinstance(val, (list, tuple, set)):
            for item in val:
                check_val(ctx, item)
        elif isinstance(val, dict):
            for k, v in val.items():
                check_val(f"{ctx}[k]", k)
                check_val(f"{ctx}[v]", v)
        elif hasattr(val, "to_dict"):
            try:
                check_val(ctx, val.to_dict())
            except Exception:
                pass

    methods = ['markdown', 'metric', 'write', 'caption', 'title', 'header', 'subheader', 'dataframe', 'table', 'info', 'warning', 'error', 'success', 'selectbox', 'radio', 'slider', 'tabs', 'expander']
    for m in methods:
        orig = getattr(st, m, None)
        if orig:
            def make_w(name, original_fn):
                def w(*args, **kwargs):
                    for a in args:
                        check_val(f"st.{name}", a)
                    for k, v in kwargs.items():
                        check_val(f"st.{name}({k})", v)
                    if name in ('selectbox', 'radio') and len(args) > 1 and args[1]:
                        return args[1][0]
                    if name == 'slider' and len(args) > 3:
                        return args[3]
                    return original_fn(*args, **kwargs)
                return w
            setattr(st, m, make_w(m, orig))

    sb = render_sidebar()
    viz = DrosophilaConnectomeVisualizer()
    study_data = {
        'corridors': {
            'Springwood': {'name': 'Springwood to Brisbane CBD', 'real_growth_pct': 3.75, 'drosophila_pred_pct': 3.75, 'tmr_predicted_growth_pct': 31.88, 'tmr_overprediction_pct': 28.13},
            'UQ': {'name': 'UQ Lakes to CBD via Busway', 'real_growth_pct': 32.0, 'drosophila_pred_pct': 32.35, 'tmr_predicted_growth_pct': 38.55, 'tmr_overprediction_pct': 6.20},
            'Route60': {'name': 'Route 60 CityGlider', 'real_growth_pct': 25.0, 'drosophila_pred_pct': 22.96, 'tmr_predicted_growth_pct': 11.12, 'tmr_overprediction_pct': -13.88},
            'Route66': {'name': 'Route 66 RBWH to UQ Lakes', 'real_growth_pct': 25.7, 'drosophila_pred_pct': 28.0, 'tmr_predicted_growth_pct': 31.27, 'tmr_overprediction_pct': 5.57},
        }
    }

    # Render new 3-tab showcase
    render_tab1_showdown(True)
    render_tab2_calibration(viz, sb.eval_res, True)
    render_tab3_sandbox(study_data, True)

    # Render legacy tabs
    render_tab1_connectome(viz, sb.eval_res, True)
    render_tab2_grounding(True)
    render_tab3_calibration_tmr(True)
    render_tab4_core_corridors(True)
    render_tab5_validation_routes(True)
    render_tab6_conclusions(study_data, True)
    render_tab7_database(True)

    # Exclude sidebar language toggle labels from leak assertions
    ui_tab_leaks = [
        (c, t) for c, t in leaks
        if not (c.startswith("st.sidebar") and ("Language /" in t or "繁體中文" in t or "選擇語言" in t))
    ]
    assert len(ui_tab_leaks) == 0, f"Detected Chinese text leaking in English UI: {ui_tab_leaks}"

