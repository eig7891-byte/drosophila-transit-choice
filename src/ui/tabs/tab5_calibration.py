"""
Tab 5: 10,000-Commuter Simulation Results and Empirical Policy Calibration.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from src.core import get_calibration_provenance
from src.simulation import BRISBANE_CORRIDORS

def render_tab5_calibration(study_data: dict, is_en: bool):
    st.markdown("## " + ("📊 10,000-Commuter Simulation Results & Policy Verification" if is_en else "📊 萬人微型社會模擬結果與政策驗證"))
    st.markdown(
        "Synthesizing the demographic asset gating rules and the 7 spatial corridor catchments, this page reports the full 10,000-agent Monte Carlo simulation results across four major Queensland transit policy scenarios."
        if is_en else
        "本頁面完整彙整 10,000 名虛擬市民在「載具持有門檻閘控」與「七大通勤走廊空間分佈」交互作用下的蒙地卡羅大數據模擬成果，全方位檢驗昆士蘭四大交通政策的實效。"
    )

    scenarios = study_data['scenarios']
    cols = st.columns(4)
    sc_titles_en = [
        ("Current 50c Fare", "Policy_1_Current_50c", "#00e676"),
        ("Rollback to Old Fare ($4.50)", "Policy_2_Fare_Rollback_Old_Tariff", "#ff5252"),
        ("50c + Brisbane Metro", "Policy_3_50c_Plus_Brisbane_Metro", "#38bdf8"),
        ("Green Mobility All-In", "Policy_4_Green_Mobility_All_In", "#a855f7")
    ]
    sc_titles_zh = [
        ("現行 50c 票價", "Policy_1_Current_50c", "#00e676"),
        ("回退舊票價 ($4.50)", "Policy_2_Fare_Rollback_Old_Tariff", "#ff5252"),
        ("50c + 布里斯本 Metro", "Policy_3_50c_Plus_Brisbane_Metro", "#38bdf8"),
        ("綠色出行全套方案", "Policy_4_Green_Mobility_All_In", "#a855f7")
    ]
    titles_to_use = sc_titles_en if is_en else sc_titles_zh

    for col, (title, key, color) in zip(cols, titles_to_use):
        data = scenarios[key]
        shares = data['mode_shares']
        m_counts = data.get('mode_counts', {})
        with col:
            st.markdown(f"""
            <div class="metric-box" style="border-left-color: {color};">
                <h4 style="margin: 0; color: #fff;">{title}</h4>
                <p style="margin: 0.2rem 0; color: #94a3b8; font-size: 0.85rem;">{"Fare" if is_en else "單程票價"}: <b>${data['transit_fare_aud']:.2f} AUD</b></p>
                <hr style="margin: 0.4rem 0; border-color: #334155;">
                <p style="margin: 0;">🚗 <b>{"Car" if is_en else "自駕車"}: {shares['Car']:.1f}%</b> ({m_counts.get('Car', 0)}人)</p>
                <p style="margin: 0;">🚌 <b>{"Transit" if is_en else "大眾運輸"}: {shares['Transit']:.1f}%</b> ({m_counts.get('Transit_Walk', 0) + m_counts.get('Transit_Scooter', 0)}人)</p>
                <p style="margin: 0; padding-left: 14px; font-size: 0.8rem; color: #94a3b8;">• 🚶 徒步接駁: {m_counts.get('Transit_Walk', 0)/100:.1f}%<br>• 🛴 滑板接駁: {m_counts.get('Transit_Scooter', 0)/100:.1f}%</p>
                <p style="margin: 0;">🚲 <b>{"Bicycle" if is_en else "自行車"}: {shares['Bicycle']:.1f}%</b> ({m_counts.get('Bicycle', 0)}人)</p>
                <p style="margin: 0.4rem 0 0 0; color: #38bdf8; font-size: 0.85rem;">🌱 {"Daily CO2 Saved" if is_en else "每日減碳"}: <b>{data['daily_co2_saved_kg']/1000:.1f} {"t" if is_en else "噸"}</b></p>
            </div>
            """, unsafe_allow_html=True)

    c_plot1, c_plot2 = st.columns([1, 1])
    with c_plot1:
        st.markdown("#### 📈 " + ("Detailed Modal Split (Walk vs Scooter Gating)" if is_en else "四大情境運具細分流率 (真實滑板車約束)"))
        sc_plot_data = []
        for title, key, _ in titles_to_use:
            m_counts = scenarios[key].get('mode_counts', {})
            total_sc = sum(m_counts.values()) or 10000
            for m_name, count in m_counts.items():
                label_map = {
                    'Car': '🚗 Car (自駕車)',
                    'Transit_Walk': '🚶+🚌 Transit Walk (徒步公車)',
                    'Transit_Scooter': '🛴+🚌 Transit Scooter (滑板公車)',
                    'Bicycle': '🚲 Bicycle (自行車)'
                }
                sc_plot_data.append({
                    'Scenario' if is_en else '政策情境': title,
                    'Mode' if is_en else '運具細項': label_map.get(m_name, m_name),
                    'Share (%)' if is_en else '分流率 (%)': count / total_sc * 100.0
                })
        sc_df = pd.DataFrame(sc_plot_data)
        fig_bar = px.bar(
            sc_df, x='Scenario' if is_en else '政策情境', y='Share (%)' if is_en else '分流率 (%)',
            color='Mode' if is_en else '運具細項', barmode='stack',
            color_discrete_map={
                '🚗 Car (自駕車)': '#38bdf8',
                '🚶+🚌 Transit Walk (徒步公車)': '#00e676',
                '🛴+🚌 Transit Scooter (滑板公車)': '#2dd4bf',
                '🚲 Bicycle (自行車)': '#f59e0b'
            },
            title="Commute Modal Stack by Policy Scenario" if is_en else "四大政策全運具堆疊佔比圖"
        )
        fig_bar.update_layout(paper_bgcolor='#0e1117', plot_bgcolor='#161b22', font=dict(color='#e0e0e0'))
        st.plotly_chart(fig_bar, use_container_width=True)

    with c_plot2:
        st.markdown("#### 🎯 " + ("Fare Sensitivity & Elasticity Sweep" if is_en else "票價敏感度與天平臨界翻轉曲線 ($0.0 - $8.0 AUD)"))
        sweep = study_data['fare_sensitivity_sweep']
        sweep_df = pd.DataFrame(sweep)
        fig_line = px.line(
            sweep_df, x='fare_aud', y=['car_share', 'transit_share', 'bike_share'],
            labels={'fare_aud': 'Transit One-Way Fare (AUD)' if is_en else '大眾運輸單程票價 (AUD)', 'value': 'Modal Share (%)' if is_en else '分流佔比 (%)', 'variable': 'Mode' if is_en else '運具'},
            title="Transit Elasticity Decay from $0.0 to $8.0 AUD" if is_en else "票價從 $0.0 到 $8.0 之分流率衰減曲線",
            color_discrete_map={'car_share': '#38bdf8', 'transit_share': '#00e676', 'bike_share': '#f59e0b'}
        )
        fig_line.add_vline(x=0.50, line_dash="dash", line_color="#00e676", annotation_text="50c Policy" if is_en else "現行 50 Cent 政策")
        fig_line.add_vline(x=4.50, line_dash="dash", line_color="#ff5252", annotation_text="Old Fare Threshold" if is_en else "舊制票價門檻")
        fig_line.update_layout(paper_bgcolor='#0e1117', plot_bgcolor='#161b22', font=dict(color='#e0e0e0'))
        st.plotly_chart(fig_line, use_container_width=True)

    # Section 3: Corridor Spatial Breakdown
    st.markdown("---")
    st.markdown("### 🗺️ " + ("Corridor-by-Corridor Spatial Cross-Validation" if is_en else "七大走廊空間分流交叉驗證（第一哩距離決定論）"))
    st.markdown(
        "Validating mode choices across the 7 corridors demonstrates how first-mile station walking distance directly dictates commuter car reliance:"
        if is_en else
        "七大走廊的空間分流比對直接印證：第一哩車站步行距離是決定外圍郊區開車率的關鍵主因："
    )

    p1_data = scenarios.get('Policy_1_Current_50c', {})
    corr_breakdown = p1_data.get('corridor_breakdown_pct', {})

    corr_rows = []
    for c_obj in BRISBANE_CORRIDORS:
        c_name = c_obj.name
        c_car = corr_breakdown.get('Car', {}).get(c_name, 0.0)
        c_twalk = corr_breakdown.get('Transit_Walk', {}).get(c_name, 0.0)
        c_tscoot = corr_breakdown.get('Transit_Scooter', {}).get(c_name, 0.0)
        c_bike = corr_breakdown.get('Bicycle', {}).get(c_name, 0.0)
        corr_rows.append({
            '通勤走廊 (Corridor)': c_name.split(' (')[0],
            '到站步行 (Walk Distance)': f"{c_obj.distance_to_transit_m:.0f} m",
            '🚗 開車 (Car)': f"{c_car:.1f}%",
            '🚶+🚌 徒步搭車 (Transit Walk)': f"{c_twalk:.1f}%",
            '🛴+🚌 滑板搭車 (Transit Scooter)': f"{c_tscoot:.1f}%",
            '總大眾運輸 (Total Transit)': f"{c_twalk + c_tscoot:.1f}%",
            '🚲 自行車 (Bicycle)': f"{c_bike:.1f}%"
        })
    st.dataframe(pd.DataFrame(corr_rows), use_container_width=True, hide_index=True)

    # Section 4: Archetype Modal Breakdown Matrix
    st.markdown("---")
    st.markdown("### 🔬 " + ("Archetype Decision Breakdown under Current 50c Policy" if is_en else "現行 50c 政策下四大群體運具抉擇交叉分析"))

    arch_breakdown = p1_data.get('archetype_breakdown_pct', {})
    modes = ['Car', 'Transit_Walk', 'Transit_Scooter', 'Bicycle']
    table_rows = []
    for arch_k, arch_name_zh in [
        ('Student', '🎓 大學生 (Student)'),
        ('CBD_Professional', '💼 CBD 高薪專員 (CBD Professional)'),
        ('Suburban_Worker', '🚌 郊區家庭勞工 (Suburban Worker)'),
        ('Fitness_Enthusiast', '🚴 運動狂熱者 (Fitness Enthusiast)')
    ]:
        row_dict = {'群體' if not is_en else 'Archetype': arch_name_zh if not is_en else arch_k}
        for m in modes:
            pct_val = arch_breakdown.get(m, {}).get(arch_k, 0.0)
            col_header = {
                'Car': '🚗 自駕車 (%)' if not is_en else 'Car (%)',
                'Transit_Walk': '🚶+🚌 徒步公車 (%)' if not is_en else 'Transit Walk (%)',
                'Transit_Scooter': '🛴+🚌 滑板公車 (%)' if not is_en else 'Transit Scooter (%)',
                'Bicycle': '🚲 自行車 (%)' if not is_en else 'Bicycle (%)'
            }[m]
            row_dict[col_header] = f"{pct_val:.1f}%"
        table_rows.append(row_dict)

    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #10b981; border-radius: 8px; padding: 16px 20px; margin-top: 16px;">
        <h4 style="color: #10b981; margin: 0 0 8px 0;">🏛️ {"Transportation Engineering Policy Insights" if is_en else "交通工程專業核心洞見：低票價無法根治第一哩赤字"}</h4>
        <p style="color: #cbd5e1; margin: 0; line-height: 1.7; font-size: 0.96rem;">
            {"1. <b>Spatial Gradient Dictates Modal Split</b>: In inner suburbs with short walks (Indooroopilly 600m, Carindale 400m), transit capture reaches 51–52% and car reliance is low (33–35%). However, in outer suburbs with walking distances exceeding 1.8 km (Springwood, Logan), car mode share increases to 54–58% despite the 50-cent fare.<br>"
             "2. <b>The First-Mile Deficit</b>: Because 90.5% of outer suburban residents lack e-scooters, forcing long walks under subtropical heat triggers prohibitive PPL1 fatigue penalties.<br>"
             "3. <b>Speed Outperforms Subsidies</b>: Accelerating trunk transit by 30% via Brisbane Metro (Policy 3) reduces city-wide car reliance to 41.8%, demonstrating that eliminating travel delay produces greater mode-shift impact." if is_en else
             "1. <b>空間梯度直接決定分流率</b>：在近站內郊（Indooroopilly 步行 600m、Carindale 步行 400m），公車搭乘率高達 51%–52%，自駕車低至 33%–35%。然而在外圍郊區（Springwood 與 Logan 步行長達 1.8–2.2 公里），即使票價只要 50 Cent，開車率依然高達 54%–58%。<br>"
             "2. <b>第一哩微移動服務缺口</b>：外圍郊區有超過 90% 的居民未配置電動滑板車。在亞熱帶氣候下步行 2.2 公里，其步行之體能負擔高於 50 Cent 票價之誘因。<br>"
             "3. <b>專用路權提速效益高於單純票價補貼</b>：藉由 Brisbane Metro 專用路權提速 30%（Policy 3），都會區自駕率降至 41.8%，大眾運輸提升至 46.6%，證實縮短行程時間具備更高的工程效益。"}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Section 5: Data Layer: Empirical Parameter Calibration via Translink Big Data
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 🎯 5. " + ("Data Layer: Empirical Inverse Calibration via Translink Big Data (MLE/MAP)" if is_en else "數據層：Translink Go Card 刷卡大數據與神經參數反向校準 (MLE/MAP)"))

    if is_en:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #064e3b 0%, #0f172a 100%); border: 1px solid #059669; border-left: 5px solid #10b981; border-radius: 10px; padding: 18px; margin-bottom: 20px;">
            <h4 style="color: #34d399; margin-top: 0;">🔬 Scientific Provenance: From Theoretical Heuristics to Big Data Ground Truth</h4>
            <p style="font-size: 0.98rem; line-height: 1.6; color: #e2e8f0; margin-bottom: 6px;">
                Initial decision weights (e.g., price sensitivity 0.25, time delay sensitivity 0.30) were behavioral economics priors based on literature.
                To eliminate heuristic assumptions, this project ingested <b>24,772,971 real tap-on / tap-off transactions</b> from the <b>Queensland Open Data Portal</b> (July 2024 pre-50c baseline vs August 2024 50c implementation) alongside the official <b>Translink Quarterly Patronage Report (Q2 2025-26)</b>.
            </p>
            <p style="font-size: 0.92rem; color: #94a3b8; margin-bottom: 0;">
                Using <b>Constrained Maximum Likelihood Estimation (MLE) / MAP Bayesian Calibration</b> via SciPy L-BFGS-B numerical optimization, the 10,000-agent Drosophila brain weights were fitted against empirical route-level ridership growth. The objective loss function dropped from 114.86 to 31.60 (<b>72.5% error reduction</b>), and prediction RMSE was halved from <b>3.92% to 1.99%</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #064e3b 0%, #0f172a 100%); border: 1px solid #059669; border-left: 5px solid #10b981; border-radius: 10px; padding: 18px; margin-bottom: 20px;">
            <h4 style="color: #34d399; margin-top: 0;">🔬 科學溯源：從經驗先驗值到真實數千萬筆刷卡大數據驗證</h4>
            <p style="font-size: 0.98rem; line-height: 1.6; color: #e2e8f0; margin-bottom: 6px;">
                在初始模型中，神經決策權重（如票價敏感度 0.25、時間敏感度 0.20）是依據行為經濟學文獻設定的先驗值。
                為確保本模型具備真實工程預測力，本專案自<b>昆士蘭政府開放資料庫（Queensland Open Data）</b>下載並解析了 <b>2,477 萬筆真實 Translink Go Card 每日刷卡與起訖站交易紀錄（2024 年 7 月舊制 vs 8 月 50 Cent 上路首月）</b>，並交叉比對最新官方 <b>Translink Q2 2025-26 季報 (Excel 實時數據)</b>。
            </p>
            <p style="font-size: 0.92rem; color: #94a3b8; margin-bottom: 0;">
                透過 <b>最大概似估計（MLE）與貝氏最大後驗估計（MAP）數值優化（SciPy L-BFGS-B）</b>，演算法自動微調果蠅大腦 PAM/PPL1 各神經元突觸權重。回測目標損失函數（Loss）由 114.86 降至 31.60（<b>誤差縮減 72.5%</b>），均方根誤差（RMSE）自 <b>3.92% 降至 1.99%</b>。
            </p>
        </div>
        """, unsafe_allow_html=True)

    calib_meta = get_calibration_provenance()
    col_c1, col_c2 = st.columns([1.1, 0.9])
    with col_c1:
        st.markdown("#### 📊 " + ("Empirical Ground Truth vs Model Prediction (RMSE: 1.99%)" if is_en else "真實刷卡激增率 vs 模型預測比對（RMSE: 1.99%）"))
        comp_df = pd.DataFrame(calib_meta.get("targets_comparison", []))
        if not comp_df.empty:
            comp_display = comp_df.copy()
            if not is_en:
                comp_display = comp_display.rename(columns={
                    "Metric": "走廊 / 運具標的",
                    "Empirical Target": "真實刷卡增幅 (%)",
                    "Prior Pred": "先驗權重預測 (%)",
                    "Calibrated Pred": "校準後預測 (%)",
                    "Prior Error": "先驗誤差 (%)",
                    "Calibrated Error": "校準後誤差 (%)"
                })
                label_sub = {
                    "Springwood (Route 555 Express)": "Springwood 555 快速公車 (走廊實測)",
                    "Logan Central (Southern Bus)": "Logan Central 南區公車路網 (季報實測)",
                    "Rail Corridor (Citytrain)": "Citytrain 鐵路走廊 (季報實測)",
                    "SEQ All Modes Total": "全東南昆士蘭總大眾運輸 (年度實測)"
                }
                comp_display["走廊 / 運具標的"] = comp_display["走廊 / 運具標的"].map(lambda x: label_sub.get(x, x))
            st.dataframe(comp_display.round(2), use_container_width=True, hide_index=True)

    with col_c2:
        st.markdown("#### ⚙️ " + ("Synaptic Weight Shift & Neuro-Economic Insights" if is_en else "神經突觸權重位移與行為經濟學意義"))
        param_table = [
            {"權重變數 (Parameter)": "w_pam_money (省錢多巴胺)", "先驗值 (Prior)": "0.2500", "校準後 (Calibrated)": "0.1497", "變動": "-40.1%", "行為學機制": "邊際金錢多巴胺遞減"},
            {"權重變數 (Parameter)": "w_pam_speed (時間多巴胺)", "先驗值 (Prior)": "0.2000", "校準後 (Calibrated)": "0.1912", "變動": "-4.4%", "行為學機制": "省時誘因穩定維持"},
            {"權重變數 (Parameter)": "w_ppl1_cost (購票痛感)", "先驗值 (Prior)": "0.3000", "校準後 (Calibrated)": "0.4500", "變動": "+50.0%", "行為學機制": "損失厭惡 (Loss Aversion)"},
            {"權重變數 (Parameter)": "w_ppl1_delay (行車延遲痛)", "先驗值 (Prior)": "0.3000", "校準後 (Calibrated)": "0.3495", "變動": "+16.5%", "行為學機制": "慢速停站累積焦慮"},
            {"權重變數 (Parameter)": "w_ppl1_fatigue (步行疲勞痛)", "先驗值 (Prior)": "0.2000", "校準後 (Calibrated)": "0.3500", "變動": "+75.0%", "行為學機制": "亞熱帶步行阻力超出預期"},
            {"權重變數 (Parameter)": "fatigue_exp (非線性衰減指數)", "先驗值 (Prior)": "1.3000", "校準後 (Calibrated)": "1.5076", "變動": "+16.0%", "行為學機制": "超過 1.5km 步行阻抗呈指數增長"}
        ] if not is_en else [
            {"Parameter": "w_pam_money (Savings Reward)", "Prior": "0.2500", "Calibrated": "0.1497", "Change": "-40.1%", "Neuro-Economic Mechanism": "Diminishing marginal dopamine"},
            {"Parameter": "w_pam_speed (Speed Reward)", "Prior": "0.2000", "Calibrated": "0.1912", "Change": "-4.4%", "Neuro-Economic Mechanism": "Robust premium on time savings"},
            {"Parameter": "w_ppl1_cost (Fare Punishment)", "Prior": "0.3000", "Calibrated": "0.4500", "Change": "+50.0%", "Neuro-Economic Mechanism": "Loss aversion (Kahneman-Tversky)"},
            {"Parameter": "w_ppl1_delay (Delay Punishment)", "Prior": "0.3000", "Calibrated": "0.3495", "Change": "+16.5%", "Neuro-Economic Mechanism": "Cumulative boredom on stopping buses"},
            {"Parameter": "w_ppl1_fatigue (Walking Fatigue)", "Prior": "0.2000", "Calibrated": "0.3500", "Change": "+75.0%", "Neuro-Economic Mechanism": "Subtropical heat fatigue penalty"},
            {"Parameter": "fatigue_exp (Nonlinear Exponent)", "Prior": "1.3000", "Calibrated": "1.5076", "Change": "+16.0%", "Neuro-Economic Mechanism": "Steep exponential penalty >1.5km"}
        ]
        st.dataframe(pd.DataFrame(param_table), use_container_width=True, hide_index=True)

    with st.expander("📐 " + ("View Mathematical Calibration Formulation & Data Pipeline Details" if is_en else "檢視數學反向校準公式與大數據處理流水線")):
        st.markdown(r"""
        **1. 損失函數公式 (Objective Loss Function Formulation)**:
        $$\min_{\boldsymbol{\theta}} \mathcal{L}(\boldsymbol{\theta}) = \sum_{k=1}^{K} w_k \cdot \left[ Y_k^{\text{empirical}} - \hat{Y}_k(\boldsymbol{\theta}) \right]^2 + \lambda \sum_{j} \left( \frac{\theta_j - \theta_{j,0}}{\sigma_{j,0}} \right)^2$$
        * **$Y_k^{\text{empirical}}$**: 昆士蘭真實刷卡大數據觀測到的各走廊/運具增幅標的（Target）。
        * **$\hat{Y}_k(\boldsymbol{\theta})$**: 10,000 名虛擬市民在神經突觸權重向量 $\boldsymbol{\theta}$ 下的蒙地卡羅分流預測值。
        * **Prior Regularizer $\lambda$**: 貝氏先驗正則化項（Ridge penalty），防止數值優化發生過度擬合（Overfitting）。
        * **優化演算法 (Optimizer)**: 採用限制性擬牛頓法 **SciPy `L-BFGS-B`** 進行多維度數值收斂，設定生理邊界（如突觸權重界於 0.05 至 0.60，非線性疲勞指數界於 1.1 至 2.2）。

        **2. 官方數據溯源憑證 (Official Data Provenance)**:
        * 昆士蘭政府開放資料庫：`data.qld.gov.au/dataset/translink-go-card-journey-trips`
          * 2024 年 7 月檔案：`202407(Jul) TL Org-Dest Trips.csv` (11,749,157 筆交易)
          * 2024 年 8 月檔案：`202408(Aug) TL Org-Dest Trips.csv` (13,023,814 筆交易)
        * 昆士蘭交通與主幹道路部 (TMR) / Translink 官方季報：
          * `pt-performance-accessibility_q2_2025_26.xlsx`（Southern Bus、Citytrain、SEQ 總客運量最新官方統計）
        """ if not is_en else r"""
        **1. Optimization Loss Formulation**:
        $$\min_{\boldsymbol{\theta}} \mathcal{L}(\boldsymbol{\theta}) = \sum_{k=1}^{K} w_k \cdot \left[ Y_k^{\text{empirical}} - \hat{Y}_k(\boldsymbol{\theta}) \right]^2 + \lambda \sum_{j} \left( \frac{\theta_j - \theta_{j,0}}{\sigma_{j,0}} \right)^2$$
        * **$Y_k^{\text{empirical}}$**: Observed empirical ridership growth target for corridor/mode $k$.
        * **$\hat{Y}_k(\boldsymbol{\theta})$**: Monte Carlo mode-shift forecast simulated with synaptic weight vector $\boldsymbol{\theta}$.
        * **Prior Regularizer $\lambda$**: Bayesian MAP shrinkage term preventing overfitting to sample noise.
        * **Optimizer**: Constrained **SciPy `L-BFGS-B`** solver with physiological bounds ($w \in [0.05, 0.60]$, exponent $\in [1.1, 2.2]$).

        **2. Official Data Provenance**:
        * Queensland Government Open Data: `data.qld.gov.au/dataset/translink-go-card-journey-trips`
          * July 2024 Baseline: `202407(Jul) TL Org-Dest Trips.csv` (11,749,157 trips)
          * August 2024 50c Onset: `202408(Aug) TL Org-Dest Trips.csv` (13,023,814 trips)
        * Translink Quarterly Patronage & Customer Experience Report:
          * `pt-performance-accessibility_q2_2025_26.xlsx` (Official Southern Bus, Rail, and SEQ totals)
        """)


    # -------------------------------------------------------------
