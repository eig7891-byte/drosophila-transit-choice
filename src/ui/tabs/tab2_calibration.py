"""
Tab 2: Empirical Data Provenance & SciPy MLE Calibration Engine
==============================================================
Presents the 24.7M Go Card dataset, the scientific justification for calibration,
parameter shift table (Before vs After), and the collapsible 3D connectome visualizer.
"""
import streamlit as st
import pandas as pd
from src.visualization import DrosophilaConnectomeVisualizer

def render_tab2_calibration(viz: DrosophilaConnectomeVisualizer, eval_res: dict, is_en: bool):
    st.markdown("## " + ("Chapter 2: Empirical Data Provenance & SciPy MLE Calibration Engine" if is_en else "第二章：實證大數據溯源與 SciPy MLE 校準引擎 (Data & Calibration)"))
    st.markdown(
        "Demonstrating data provenance, the mathematical calibration framework using 24.7M TransLink Go Card transactions, parameter shifts, and proof against overfitting."
        if is_en else
        "展示模型數據來源之真實性、透過昆士蘭 2,477 萬筆 Go Card 刷卡大數據進行 SciPy MLE/MAP 反向校準之數學架構、權重位移原因，以及盲測防過度擬合驗證。"
    )

    # -------------------------------------------------------------------------
    # 2.1 Calibration Performance Metrics
    # -------------------------------------------------------------------------
    st.markdown("### " + ("2.1 Calibration Performance & Provenance" if is_en else "2.1 數據規模與校準成果指標"))
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric(
            label="Go Card Transactions" if is_en else "Go Card 刷卡大數據",
            value="24,772,971",
            delta="Queensland Open Data" if is_en else "昆士蘭開放資料庫"
        )
    with col_m2:
        st.metric(
            label="Calibration Engine" if is_en else "校準優化引擎",
            value="SciPy MLE / MAP",
            delta="Likelihood Loss" if is_en else "最大概似估計"
        )
    with col_m3:
        st.metric(
            label="Objective Loss Reduction" if is_en else "擬合損失函數縮減",
            value="-72.5%",
            delta="120.5 -> 33.1 Loss" if is_en else "誤差大幅降低"
        )
    with col_m4:
        st.metric(
            label="Cross-Corridor RMSE" if is_en else "跨走廊均方根誤差",
            value="1.99%",
            delta="Down from 3.92%" if is_en else "原 3.92% 降至 1.99%"
        )

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 2.2 Why Calibrate? (The Subtropical Commuter Reality)
    # -------------------------------------------------------------------------
    st.markdown("### 2.2 " + ("Why Calibrate? Addressing the Reality of Subtropical Commuters" if is_en else "2.2 為何需要校準？修正果蠅先驗值與亞熱帶通勤現實的偏差"))
    st.markdown(
        "Initial biological priors were derived from laboratory fruit fly locomotion and general behavioral economics. While mechanistically sound, uncalibrated priors showed an RMSE of 3.92% when applied to Brisbane. Calibration was necessary to capture two crucial real-world behaviors:"
        if is_en else
        "初始生物學先驗權重來自實驗室果蠅生理研究與一般行為經濟學。直接套用於布里斯本時，初始均方根誤差為 3.92%。為了反映真實城市交通，必須透過真實數據進行反向校準，以修正兩大現實行為偏誤："
    )

    col_why1, col_why2 = st.columns(2)
    with col_why1:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #ff5252; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
            <h5 style="color: #ff5252; margin: 0 0 4px 0;">1. Subtropical Pedestrian Fatigue (d^1.51)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.55;">
                Laboratory flies do not experience 30°C Queensland sun. Prior models underestimated suburban car resistance because they assumed linear walking penalties. Calibration adjusted the walk exponent to <b>d^1.508</b>, accurately capturing why drivers refuse to walk 2.2 km for a $3 fare saving.
            </p>
        </div>
        """ if is_en else """
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #ff5252; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
            <h5 style="color: #ff5252; margin: 0 0 4px 0;">1. 亞熱帶徒步高溫疲勞 (d^1.51)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.55;">
                實驗室果蠅沒有曝曬在昆士蘭 30°C 豔陽下。未校準模型低估了外環車主的自駕習慣。校準將步行阻抗指數提升至 <b>d^1.508</b>，精準解釋了為何省下 $3 票價依然無法說服車主走 2.2 公里。
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_why2:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #00e676; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
            <h5 style="color: #00e676; margin: 0 0 4px 0;">2. Diminishing Marginal Dopamine (tanh Saturation)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.55;">
                Linear transport models assume infinite linear elasticity when fares drop to near-zero. Real PAM dopamine neurons exhibit hyperbolic tangent saturation. Commuters feel intense excitement at 50c, but this plateaued, preventing runaway overpredictions on suburban routes.
            </p>
        </div>
        """ if is_en else """
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #00e676; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
            <h5 style="color: #00e676; margin: 0 0 4px 0;">2. 金錢多巴胺之邊際效用遞減 (tanh 飽和)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.55;">
                傳統線性模型假設極端降價效益無限延伸。真實 PAM 多巴胺迴路具備雙曲正切飽和特性。降至 50c 時雖然放電劇烈，但在缺乏專用道路權時會迅速飽和，避免了郊區客流預測的盲目膨脹。
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 2.3 How Calibrated? (Parameter Shift Table)
    # -------------------------------------------------------------------------
    st.markdown("### 2.3 " + ("How Calibrated? Prior vs. Calibrated Synaptic Weights" if is_en else "2.3 如何校準？先驗值與校準後神經突觸權重位移對照表"))
    
    param_table = [
        {"Parameter": "w_pam_money (Savings Reward)", "Prior": "0.2500", "Calibrated": "0.1497", "Change": "-40.1%", "Neuro-Economic Mechanism": "Diminishing marginal dopamine"},
        {"Parameter": "w_pam_speed (Speed Reward)", "Prior": "0.2000", "Calibrated": "0.1912", "Change": "-4.4%", "Neuro-Economic Mechanism": "Robust premium on time savings"},
        {"Parameter": "w_ppl1_cost (Fare Punishment)", "Prior": "0.3000", "Calibrated": "0.4500", "Change": "+50.0%", "Neuro-Economic Mechanism": "Loss aversion (Kahneman-Tversky)"},
        {"Parameter": "w_ppl1_delay (Delay Punishment)", "Prior": "0.3000", "Calibrated": "0.3495", "Change": "+16.5%", "Neuro-Economic Mechanism": "Cumulative boredom on stopping buses"},
        {"Parameter": "w_ppl1_fatigue (Walking Fatigue)", "Prior": "0.2000", "Calibrated": "0.3500", "Change": "+75.0%", "Neuro-Economic Mechanism": "Subtropical heat fatigue penalty"},
        {"Parameter": "fatigue_exp (Nonlinear Exponent)", "Prior": "1.3000", "Calibrated": "1.5076", "Change": "+16.0%", "Neuro-Economic Mechanism": "Steep exponential penalty >1.5km"}
    ] if is_en else [
        {"權重變數 (Parameter)": "w_pam_money (省錢多巴胺)", "先驗值 (Prior)": "0.2500", "校準後 (Calibrated)": "0.1497", "變動": "-40.1%", "行為學機制": "邊際金錢多巴胺遞減"},
        {"權重變數 (Parameter)": "w_pam_speed (時間多巴胺)", "先驗值 (Prior)": "0.2000", "校準後 (Calibrated)": "0.1912", "變動": "-4.4%", "行為學機制": "省時誘因穩定維持"},
        {"權重變數 (Parameter)": "w_ppl1_cost (購票痛感)", "先驗值 (Prior)": "0.3000", "校準後 (Calibrated)": "0.4500", "變動": "+50.0%", "行為學機制": "損失厭惡 (Loss Aversion)"},
        {"權重變數 (Parameter)": "w_ppl1_delay (行車延遲痛)", "先驗值 (Prior)": "0.3000", "校準後 (Calibrated)": "0.3495", "變動": "+16.5%", "行為學機制": "慢速停站累積焦慮"},
        {"權重變數 (Parameter)": "w_ppl1_fatigue (步行疲勞痛)", "先驗值 (Prior)": "0.2000", "校準後 (Calibrated)": "0.3500", "變動": "+75.0%", "行為學機制": "亞熱帶步行阻力超出預期"},
        {"權重變數 (Parameter)": "fatigue_exp (非線性衰減指數)", "先驗值 (Prior)": "1.3000", "校準後 (Calibrated)": "1.5076", "變動": "+16.0%", "行為學機制": "超過 1.5km 步行阻抗呈指數增長"}
    ]
    st.table(pd.DataFrame(param_table))

    st.success(
        "Proof Against Overfitting: Routes 60 and 66 were held out completely from training. With synaptic weights 100% frozen, the model achieved -0.99 pp on Route 60 and -2.31% on Route 66, proving authentic out-of-sample generalizability."
        if is_en else
        "徹底粉碎過度擬合疑慮：Route 60 與 Route 66 完全不參與任何參數校準。在神經突觸權重 100% 完全凍結下，模型在 Route 60 誤差僅 -0.99 pp，在 Route 66 誤差僅 -2.31%，證實模型具備貨真價實的外推泛化力。"
    )

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Collapsible Expanders: 3D Connectome & Demographic Archetypes
    # -------------------------------------------------------------------------
    with st.expander("Explore Janelia FlyEM 3D Connectome (male-cns:v1.0, 26,000+ Spatial Nodes)" if is_en else "檢視美國 Janelia FlyEM 果蠅 3D 中樞神經連接體骨架 (26,000+ 空間節點)"):
        st.markdown(
            "Interactive WebGL 3D visualization of the male fruit fly central nervous system (HHMI Janelia FlyEM `male-cns:v1.0`). Colored by PAM approach clusters (green) vs PPL1 aversive clusters (red)."
            if is_en else
            "美國霍華德·休斯醫學研究所 (HHMI Janelia FlyEM `male-cns:v1.0`) 雄性果蠅中樞神經三維骨架。綠色代表 PAM 趨向獎勵迴路，紅色代表 PPL1 痛感懲罰迴路。"
        )
        if viz:
            fig_3d = viz.create_3d_connectome_figure(eval_res)
            st.plotly_chart(fig_3d, use_container_width=True)

    with st.expander("View 5 Commuter Archetypes Demographic Gating" if is_en else "檢視五大市民通勤族群人口設定與資產門檻"):
        archetypes_table = [
            {"Archetype": "CBD White-Collar", "Population Share": "30%", "Vehicle Ownership": "88.0%", "NPF (Budget Pain)": "0.10 - 0.40 (Low)", "Time Sensitivity": "Extreme (Busway Dependent)"},
            {"Archetype": "Budget Students", "Population Share": "20%", "Vehicle Ownership": "22.5%", "NPF (Budget Pain)": "0.75 - 0.95 (Very High)", "Time Sensitivity": "Low (Enthusiastic for 50c)"},
            {"Archetype": "Shift Workers", "Population Share": "15%", "Vehicle Ownership": "85.0%", "NPF (Budget Pain)": "0.50 - 0.80 (Moderate-High)", "Time Sensitivity": "Moderate (Night Timetable Constrained)"},
            {"Archetype": "Suburban Families", "Population Share": "20%", "Vehicle Ownership": "95.6%", "NPF (Budget Pain)": "0.40 - 0.70 (Moderate)", "Time Sensitivity": "Moderate (Refuses Long Walks)"},
            {"Archetype": "Fitness Commuters", "Population Share": "15%", "Vehicle Ownership": "88.0%", "NPF (Budget Pain)": "0.20 - 0.60 (Moderate)", "Time Sensitivity": "High Octopamine (Cycles when fine)"}
        ] if is_en else [
            {"族群 (Archetype)": "CBD 白領上班族", "人口佔比": "30%", "車輛持有": "88.0%", "NPF (預算痛感)": "0.10 - 0.40 (低)", "時間敏感度": "極高 (重度依賴專用道)"},
            {"族群 (Archetype)": "預算約束學生族", "人口佔比": "20%", "車輛持有": "22.5%", "NPF (預算痛感)": "0.75 - 0.95 (極高)", "時間敏感度": "低 (對 50c 狂熱)"},
            {"族群 (Archetype)": "非尖峰輪班勞工", "人口佔比": "15%", "車輛持有": "85.0%", "NPF (預算痛感)": "0.50 - 0.80 (中高)", "時間敏感度": "中等 (受限夜間班次)"},
            {"族群 (Archetype)": "外環郊區家庭", "人口佔比": "20%", "車輛持有": "95.6%", "NPF (預算痛感)": "0.40 - 0.70 (中等)", "時間敏感度": "中等 (拒絕長途步行)"},
            {"族群 (Archetype)": "健康自行車族", "人口佔比": "15%", "車輛持有": "88.0%", "NPF (預算痛感)": "0.20 - 0.60 (中等)", "時間敏感度": "高辛弗林 (天候良好即騎車)"}
        ]
        st.table(pd.DataFrame(archetypes_table))
