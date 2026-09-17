"""
🧠 Drosophila Connectome Commute Simulator: Brisbane Transit Choice
Main Streamlit Application Entry Point.
"""
import os
import json
import streamlit as st

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
from src.ai import inject_fly_engineer_floating_widget

st.set_page_config(
    page_title="Drosophila Connectome Transit Simulator | Brisbane AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        st.markdown('<div class="main-header">🧠 Drosophila Connectome Commute Simulator | Brisbane Transit AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Grounding Real Janelia FlyEM (male-cns:v1.0) Neuronal Connectome into Urban Transit Choice & Queensland 50-Cent Policy Analysis</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid #10b981; border-radius: 8px; padding: 10px 16px; margin-bottom: 14px;">
            <span style="color: #10b981; font-weight: 700;">🟢 Model Provenance:</span>
            <span style="color: #e2e8f0; font-size: 0.92rem;"> Neural decision weights empirically calibrated via SciPy MLE against <b>24.7M Translink Go Card transactions</b> (Queensland Open Data Jul–Aug 2024) & <b>Q2 2025-26 Patronage Report</b> (RMSE: 3.92% ➔ <b>1.99%</b>, Loss <b>-72.5%</b>).</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="main-header">🧠 果蠅大腦通勤決策模擬器 (Brisbane Transit)</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">整合美國 Janelia FlyEM 真實雄性果蠅中樞神經連接體 (male-cns:v1.0) 與昆士蘭 50-Cent 大眾交通博弈決策</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid #10b981; border-radius: 8px; padding: 10px 16px; margin-bottom: 14px;">
            <span style="color: #10b981; font-weight: 700;">🟢 數據層科學校準：</span>
            <span style="color: #e2e8f0; font-size: 0.92rem;"> 神經權重已透過 <b>昆士蘭開放資料庫 2,477 萬筆 Translink Go Card 刷卡大數據 (2024 年 7-8 月)</b> 與 <b>Q2 2025-26 季報</b> 完成 SciPy MLE/MAP 反向校準（RMSE: 3.92% ➔ <b>1.99%</b>，擬合誤差縮減 <b>72.5%</b>）。</span>
        </div>
        """, unsafe_allow_html=True)

    # Tabs definition
    tab_titles_en = [
        "🔬 3D Connectome & System Intro",
        "🎬 Doomfly Telemetry Arena",
        "🔍 Curious Phenomena & Insights",
        "👥 10,000-Commuter Population Setup",
        "📊 10,000-Commuter Simulation Results",
        "🏛️ Policy & Engineering White Paper",
        "🔮 Future Urban Horizons (2032/2040/2050)",
        "🎯 Suburb Transit & Spatial Equity"
    ]
    tab_titles_zh = [
        "🔬 果蠅神經 3D 解剖與系統導論",
        "🎬 果蠅通勤動態舞台 (Doomfly Arena)",
        "🔍 有趣的現象與反常數據",
        "👥 萬人群體設定與空間佈局",
        "📊 萬人模擬結果與政策驗證",
        "🏛️ 布里斯本交通工程規劃建言",
        "🔮 未來路網願景規劃 (2032/2040/2050)",
        "🎯 區域生活圈大眾運輸與路權診斷室"
    ]

    t_home, t_arena, t_phenom, t_pop_setup, t_pop_results, t_whitepaper, t_future, t_equity = st.tabs(
        tab_titles_en if sb.is_en else tab_titles_zh
    )

    with t_home:
        render_tab1_connectome(viz, sb.eval_res, sb.is_en)

    with t_arena:
        render_tab2_archetypes(sb.is_en)

    with t_phenom:
        render_tab3_phenomena(sb.is_en)

    with t_pop_setup:
        render_tab4_society_setup(study_data, sb.is_en)

    with t_pop_results:
        render_tab5_calibration(study_data, sb.is_en)

    with t_whitepaper:
        render_tab6_whitepaper(sb.is_en)

    with t_future:
        render_tab7_future(sb.is_en)

    with t_equity:
        render_tab8_spatial_equity(sb.is_en)

    # Footer
    st.markdown("---")
    st.caption("🔬 Bio-Inspired Transit Choice Model | Powered by Streamlit, Plotly & Janelia FlyEM Connectome Dataset")

    # Fly Engineer Floating AI Assistant
    inject_fly_engineer_floating_widget(sb.is_en)

if __name__ == "__main__":
    main()
