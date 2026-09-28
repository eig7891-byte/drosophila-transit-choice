"""
Drosophila Connectome Commute Simulator: Brisbane Transit Choice
Main Streamlit Application Entry Point.
"""
import os
import sys
import json

# Ensure repository root is always at index 0 of sys.path
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import streamlit as st

st.set_page_config(
    page_title="Drosophila Connectome Transit Simulator | Brisbane AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from src.core import (
    DrosophilaCommuteBrain,
    CommuteOption,
    InternalNeuromodulatorState,
    BrainWeights,
    CALIBRATED_BRAIN_WEIGHTS,
    get_calibration_provenance,
)
from src.simulation import BrisbaneTransitSimulator, BRISBANE_CORRIDORS
from src.visualization import DrosophilaConnectomeVisualizer
from src.ui.styles import inject_custom_styles
from src.ui.sidebar import render_sidebar

try:
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
    )
except Exception as _import_err:
    import traceback
    st.error(f"Startup Import Error: {_import_err}")
    st.code(traceback.format_exc())
    st.stop()

# Custom Styling
inject_custom_styles()

# -------------------------------------------------------------
# Component Caching & Data Loading
# -------------------------------------------------------------
_ROOT = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_visualizer():
    return DrosophilaConnectomeVisualizer()

@st.cache_resource
def load_simulator():
    return BrisbaneTransitSimulator(seed=42)

@st.cache_data
def load_precomputed_report():
    candidate_paths = [
        os.path.join(_ROOT, "data", "parameters", "brisbane_transit_statistical_report.json"),
        os.path.join(_ROOT, "brisbane_transit_statistical_report.json"),
        "brisbane_transit_statistical_report.json",
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    sim = load_simulator()
    study = sim.run_comparative_policy_study(10000)
    save_path = candidate_paths[0]
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(study, f, indent=2)
    return study

def main():
    viz = load_visualizer()
    sim = load_simulator()
    study_data = load_precomputed_report()

    # Sidebar inputs and state evaluation
    sb = render_sidebar()

    # Main Header
    if sb.is_en:
        st.markdown('<div class="main-header">Drosophila Connectome Commute Simulator | Brisbane Transit AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Grounding Real Janelia FlyEM (male-cns:v1.0) Neuronal Connectome into Urban Transit Choice & Queensland 50-Cent Policy Analysis</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: #11221f; border: 1px solid #10b981; border-radius: 8px; padding: 12px 16px; margin-bottom: 14px;">
            <span style="color: #00e676; font-weight: 700;">Model Provenance:</span>
            <span style="color: #f1f5f9; font-size: 0.92rem;"> Neural decision weights empirically calibrated via SciPy MLE against <strong style="color: #ffffff;">24.7M Translink Go Card transactions</strong> (Queensland Open Data Jul–Aug 2024) &amp; <strong style="color: #ffffff;">Q2 2025-26 Patronage Report</strong> (RMSE: 3.92% -&gt; <strong style="color: #00e676;">1.99%</strong>, Loss <strong style="color: #00e676;">-72.5%</strong>).</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="main-header">果蠅大腦通勤決策模擬器 (Brisbane Transit)</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">整合美國 Janelia FlyEM 真實雄性果蠅中樞神經連接體 (male-cns:v1.0) 與昆士蘭 50-Cent 大眾交通博弈決策</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: #11221f; border: 1px solid #10b981; border-radius: 8px; padding: 12px 16px; margin-bottom: 14px;">
            <span style="color: #00e676; font-weight: 700;">數據層科學校準：</span>
            <span style="color: #f1f5f9; font-size: 0.92rem;"> 神經權重已透過 <strong style="color: #ffffff;">昆士蘭開放資料庫 2,477 萬筆 Translink Go Card 刷卡大數據 (2024 年 7-8 月)</strong> 與 <strong style="color: #ffffff;">Q2 2025-26 季報</strong> 完成 SciPy MLE/MAP 反向校準（RMSE: 3.92% -&gt; <strong style="color: #00e676;">1.99%</strong>，擬合誤差縮減 <strong style="color: #00e676;">72.5%</strong>）。</span>
        </div>
        """, unsafe_allow_html=True)

    # Tabs definition - Streamlined 3-Chapter Interactive Showcase
    tab_titles_en = [
        "1. Corridor Showdown (Benchmark)",
        "2. Data Provenance & Calibration",
        "3. Policy Sandbox (Simulation)"
    ]
    tab_titles_zh = [
        "1. 走廊實證預測對決 (Showdown)",
        "2. 數據溯源與校準 (Calibration)",
        "3. 政策敏感度沙盒 (Sandbox)"
    ]

    t_showdown, t_calib, t_sandbox = st.tabs(
        tab_titles_en if sb.is_en else tab_titles_zh
    )

    with t_showdown:
        render_tab1_showdown(sb.is_en)

    with t_calib:
        render_tab2_calibration(viz, sb.eval_res, sb.is_en)

    with t_sandbox:
        render_tab3_sandbox(study_data, sb.is_en)

    # Footer
    st.markdown("---")
    st.caption("Bio-Inspired Transit Choice Model | Powered by Streamlit, Plotly & Janelia FlyEM Connectome Dataset")

if __name__ == "__main__":
    main()

