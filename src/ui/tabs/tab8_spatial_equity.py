"""
Tab 8: Suburb Transit and Spatial Equity Sandbox.
"""
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.core import (
    DrosophilaCommuteBrain,
    CommuteOption,
    InternalNeuromodulatorState,
    CALIBRATED_BRAIN_WEIGHTS,
)

def render_tab8_spatial_equity(is_en: bool):
    st.markdown("## " + (" Suburb Transit & Spatial Equity Sandbox: Area-Level Modal Split & Access Diagnostic" if is_en else " 區域生活圈大眾運輸與路權空間診斷室：生活圈運具分流與可及性評估沙盒"))

    if is_en:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); border: 1px solid #00e676; border-left: 5px solid #00e676; border-radius: 10px; padding: 18px; margin-bottom: 20px;">
            <h4 style="color: #00e676; margin-top: 0;"> Scientific Methodology: Multi-Agent Area Diagnostics via Queensland TMR Framework</h4>
            <p style="font-size: 0.96rem; line-height: 1.6; color: #e2e8f0; margin-bottom: 6px;">
                Instead of testing a single household, this sandbox evaluates an <b>entire suburb / residential catchment</b> using the <b>Queensland Department of Transport and Main Roads (TMR)</b> official travel demand classifications:
                <b>(1) CBD Commuters</b>, <b>(2) Non-CBD Suburban Workers</b> (70%+ of QLD jobs), <b>(3) Tertiary Students</b>, and <b>(4) Family Escort / School Run Trips</b> (Trip Chaining).
            </p>
            <p style="font-size: 0.90rem; color: #cbd5e1; margin-bottom: 0;">
                The Drosophila connectome engine (empirically calibrated against 24.7M Translink Go Card transactions) runs 500 multi-agent synthetic commuters to compute the area's <b>public transit share</b>, <b>road space footprint (FIFA soccer fields occupied)</b>, <b>first-mile access deficit</b>, and <b>primary travel impedances</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); border: 1px solid #00e676; border-left: 5px solid #00e676; border-radius: 10px; padding: 18px; margin-bottom: 20px;">
            <h4 style="color: #00e676; margin-top: 0;"> 科學評估架構：導入昆士蘭主幹道交通部 (TMR) 官方四大交通市場區隔</h4>
            <p style="font-size: 0.96rem; line-height: 1.6; color: #e2e8f0; margin-bottom: 6px;">
                本模組不再局限於單一家庭，而是評估<b>「整個生活圈／行政社區」</b>的總體交通健康度。系統嚴格對標昆士蘭 TMR 官方家戶旅次調查（HTS）四大分類：
                <b>(1) CBD 白領通勤族</b>、<b>(2) 跨郊區在地工薪族</b>（佔昆士蘭工作大宗 70% 以上）、<b>(3) 大專與青年學生</b>、以及<b>(4) 家庭育兒接送族（School Run 旅次鏈）</b>。
            </p>
            <p style="font-size: 0.90rem; color: #cbd5e1; margin-bottom: 0;">
                透過由 2,477 萬筆 Translink Go Card 刷卡大數據反向校準之果蠅連接體決策大腦，即時蒙地卡羅模擬 500 名虛擬市民，精確產出該區域之<b>大眾運輸市占率</b>、<b>尖峰道路空間佔用量（等效國際足球場）</b>、<b>第一哩步行可及性赤字</b>與<b>三大主要阻抗來源</b>。
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Preset Suburb Definitions
    # ---------------------------------------------------------
    preset_data = {
        "Springwood (外圍家庭型汽車城 - Logan City)": {
            "en_name": "Springwood (Outer Suburban Family Car Haven - Logan)",
            "pop": 9400,
            "walk_m": 1800.0,
            "within_400m": 28.0,
            "headway": 30.0,
            "cars": 1.9,
            "scooter": 8.0,
            "pct_cbd": 15,
            "pct_suburban": 35,
            "pct_student": 10,
            "pct_family": 40,
            "desc_zh": "典型外圍低密度家庭社區：依賴汽車、第一哩步行偏遠、家庭接送與跨區工薪佔比高達 75%。",
            "desc_en": "Classic outer low-density suburb: Car-dependent, long first-mile walk, 75% family escort & non-CBD workers."
        },
        "Logan Central (多元工薪與大眾運輸弱勢區 - Logan City)": {
            "en_name": "Logan Central (Diverse Working-Class Suburb - Logan)",
            "pop": 6400,
            "walk_m": 1600.0,
            "within_400m": 35.0,
            "headway": 25.0,
            "cars": 1.5,
            "scooter": 7.0,
            "pct_cbd": 10,
            "pct_suburban": 45,
            "pct_student": 20,
            "pct_family": 25,
            "desc_zh": "外圍藍領工薪生活圈：收入較低、無車比例偏高，受惠於 50 Cent 票價補貼，但受限於轉乘與步行距離。",
            "desc_en": "Outer working-class hub: Lower median income, higher transit captivity, benefits from 50c fare but constrained by access."
        },
        "St Lucia / Toowong (大學城與高眾運內環區 - Brisbane Inner West)": {
            "en_name": "St Lucia / Toowong (University Hub & High-Transit Inner Suburb)",
            "pop": 14000,
            "walk_m": 350.0,
            "within_400m": 92.0,
            "headway": 10.0,
            "cars": 1.1,
            "scooter": 28.0,
            "pct_cbd": 35,
            "pct_suburban": 10,
            "pct_student": 45,
            "pct_family": 10,
            "desc_zh": "內環高密度青年生活圈：公車站密布（400m 覆蓋率 92%）、學生與 CBD 白領主導，大眾運輸使用率極高。",
            "desc_en": "Inner-ring student & professional hub: 92% 400m stop coverage, 10-min headways, high active & transit usage."
        },
        "Indooroopilly / Carindale (中密度綜合生活圈 - Brisbane Middle Ring)": {
            "en_name": "Indooroopilly / Carindale (Medium-Density Activity Centre)",
            "pop": 12000,
            "walk_m": 550.0,
            "within_400m": 78.0,
            "headway": 15.0,
            "cars": 1.6,
            "scooter": 18.0,
            "pct_cbd": 40,
            "pct_suburban": 20,
            "pct_student": 15,
            "pct_family": 25,
            "desc_zh": "中密度中環核心區：結合大型購物中心、公車專用道樞紐與優質學區，通勤運具多元均衡。",
            "desc_en": "Middle-ring regional hub: Major busway interchange, balanced professional & family demographic mix."
        },
        "Custom Area (自訂自選社區參數)": {
            "en_name": "Custom Area (User-Defined Suburb)",
            "pop": 10000,
            "walk_m": 800.0,
            "within_400m": 50.0,
            "headway": 20.0,
            "cars": 1.8,
            "scooter": 12.0,
            "pct_cbd": 25,
            "pct_suburban": 35,
            "pct_student": 15,
            "pct_family": 25,
            "desc_zh": "自由調整下方所有空間、人口與設施參數，評估任何自訂社區的果蠅通勤幸福度。",
            "desc_en": "Freely adjust all spatial, demographic and infrastructure parameters below."
        }
    }

    # Preset Selector Box
    st.markdown("### 1. " + ("Select a Suburb Preset or Customize" if is_en else "選擇生活圈模板或自訂區域參數"))
    suburb_choice_keys = list(preset_data.keys())
    selected_suburb_key = st.selectbox(
        "Choose an Area Benchmark:" if is_en else "選擇區域生活圈標竿：",
        suburb_choice_keys,
        format_func=lambda k: preset_data[k]["en_name"] if is_en else k,
        index=0
    )
    cur_p = preset_data[selected_suburb_key]
    st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #1e3a8a; border-left: 5px solid #38bdf8; border-radius: 8px; padding: 12px 16px; margin: 10px 0 16px 0;">
        <span style="color: #38bdf8; font-weight: 700; font-size: 0.96rem;">{cur_p['en_name'] if is_en else selected_suburb_key}:</span>
        <span style="color: #f1f5f9; font-size: 0.94rem; margin-left: 6px;">{cur_p['desc_en'] if is_en else cur_p['desc_zh']}</span>
    </div>
    """, unsafe_allow_html=True)

    # Sliders and Control Panels
    with st.expander("Fine-Tune Area Demographic & Spatial Indicators" if is_en else "微調該區域人口組成與空間指標", expanded=(selected_suburb_key.startswith("Custom"))):
        col_ctl1, col_ctl2, col_ctl3 = st.columns(3)
        with col_ctl1:
            st.markdown("##### " + ("TMR 4 Commuter Segments (%)" if is_en else "昆士蘭 TMR 四大通勤族群佔比 (%)"))
            in_cbd = st.slider("CBD Commuters (%):" if is_en else "CBD 白領族佔比 (%):", 0, 100, cur_p["pct_cbd"], 5)
            in_suburban = st.slider("Non-CBD Workers (%):" if is_en else "跨郊區工薪佔比 (%):", 0, 100, cur_p["pct_suburban"], 5)
            in_student = st.slider("Tertiary Students (%):" if is_en else "大專青年學生佔比 (%):", 0, 100, cur_p["pct_student"], 5)
            in_family = st.slider("Family Escort (%):" if is_en else "育兒接送家庭佔比 (%):", 0, 100, cur_p["pct_family"], 5)

        with col_ctl2:
            st.markdown("##### " + ("Spatial & Transit Catchment (TMR PTIM)" if is_en else "空間覆蓋與站點距離 (TMR PTIM 標準)"))
            in_walk = st.slider("Walk Distance to Stop (m):" if is_en else "平均到站步行距離 (m):", 100, 2500, int(cur_p["walk_m"]), 50)
            in_cov = st.slider("Pop. within 400m Coverage (%):" if is_en else "400m 站點人口覆蓋率 (%):", 10, 100, int(cur_p["within_400m"]), 5)
            in_headway = st.slider("Bus Headway (min):" if is_en else "公車服務班距 (分鐘):", 5, 60, int(cur_p["headway"]), 5)
            in_cars = st.slider("Cars per Dwelling:" if is_en else "每戶平均擁車數:", 0.5, 3.0, float(cur_p["cars"]), 0.1)

        with col_ctl3:
            st.markdown("##### " + ("Policy, Asset & Climate Context" if is_en else "票價補貼、微移動與天氣情境"))
            in_fare = st.slider("Transit Fare (AUD):" if is_en else "單程大眾運輸票價 (AUD):", 0.0, 6.0, 0.50, 0.50)
            in_scooter = st.slider("E-Scooter Ownership (%):" if is_en else "私人滑板車持有率 (%):", 2, 50, int(cur_p["scooter"]), 2)
            in_heat = st.slider("Weather Heat Index:" if is_en else "夏季高溫熱浪指數:", 0.0, 1.0, 0.25, 0.05, help="0.0=20°C, 1.0=36°C humid summer storm" if is_en else "0.0=20°C 晴朗舒適, 1.0=36°C 酷暑暴雨")

    # Policy Intervention Toggles
    st.markdown("### 2. " + ("Interactive Planning Interventions (What-If Prescriptions)" if is_en else "互動式都市交通工程處方箋（即時沙盒試算）"))
    col_rx1, col_rx2, col_rx3 = st.columns(3)
    with col_rx1:
        rx_stops = st.checkbox("Prescription 1: Dense Feeder Stops" if is_en else "處方一：增設公車支線站牌", value=False, help="Reduces average walking distance to 400m PTIM standard" if is_en else "將全區平均步行距離壓縮至 400m 標準")
    with col_rx2:
        rx_scooters = st.checkbox("Prescription 2: Shared E-Scooter Hubs" if is_en else "處方二：廣設公共微移動租借站", value=False, help="Elevates first-mile micro-mobility access to 75%" if is_en else "解決第一哩接駁，滑板車可用度提升至 75%")
    with col_rx3:
        rx_metro = st.checkbox("Prescription 3: Dedicated Transit Speedup" if is_en else "處方三：專用路權／Brisbane Metro 提速 30%", value=False, help="Accelerates trunk transit travel time by 30%" if is_en else "幹線專用道提速 30%，消滅行車延遲")

    # ---------------------------------------------------------
    # Run Connectome Simulation for this Suburb
    # ---------------------------------------------------------
    # Effective values after interventions
    eff_walk_m = 400.0 if rx_stops else float(in_walk)
    eff_scooter_prob = 0.75 if rx_scooters else (in_scooter / 100.0)
    speed_factor = 0.70 if rx_metro else 1.0

    total_segment_weight = in_cbd + in_suburban + in_student + in_family
    if total_segment_weight <= 0:
        total_segment_weight = 100
    prob_segments = [in_cbd / total_segment_weight, in_suburban / total_segment_weight, in_student / total_segment_weight, in_family / total_segment_weight]

    rng_sim = np.random.default_rng(42)
    sample_n = 500
    suburb_pop = cur_p["pop"]

    sampled_types = rng_sim.choice(['CBD', 'Suburban', 'Student', 'Family'], size=sample_n, p=prob_segments)

    sim_records = []
    brain_diag = DrosophilaCommuteBrain(weights=CALIBRATED_BRAIN_WEIGHTS)

    for t_commuter in sampled_types:
        has_car = bool(rng_sim.random() < min(0.98, in_cars * 0.52))
        has_scooter = bool(rng_sim.random() < eff_scooter_prob)
        has_bike = bool(rng_sim.random() < 0.25)

        if t_commuter == 'CBD':
            state_commuter = InternalNeuromodulatorState(
                npf_hunger=rng_sim.uniform(0.05, 0.35),
                octopamine_vigor=rng_sim.uniform(0.15, 0.45),
                serotonin_patience=rng_sim.uniform(0.10, 0.40),
                pdf_sleep_debt=rng_sim.uniform(0.50, 0.90)
            )
            t_car = 32.0
            c_car = 28.0  # High CBD parking fee
            base_t_transit = 45.0 * speed_factor + in_headway / 2.0
            effort_mult = 1.0
        elif t_commuter == 'Suburban':
            state_commuter = InternalNeuromodulatorState(
                npf_hunger=rng_sim.uniform(0.35, 0.70),
                octopamine_vigor=rng_sim.uniform(0.20, 0.50),
                serotonin_patience=rng_sim.uniform(0.20, 0.50),
                pdf_sleep_debt=rng_sim.uniform(0.30, 0.70)
            )
            t_car = 20.0
            c_car = 10.0  # Free parking at suburban industrial/retail workplace
            base_t_transit = 55.0 * speed_factor + in_headway / 2.0
            effort_mult = 1.0
        elif t_commuter == 'Student':
            state_commuter = InternalNeuromodulatorState(
                npf_hunger=rng_sim.uniform(0.75, 0.98),
                octopamine_vigor=rng_sim.uniform(0.20, 0.50),
                serotonin_patience=rng_sim.uniform(0.40, 0.75),
                pdf_sleep_debt=rng_sim.uniform(0.30, 0.70)
            )
            t_car = 30.0
            c_car = 22.0
            base_t_transit = 40.0 * speed_factor + in_headway / 2.0
            effort_mult = 1.0
        else: # Family Escort
            state_commuter = InternalNeuromodulatorState(
                npf_hunger=rng_sim.uniform(0.30, 0.65),
                octopamine_vigor=rng_sim.uniform(0.15, 0.40),
                serotonin_patience=rng_sim.uniform(0.10, 0.35),
                pdf_sleep_debt=rng_sim.uniform(0.50, 0.85)
            )
            t_car = 25.0
            c_car = 16.0
            base_t_transit = 62.0 * speed_factor + in_headway / 2.0
            effort_mult = 1.45  # Child handling / stroller burden

        walk_time_min = eff_walk_m / 84.0
        t_transit_walk = base_t_transit + walk_time_min * 2.0
        walk_effort = min(1.0, (0.15 + eff_walk_m / 3500.0) * effort_mult)

        scooter_time_min = eff_walk_m / 240.0
        t_transit_scooter = base_t_transit + scooter_time_min * 2.0
        scooter_cost = (in_fare + (1.0 + 0.45 * scooter_time_min)) * 2.0

        options_c = []
        if has_car:
            options_c.append(CommuteOption('Car', t_car, c_car, 0.05, 9.0 - t_car / 60.0, 0.95))
        options_c.append(CommuteOption('Transit_Walk', t_transit_walk, in_fare * 2.0, walk_effort, 9.0 - t_transit_walk / 60.0, 0.70))
        if has_scooter:
            options_c.append(CommuteOption('Transit_Scooter', t_transit_scooter, scooter_cost, 0.10, 9.0 - t_transit_scooter / 60.0, 0.80))
        if has_bike:
            options_c.append(CommuteOption('Bicycle', 55.0, 0.0, 0.85, 8.0, 0.45))

        decision_c = brain_diag.decide_commute(
            options_c, state_commuter,
            weather_heat_index=in_heat,
            stochastic_sample=True,
            rng=rng_sim
        )

        chosen_m = decision_c['chosen_mode']
        eval_c = next(e for e in decision_c['evaluations'] if e['option_name'] == chosen_m)

        sim_records.append({
            'type': t_commuter,
            'chosen_mode': chosen_m,
            'net_valence': float(eval_c['net_valence']),
            'pam_reward': float(eval_c['pam_reward_total']),
            'ppl1_cost': float(eval_c['ppl1_cost_total']),
            'fatigue_pain': float(eval_c['ppl1_components']['physical_fatigue']),
            'delay_pain': float(eval_c['ppl1_components']['time_delay']),
            'cost_pain': float(eval_c['ppl1_components']['out_of_pocket_cost'])
        })

    df_sim_res = pd.DataFrame(sim_records)

    # Aggregated Metrics
    car_pct = float((df_sim_res['chosen_mode'] == 'Car').mean() * 100.0)
    transit_walk_pct = float((df_sim_res['chosen_mode'] == 'Transit_Walk').mean() * 100.0)
    transit_scoot_pct = float((df_sim_res['chosen_mode'] == 'Transit_Scooter').mean() * 100.0)
    transit_total_pct = transit_walk_pct + transit_scoot_pct
    bike_pct = float((df_sim_res['chosen_mode'] == 'Bicycle').mean() * 100.0)

    # Road space calculation: Car 35m2, Bus 1.4m2, Bike 3.0m2
    total_road_m2 = (car_pct / 100.0 * 35.0 + transit_total_pct / 100.0 * 1.4 + bike_pct / 100.0 * 3.0) * suburb_pop
    fifa_soccer_fields = total_road_m2 / 7140.0

    # ---------------------------------------------------------
    # Output Display
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("### 3. " + ("Multi-Agent Transportation Engineering Diagnostic Dashboard" if is_en else "多主體交通工程與路權公平診斷儀表板"))

    # Row 1: KPI Metric Cards (Option A: 4 Hard Engineering & Spatial Equity Pillars)
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)

    # 1. Transit Share Status
    if transit_total_pct >= 60.0:
        transit_color = "#00e676"
        transit_status = " 高眾運主導生活圈" if not is_en else " High Transit Integration"
    elif transit_total_pct >= 35.0:
        transit_color = "#f59e0b"
        transit_status = "Moderate Transit Share" if is_en else "多模態過渡生活圈"
    else:
        transit_color = "#ff3366"
        transit_status = "High Car Captivity" if is_en else "嚴重自駕單一依賴"

    with col_k1:
        st.markdown(f"""
        <div class="metric-box" style="border-left-color: {transit_color};">
            <h4 style="margin: 0; color: #fff;">{"Public Transit Mode Share" if is_en else "全區大眾運輸市占率"}</h4>
            <h2 style="margin: 0.3rem 0; color: {transit_color};">{transit_total_pct:.1f}%</h2>
            <p style="margin: 0; color: {transit_color}; font-size: 0.82rem; font-weight: 600;">{transit_status}</p>
            <p style="margin: 0.2rem 0 0 0; color: #cbd5e1; font-size: 0.85rem;">{"Walk: " if is_en else "徒步: "}{transit_walk_pct:.1f}% | {"Scooter: " if is_en else "滑板: "}{transit_scoot_pct:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    # 2. Car Share & Congestion Load
    car_color = "#38bdf8"
    if car_pct > 70.0:
        car_status = "Arterial Near Capacity" if is_en else "幹道容量極度吃緊"
    elif car_pct < 45.0:
        car_status = "Sustainable Car Load" if is_en else "幹道車流負荷可控"
    else:
        car_status = "Moderate Congestion" if is_en else "輕度尖峰壅塞風險"

    with col_k2:
        st.markdown(f"""
        <div class="metric-box" style="border-left-color: {car_color};">
            <h4 style="margin: 0; color: #fff;">{"Private Car Mode Share" if is_en else "私家車自駕依賴率"}</h4>
            <h2 style="margin: 0.3rem 0; color: {car_color};">{car_pct:.1f}%</h2>
            <p style="margin: 0; color: {car_color}; font-size: 0.82rem; font-weight: 600;">{car_status}</p>
            <p style="margin: 0.2rem 0 0 0; color: #cbd5e1; font-size: 0.85rem;">{"Equivalent Fleet: " if is_en else "尖峰自駕車隊: "}{int(suburb_pop * car_pct / 100):,} {"Vehicles" if is_en else "輛"}</p>
        </div>
        """, unsafe_allow_html=True)

    # 3. Peak Road Space Footprint
    with col_k3:
        st.markdown(f"""
        <div class="metric-box" style="border-left-color: #a855f7;">
            <h4 style="margin: 0; color: #fff;">{"Peak Road Space Occupied" if is_en else "尖峰道路空間佔用量"}</h4>
            <h2 style="margin: 0.3rem 0; color: #a855f7;">{fifa_soccer_fields:.1f} <span style="font-size: 0.95rem; color: #cbd5e1;">{"Fields" if is_en else "座足球場"}</span></h2>
            <p style="margin: 0; color: #a855f7; font-size: 0.82rem; font-weight: 600;">{"Car 35m² vs Bus 1.4m² (25x)" if is_en else "自駕 35m² vs 公車 1.4m² (25倍)"}</p>
            <p style="margin: 0.2rem 0 0 0; color: #cbd5e1; font-size: 0.85rem;">{"Total road space: " if is_en else "總佔用 "}{total_road_m2/10000:.1f}{"0k m² lanes" if is_en else " 萬 m² 瀝青車道"}</p>
        </div>
        """, unsafe_allow_html=True)

    # 4. First-Mile Access & Equity Deficit
    if eff_walk_m <= 450.0:
        walk_color = "#00e676"
        walk_status = "Meets TMR PTIM 400m Std" if is_en else "符合 TMR PTIM 400m 標準"
    elif eff_walk_m <= 800.0:
        walk_color = "#f59e0b"
        walk_status = "Near 800m Catchment Limit" if is_en else "接近 800m 站點極限"
    else:
        walk_color = "#ff3366"
        walk_status = "Severe First-Mile Deficit" if is_en else "嚴重第一哩赤字 (交通沙漠)"

    with col_k4:
        st.markdown(f"""
        <div class="metric-box" style="border-left-color: {walk_color};">
            <h4 style="margin: 0; color: #fff;">{"First-Mile Access Deficit" if is_en else "第一哩可及性赤字"}</h4>
            <h2 style="margin: 0.3rem 0; color: {walk_color};">{eff_walk_m:.0f} <span style="font-size: 0.95rem; color: #cbd5e1;">m</span></h2>
            <p style="margin: 0; color: {walk_color}; font-size: 0.82rem; font-weight: 600;">{walk_status}</p>
            <p style="margin: 0.2rem 0 0 0; color: #cbd5e1; font-size: 0.85rem;">{"Walk: " if is_en else "徒步 "}{eff_walk_m/84.0:.1f}{" min | 400m Cov: " if is_en else " 分鐘 ｜ 400m 覆蓋: "}{in_cov}%</p>
        </div>
        """, unsafe_allow_html=True)

    # Row 2: Charts (Modal Split vs Pain Radar)
    col_g1, col_g2 = st.columns([1.1, 0.9])
    with col_g1:
        st.markdown("#### " + ("Predicted Commuter Modal Split" if is_en else "全區預測運具分流堆疊分佈"))
        mode_counts = df_sim_res['chosen_mode'].value_counts()
        car_lbl = "Private Car" if is_en else "私家車 (Car)"
        transit_walk_lbl = "Transit (Walk)" if is_en else "徒步公車 (Transit Walk)"
        transit_scoot_lbl = "Transit (E-Scooter)" if is_en else "滑板公車 (Transit Scooter)"
        bike_lbl = "Bicycle" if is_en else "自行車 (Bicycle)"

        df_modes_plot = pd.DataFrame({
            "Mode" if is_en else "運具模式": [car_lbl, transit_walk_lbl, transit_scoot_lbl, bike_lbl],
            "Share (%)" if is_en else "分流佔比 (%)": [car_pct, transit_walk_pct, transit_scoot_pct, bike_pct]
        })
        fig_donut = px.pie(
            df_modes_plot, names="Mode" if is_en else "運具模式", values="Share (%)" if is_en else "分流佔比 (%)",
            hole=0.45,
            color="Mode" if is_en else "運具模式",
            color_discrete_map={
                car_lbl: "#38bdf8",
                transit_walk_lbl: "#00e676",
                transit_scoot_lbl: "#2dd4bf",
                bike_lbl: "#f59e0b"
            }
        )
        fig_donut.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b0e14",
            plot_bgcolor="#161b22",
            font=dict(color="#f8fafc"),
            legend=dict(font=dict(color="#f8fafc", size=12)),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_g2:
        st.markdown("#### " + ("Regional Commuter Impedance Triangle (PPL1 Aversion)" if is_en else "區域通勤三大阻抗維度診斷（PPL1 負向活化）"))
        mean_fatigue = float(df_sim_res['fatigue_pain'].mean())
        mean_delay = float(df_sim_res['delay_pain'].mean())
        mean_cost = float(df_sim_res['cost_pain'].mean())

        # Scale to 0-100 relative index
        fatigue_idx = min(100.0, mean_fatigue * 4.5)
        delay_idx = min(100.0, mean_delay * 5.0)
        cost_idx = min(100.0, mean_cost * 6.5)

        pain_categories = [
            "First-Mile Fatigue" if is_en else "第一哩步行疲勞 (PPL1 Fatigue)",
            "Travel Delay & Waiting" if is_en else "行車停站延遲 (PPL1 Delay)",
            "Out-of-Pocket Expense" if is_en else "購票與養車成本 (PPL1 Cost)"
        ]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[fatigue_idx, delay_idx, cost_idx, fatigue_idx],
            theta=pain_categories + [pain_categories[0]],
            fill='toself',
            fillcolor='rgba(255, 51, 102, 0.35)',
            line=dict(color='#ff3366', width=2),
            name="Pain Level"
        ))
        fig_radar.update_layout(
            template="plotly_dark",
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color="#cbd5e1", gridcolor="#334155", linecolor="#475569"),
                bgcolor="#161b22"
            ),
            paper_bgcolor="#0b0e14",
            font=dict(color="#f8fafc"),
            showlegend=False,
            margin=dict(t=25, b=25, l=25, r=25)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Row 3: TMR 4 Segments Table
    st.markdown("#### " + ("Breakdown by Queensland TMR 4 Commuter Segments" if is_en else "昆士蘭 TMR 四大通勤族群細部決策透視表"))
    seg_breakdown_rows = []
    seg_labels = {
        'CBD': ('CBD 白領族 (CBD Commuters)', 'CBD Commuters'),
        'Suburban': ('跨郊區工薪 (Non-CBD Workers)', 'Non-CBD Workers'),
        'Student': ('大專青年學生 (Tertiary Students)', 'Tertiary Students'),
        'Family': ('育兒接送家庭 (Family Escort)', 'Family Escort')
    }

    for s_code in ['CBD', 'Suburban', 'Student', 'Family']:
        sub_df = df_sim_res[df_sim_res['type'] == s_code]
        if sub_df.empty:
            continue
        s_net_val = sub_df['net_valence'].mean()
        s_car_share = (sub_df['chosen_mode'] == 'Car').mean() * 100.0
        s_transit_share = sub_df['chosen_mode'].str.startswith('Transit').mean() * 100.0
        top_mode = sub_df['chosen_mode'].mode()[0] if not sub_df.empty else 'Car'

        mode_clean = {
            'Car': 'Private Car' if is_en else '私家車',
            'Transit_Walk': 'Transit (Walk)' if is_en else '徒步公車',
            'Transit_Scooter': 'Transit (E-Scooter)' if is_en else '滑板公車',
            'Bicycle': 'Bicycle' if is_en else '自行車'
        }.get(top_mode, top_mode)

        # Main Pain
        f_p = sub_df['fatigue_pain'].mean()
        d_p = sub_df['delay_pain'].mean()
        c_p = sub_df['cost_pain'].mean()
        max_p = max([('Walking Fatigue', f_p), ('Transit Delay', d_p), ('Financial Cost', c_p)], key=lambda x: x[1])[0] if is_en else max([('步行疲勞', f_p), ('行車延遲', d_p), ('金錢花費', c_p)], key=lambda x: x[1])[0]

        seg_breakdown_rows.append({
            "TMR Segment" if is_en else "TMR 通勤族群": seg_labels[s_code][1 if is_en else 0],
            "Pop. Share" if is_en else "樣本佔比": f"{len(sub_df)/len(df_sim_res)*100:.1f}%",
            "Dominant Mode" if is_en else "首選運具模式": mode_clean,
            "Car Share (%)" if is_en else "自駕率 (%)": f"{s_car_share:.1f}%",
            "Transit Share (%)" if is_en else "大眾運輸 (%)": f"{s_transit_share:.1f}%",
            "Net Valence (PAM-PPL1)" if is_en else "神經淨效用 (Net Valence)": f"{s_net_val:+.3f}",
            "Primary Impedance" if is_en else "主要嫌惡阻抗": max_p
        })

    st.dataframe(pd.DataFrame(seg_breakdown_rows), use_container_width=True, hide_index=True)

    # Row 4: Area Diagnostic Summary & Practical Feedback
    st.markdown("#### " + ("Area Diagnostic Summary & Feedback" if is_en else "該區域交通診斷評語"))

    # Identify primary regional pain point
    mean_f = float(df_sim_res['fatigue_pain'].mean())
    mean_d = float(df_sim_res['delay_pain'].mean())
    mean_c = float(df_sim_res['cost_pain'].mean())
    if mean_f >= mean_d and mean_f >= mean_c:
        top_pain_str_zh = "第一哩步行距離過長與酷暑體力負擔"
        top_pain_str_en = "long first-mile walking distance and heat fatigue"
        rx_suggestion_zh = "增設社區接駁公車站牌，或引入共享微移動工具以縮短步行時間"
        rx_suggestion_en = "adding feeder bus stops or introducing shared e-scooters to reduce walking"
    elif mean_d >= mean_f and mean_d >= mean_c:
        top_pain_str_zh = "公車班距等候與尖峰路段車行延誤"
        top_pain_str_en = "bus headway waiting time and traffic delays"
        rx_suggestion_zh = "加密公車尖峰班次，或設置公車專用道進行提速"
        rx_suggestion_en = "increasing peak bus frequency or establishing dedicated bus lanes"
    else:
        top_pain_str_zh = "私家車市中心高額停車費用負擔"
        top_pain_str_en = "high city parking costs for private car drivers"
        rx_suggestion_zh = "維持 50 Cent 低票價誘因，吸引開車族轉乘大眾運輸"
        rx_suggestion_en = "maintaining the 50c transit incentive to encourage drivers to switch"

    if car_pct >= 60.0:
        area_status_zh = f"該區域目前以<b>私家車自駕為主（佔比 {car_pct:.1f}%）</b>。主要受限於平均步行至站點需 <b>{eff_walk_m:.0f} 公尺</b>（約 {eff_walk_m/84.0:.1f} 分鐘）以及 <b>{in_headway:.0f} 分鐘</b> 的公車班距，導致多數有車居民傾向開車。"
        area_status_en = f"This suburb currently has <b>high private car reliance ({car_pct:.1f}% share)</b>. Commuters face an average <b>{eff_walk_m:.0f}m walk</b> ({eff_walk_m/84.0:.1f} min) to transit and <b>{in_headway:.0f}-minute bus headways</b>, so most residents choose private cars."
    elif transit_total_pct >= 50.0:
        area_status_zh = f"該區域<b>大眾運輸成效良好（佔比 {transit_total_pct:.1f}%）</b>。站點平均步行僅 <b>{eff_walk_m:.0f} 公尺</b>，在 50 Cent 票價與高班次頻率下，公共運輸已成為多數居民的首選。"
        area_status_en = f"Public transit is <b>performing well in this area ({transit_total_pct:.1f}% share)</b>. With stops within a short <b>{eff_walk_m:.0f}m walk</b> and 50c fares, transit is the preferred choice for most residents."
    else:
        area_status_zh = f"該區域呈現<b>自駕（{car_pct:.1f}%）與大眾運輸（{transit_total_pct:.1f}%）混合型態</b>。各族群依時間與預算彈性分流，運具結構相對均衡。"
        area_status_en = f"This suburb has a <b>mixed multimodal split</b> between private cars ({car_pct:.1f}%) and transit ({transit_total_pct:.1f}%), with choices distributed across demographics."

    car_users_count = int(suburb_pop * car_pct / 100.0)
    transit_users_count = int(suburb_pop * transit_total_pct / 100.0)

    if is_en:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.75); border: 1px solid #38bdf8; border-radius: 8px; padding: 16px 18px; margin-bottom: 20px;">
            <p style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.6; margin: 0 0 10px 0;">
                {area_status_en}
            </p>
            <p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6; margin: 0;">
                • <b>Road Space Load</b>: Morning peak drivers ({car_users_count:,} cars) occupy about <b>{fifa_soccer_fields:.1f} FIFA soccer fields</b> of roadway.<br>
                • <b>Primary Issue</b>: The main friction is <b>{top_pain_str_en}</b>.<br>
                • <b>Next Steps</b>: Recommended improvement is <b>{rx_suggestion_en}</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.75); border: 1px solid #38bdf8; border-radius: 8px; padding: 16px 18px; margin-bottom: 20px;">
            <p style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.6; margin: 0 0 10px 0;">
                {area_status_zh}
            </p>
            <p style="color: #cbd5e1; font-size: 0.90rem; line-height: 1.6; margin: 0;">
                • <b>道路負擔</b>：早晨 {car_users_count:,} 輛自駕車約佔用 <b>{fifa_soccer_fields:.1f} 座足球場</b> 的車道空間。<br>
                • <b>主要阻抗</b>：居民目前面臨的最大交通阻力為<b>【{top_pain_str_zh}】</b>。<br>
                • <b>改善建議</b>：建議之工程對策為<b>【{rx_suggestion_zh}】</b>。
            </p>
        </div>
        """, unsafe_allow_html=True)
