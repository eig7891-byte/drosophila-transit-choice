"""
Tab 4: 10,000-Commuter Population and Spatial Setup.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from src.simulation import BRISBANE_CORRIDORS

def render_tab4_society_setup(study_data: dict, is_en: bool):
    st.markdown("## " + (" 10,000-Commuter Population & Spatial Setup" if is_en else " 萬人群體架構、載具持有與空間佈局設定"))
    st.markdown(
        "Standard transportation planning models assume unconstrained access to all travel modes. In reality, commuter choices are strictly governed by household vehicle availability and physical urban geography. "
        "Grounded in **Australian Bureau of Statistics (ABS 2021 Census QuickStats: SAL32626)** and **Queensland Department of Transport and Main Roads (TMR)** empirical datasets, "
        "this page documents the three fundamental pillars configured for the 10,000-commuter synthetic population: **Commuter Archetype Profiles**, **Asset Ownership Rates (Choice Set Gating)**, and **Spatial Corridor Layouts**."
        if is_en else
        "傳統交通規劃模型通常預設所有市民皆具備使用所有運具之權利。在真實世界中，通勤決策嚴格受到家戶載具持有狀態與都市實體地理空間之約束。"
        "本頁面完整呈現基於**澳洲統計局 (ABS 2021 Census QuickStats: SAL32626)** 與 **昆士蘭交通與主幹道部 (TMR)** 官方實證人口統計學數據，"
        "為 10,000 名虛擬市民所配置的三大核心基石：**【角色設定】**、**【數據設定 (持有約束)】** 與 **【位置設定 (七大通勤走廊)】**。"
    )

    demographics = study_data.get('demographics', {})
    overall_own = demographics.get('overall_ownership', {'car': 87.8, 'bike': 32.9, 'scooter': 9.5})
    arch_counts = demographics.get('archetype_counts', {'CBD_Professional': 3998, 'Student': 2545, 'Suburban_Worker': 1982, 'Fitness_Enthusiast': 1475})
    arch_own = demographics.get('archetype_ownership', {})
    total_pop = study_data.get('total_commuters_simulated', 10000)

    # -------------------------------------------------------------
    # 1. 角色設定 (Archetype Profiles & Demographics)
    # -------------------------------------------------------------
    st.markdown("### 1. " + ("Archetype Demographics & Physiological Neuromodulators" if is_en else "角色設定：四大通勤原型與神經調控劑初始濃度"))
    st.markdown(
        "10,000 synthetic commuters are drawn from four empirical Brisbane commuter archetypes, each governed by distinct internal neuromodulator concentrations:"
        if is_en else
        "10,000 名合成市民依據布里斯本人口統計學特徵抽樣自四大代表性通勤族群，各具備不同的內在果蠅神經調控劑生理狀態："
    )

    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
    with col_a1:
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.85); border-left: 4px solid #38bdf8; padding: 12px 14px; border-radius: 6px; height: 100%;">
            <h4 style="margin: 0; color: #fff;"> {"CBD Corporate Executive" if is_en else "CBD 高薪專員"}</h4>
            <h2 style="margin: 0.2rem 0; color: #38bdf8;">{arch_counts.get('CBD_Professional', 3998)} {"ppl" if is_en else "人"}</h2>
            <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0;">{"Share: 40.0% of population" if is_en else "佔比：全體人口 40.0%"}</p>
            <hr style="margin: 0.4rem 0; border-color: #334155;">
            <ul style="font-size: 0.82rem; color: #cbd5e1; padding-left: 18px; margin: 0;">
                <li><b>{"NPF (Price Sensitivity)" if is_en else "NPF (省錢渴望)"}</b>: 0.05–0.35 {"(Low)" if is_en else "(低)"}</li>
                <li><b>{"Octopamine (Motor Vigor)" if is_en else "Octopamine (體能)"}</b>: 0.15–0.45</li>
                <li><b>{"Serotonin (Delay Patience)" if is_en else "Serotonin (耐性)"}</b>: 0.10–0.40 {"(Low)" if is_en else "(低)"}</li>
                <li><b>{"PDF (Sleep Debt Pain)" if is_en else "PDF (早起痛苦)"}</b>: 0.60–0.95 {"(Extreme)" if is_en else "(極高)"}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_a2:
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.85); border-left: 4px solid #00e676; padding: 12px 14px; border-radius: 6px; height: 100%;">
            <h4 style="margin: 0; color: #fff;"> {"Tertiary Student" if is_en else "大專院校學生"}</h4>
            <h2 style="margin: 0.2rem 0; color: #00e676;">{arch_counts.get('Student', 2545)} {"ppl" if is_en else "人"}</h2>
            <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0;">{"Share: 25.5% of population" if is_en else "佔比：全體人口 25.5%"}</p>
            <hr style="margin: 0.4rem 0; border-color: #334155;">
            <ul style="font-size: 0.82rem; color: #cbd5e1; padding-left: 18px; margin: 0;">
                <li><b>{"NPF (Price Sensitivity)" if is_en else "NPF (省錢渴望)"}</b>: 0.75–0.98 {"(Extreme)" if is_en else "(極高)"}</li>
                <li><b>{"Octopamine (Motor Vigor)" if is_en else "Octopamine (體能)"}</b>: 0.20–0.50</li>
                <li><b>{"Serotonin (Delay Patience)" if is_en else "Serotonin (耐性)"}</b>: 0.40–0.75 {"(High)" if is_en else "(高)"}</li>
                <li><b>{"PDF (Sleep Debt Pain)" if is_en else "PDF (早起痛苦)"}</b>: 0.30–0.70</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_a3:
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.85); border-left: 4px solid #f59e0b; padding: 12px 14px; border-radius: 6px; height: 100%;">
            <h4 style="margin: 0; color: #fff;"> {"Suburban Worker Family" if is_en else "外圍郊區家庭勞工"}</h4>
            <h2 style="margin: 0.2rem 0; color: #f59e0b;">{arch_counts.get('Suburban_Worker', 1982)} {"ppl" if is_en else "人"}</h2>
            <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0;">{"Share: 19.8% of population" if is_en else "佔比：全體人口 19.8%"}</p>
            <hr style="margin: 0.4rem 0; border-color: #334155;">
            <ul style="font-size: 0.82rem; color: #cbd5e1; padding-left: 18px; margin: 0;">
                <li><b>{"NPF (Price Sensitivity)" if is_en else "NPF (省錢渴望)"}</b>: 0.40–0.70</li>
                <li><b>{"Octopamine (Motor Vigor)" if is_en else "Octopamine (體能)"}</b>: 0.20–0.50</li>
                <li><b>{"Serotonin (Delay Patience)" if is_en else "Serotonin (耐性)"}</b>: 0.30–0.60</li>
                <li><b>{"PDF (Sleep Debt Pain)" if is_en else "PDF (早起痛苦)"}</b>: 0.40–0.75</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_a4:
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.85); border-left: 4px solid #a855f7; padding: 12px 14px; border-radius: 6px; height: 100%;">
            <h4 style="margin: 0; color: #fff;"> {"Fitness Active Cyclist" if is_en else "運動狂熱騎士"}</h4>
            <h2 style="margin: 0.2rem 0; color: #a855f7;">{arch_counts.get('Fitness_Enthusiast', 1475)} {"ppl" if is_en else "人"}</h2>
            <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0;">{"Share: 14.8% of population" if is_en else "佔比：全體人口 14.8%"}</p>
            <hr style="margin: 0.4rem 0; border-color: #334155;">
            <ul style="font-size: 0.82rem; color: #cbd5e1; padding-left: 18px; margin: 0;">
                <li><b>{"NPF (Price Sensitivity)" if is_en else "NPF (省錢渴望)"}</b>: 0.20–0.60</li>
                <li><b>{"Octopamine (Motor Vigor)" if is_en else "Octopamine (體能)"}</b>: 0.80–0.98 {"(Extreme)" if is_en else "(極高)"}</li>
                <li><b>{"Serotonin (Delay Patience)" if is_en else "Serotonin (耐性)"}</b>: 0.40–0.70</li>
                <li><b>{"PDF (Sleep Debt Pain)" if is_en else "PDF (早起痛苦)"}</b>: 0.05–0.35 {"(Early Riser)" if is_en else "(耐早起)"}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 2. 數據設定 (Asset Ownership & Choice Set Gating)
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 2. " + ("Data Settings: Asset Ownership Benchmarks & Choice Set Gating" if is_en else "數據設定：載具持有率基準與選擇集合閘控規則"))

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"""
        <div class="metric-box" style="border-left-color: #38bdf8;">
            <h4 style="margin: 0; color: #fff;"> {"Car Ownership Access" if is_en else "私家車全境可用率"}</h4>
            <h2 style="margin: 0.3rem 0; color: #38bdf8;">{overall_own.get('car', 87.8):.1f}%</h2>
            <p style="margin: 0; color: #cbd5e1; font-size: 0.85rem;">{"ABS Census 2021 (Springwood: 2.2 cars/dwelling)" if is_en else "ABS 2021 人口普查 (Springwood 平均每戶 2.2 輛車)"}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="metric-box" style="border-left-color: #f59e0b;">
            <h4 style="margin: 0; color: #fff;"> {"Bicycle Ownership Rate" if is_en else "自行車活躍持有率"}</h4>
            <h2 style="margin: 0.3rem 0; color: #f59e0b;">{overall_own.get('bike', 32.9):.1f}%</h2>
            <p style="margin: 0; color: #cbd5e1; font-size: 0.85rem;">{"Austroads QLD Survey (Fitness 91.7%, Suburban 17.2%)" if is_en else "Austroads 昆士蘭報告 (運動族 91.7%，郊區勞工僅 17.2%)"}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div class="metric-box" style="border-left-color: #2dd4bf;">
            <h4 style="margin: 0; color: #fff;"> {"E-Scooter Ownership Rate" if is_en else "私人電動滑板車持有率"}</h4>
            <h2 style="margin: 0.3rem 0; color: #2dd4bf;">{overall_own.get('scooter', 9.5):.1f}%</h2>
            <p style="margin: 0; color: #cbd5e1; font-size: 0.85rem;">{"TMR E-mobility Report (No shared fleets in outer suburbs)" if is_en else "TMR 微移動評估 (外圍郊區無商業共享滑板車租賃站)"}</p>
        </div>
        """, unsafe_allow_html=True)

    col_own_chart, col_gating_box = st.columns([1.1, 0.9])
    with col_own_chart:
        arch_names = ['Student', 'CBD_Professional', 'Suburban_Worker', 'Fitness_Enthusiast']
        arch_labels = ['大學生', 'CBD 白領', '郊區勞工', '運動狂熱者'] if not is_en else ['Student', 'CBD Exec', 'Suburban', 'Cyclist']
        car_rates = [arch_own.get('has_car', {}).get(a, 0.0) for a in arch_names]
        bike_rates = [arch_own.get('has_bike', {}).get(a, 0.0) for a in arch_names]
        scooter_rates = [arch_own.get('has_scooter', {}).get(a, 0.0) for a in arch_names]

        df_own = pd.DataFrame({
            'Archetype' if is_en else '通勤群體': arch_labels * 3,
            'Rate (%)' if is_en else '持有率 (%)': car_rates + bike_rates + scooter_rates,
            'Asset' if is_en else '載具類型': (['Car' if is_en else '私家車'] * 4) + (['Bicycle' if is_en else '自行車'] * 4) + (['E-Scooter' if is_en else '電動滑板車'] * 4)
        })
        fig_own = px.bar(
            df_own, x='Archetype' if is_en else '通勤群體', y='Rate (%)' if is_en else '持有率 (%)',
            color='Asset' if is_en else '載具類型', barmode='group',
            color_discrete_map={
                'Car': '#38bdf8', '私家車': '#38bdf8',
                'Bicycle': '#f59e0b', '自行車': '#f59e0b',
                'E-Scooter': '#2dd4bf', '電動滑板車': '#2dd4bf'
            },
            title="Asset Ownership Rate by Commuter Archetype" if is_en else "四大通勤群體載具持有率分佈矩陣"
        )
        fig_own.update_layout(
            template="plotly_dark",
            paper_bgcolor='#0e1117',
            plot_bgcolor='#161b22',
            font=dict(color='#f8fafc'),
            legend=dict(
                title=dict(text="Asset" if is_en else "載具類型", font=dict(color="#f8fafc", size=12)),
                font=dict(color="#f8fafc", size=12),
                bgcolor="rgba(15, 23, 42, 0.85)",
                bordercolor="#334155",
                borderwidth=1
            ),
            xaxis=dict(title_font=dict(color="#f8fafc"), tickfont=dict(color="#cbd5e1"), gridcolor="#1e293b"),
            yaxis=dict(title_font=dict(color="#f8fafc"), tickfont=dict(color="#cbd5e1"), gridcolor="#1e293b"),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_own, use_container_width=True)

    with col_gating_box:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.75); border: 1px solid #38bdf8; border-radius: 8px; padding: 16px; height: 100%;">
            <h5 style="color: #38bdf8; margin: 0 0 8px 0;"> {"Choice Set Availability Gating Protocol" if is_en else "選擇集合可用性閘控規則 (Availability Gating)"}</h5>
            <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.6; margin: 0;">
                {"1. <b>Car Gating</b>: Commuters without car ownership cannot select <code>Car</code>.<br>"
                 "2. <b>Micro-Mobility Gating</b>: 90.5% without e-scooters have <code>Transit_Scooter</code> purged from their menu. Their sole transit choice is <code>Transit_Walk</code> (walking up to 2.2 km to the station).<br>"
                 "3. <b>Bicycle Gating</b>: Commuters without a functional bike cannot select <code>Bicycle</code>.<br>"
                 "4. <b>Behavioral Impact</b>: In outer suburbs where 95.6% own cars and walking distances exceed 1.8 km, commuters lacking scooters face severe PPL1 heat-fatigue penalties, causing massive diversion into private cars." if is_en else
                 "1. <b>汽車閘控</b>：未持有汽車者，選單嚴禁出現 <code>自駕車 (Car)</code>。<br>"
                 "2. <b>微移動閘控</b>：90.5% 無滑板車市民，選單徹底封鎖 <code>滑板接駁公車 (Transit_Scooter)</code>。欲搭乘大眾運輸唯一合法途徑為徒步走至車站 (Transit_Walk)。<br>"
                 "3. <b>自行車閘控</b>：未持有單車者，選單嚴禁出現 <code>自行車 (Bicycle)</code>。<br>"
                 "4. <b>行為效應</b>：在外圍郊區，因高達 95.6% 擁車且第一哩步行長達 1.8–2.2 公里，缺乏滑板車的市民在酷暑步行懲罰下被迫倒向開車。"}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 3. 位置設定 (Spatial Locations & 7 Corridors)
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 3. " + ("Spatial Settings: 7 Representative Greater Brisbane Commute Corridors" if is_en else "位置設定：大布里斯本都會區七大代表性通勤走廊佈局"))
    st.markdown(
        "To capture urban spatial heterogeneity, the 10,000 commuters are distributed across seven real-world corridors covering inner-ring, middle-ring, and outer-suburban catchments:"
        if is_en else
        "為精確捕捉布里斯本都會區的空間異質性，10,000 名虛擬市民被均勻抽樣分佈於涵蓋內環、中環與外圍郊區的七大實體通勤走廊（每走廊約 1,400 人）："
    )

    if is_en:
        corridor_data = [
            {"Corridor": "Carindale to CBD", "Sector": "Eastern", "Trip Distance": "11.0 km", "First-Mile Walk": "400 m", "Car Time": "28 min", "Transit Time": "48 min", "Key Transit Spine": "Eastern Busway Arterial (Routes 200, 222)"},
            {"Corridor": "Indooroopilly to CBD", "Sector": "Western", "Trip Distance": "7.2 km", "First-Mile Walk": "600 m", "Car Time": "22 min", "Transit Time": "35 min", "Key Transit Spine": "Western Freeway / Coronation Dr (Routes 444, 430)"},
            {"Corridor": "Chermside to CBD", "Sector": "Northern", "Trip Distance": "10.5 km", "First-Mile Walk": "800 m", "Car Time": "30 min", "Transit Time": "50 min", "Key Transit Spine": "Northern Busway / Gympie Rd (Routes 333, 340)"},
            {"Corridor": "Mt Gravatt to CBD", "Sector": "South-East Core", "Trip Distance": "13.8 km", "First-Mile Walk": "1,500 m", "Car Time": "35 min", "Transit Time": "55 min", "Key Transit Spine": "South East Busway (Routes 111, 150)"},
            {"Corridor": "Logan Central to CBD", "Sector": "Outer South", "Trip Distance": "26.5 km", "First-Mile Walk": "1,800 m", "Car Time": "45 min", "Transit Time": "85 min", "Key Transit Spine": "Beenleigh Rail Line / Route 555 Express Bus"},
            {"Corridor": "Springwood to Rochedale South", "Sector": "Outer Local Catchment (Scenario A)", "Trip Distance": "5.2 km", "First-Mile Walk": "2,200 m", "Car Time": "8.5 min", "Transit Time": "20 min", "Key Transit Spine": "Suburban Feeder Bus (Routes 574, 575)"},
            {"Corridor": "Springwood to UQ St Lucia", "Sector": "Outer University Corridor (Scenario B)", "Trip Distance": "28.8 km", "First-Mile Walk": "2,200 m", "Car Time": "38 min", "Transit Time": "42 min", "Key Transit Spine": "555 Express Bus to 66 via Eleanor Schonell Bridge"}
        ]
    else:
        corridor_data = [
            {"走廊名稱 (Corridor)": "Carindale to CBD", "區位 (Sector)": "東區 (Eastern)", "單程里程": "11.0 km", "第一哩步行": "400 m", "自駕時間": "28 min", "公車時間": "48 min", "主要大眾運輸路網": "Eastern Busway 幹線 (200, 222 路)"},
            {"走廊名稱 (Corridor)": "Indooroopilly to CBD", "區位 (Sector)": "西區 (Western)", "單程里程": "7.2 km", "第一哩步行": "600 m", "自駕時間": "22 min", "公車時間": "35 min", "主要大眾運輸路網": "Western Freeway / Coronation Dr (444, 430 路)"},
            {"走廊名稱 (Corridor)": "Chermside to CBD", "區位 (Sector)": "北區 (Northern)", "單程里程": "10.5 km", "第一哩步行": "800 m", "自駕時間": "30 min", "公車時間": "50 min", "主要大眾運輸路網": "Northern Busway / Gympie Rd (333, 340 路)"},
            {"走廊名稱 (Corridor)": "Mt Gravatt to CBD", "區位 (Sector)": "南區核心 (South-East)", "單程里程": "13.8 km", "第一哩步行": "1,500 m", "自駕時間": "35 min", "公車時間": "55 min", "主要大眾運輸路網": "South East Busway (111, 150 路)"},
            {"走廊名稱 (Corridor)": "Logan Central to CBD", "區位 (Sector)": "外圍深南區 (Outer South)", "單程里程": "26.5 km", "第一哩步行": "1,800 m", "自駕時間": "45 min", "公車時間": "85 min", "主要大眾運輸路網": "Beenleigh 鐵路支線 / 555 快速公車"},
            {"走廊名稱 (Corridor)": "Springwood to Rochedale South", "區位 (Sector)": "外圍短途生活圈 (Scenario A)", "單程里程": "5.2 km", "第一哩步行": "2,200 m", "自駕時間": "8.5 min", "公車時間": "20 min", "主要大眾運輸路網": "郊區接駁公車 (574, 575 路)"},
            {"走廊名稱 (Corridor)": "Springwood to UQ St Lucia", "區位 (Sector)": "外圍跨區通學 (Scenario B)", "單程里程": "28.8 km", "第一哩步行": "2,200 m", "自駕時間": "38 min", "公車時間": "42 min", "主要大眾運輸路網": "555 快速公車轉 66 路 Eleanor Schonell Bridge"}
        ]
    st.dataframe(pd.DataFrame(corridor_data), use_container_width=True, hide_index=True)

    # Visualizing the distance to transit gradient
    df_corr_plot = pd.DataFrame([
        {"Corridor": c.name.split(' (')[0], "Distance_km": c.distance_km, "Walk_m": c.distance_to_transit_m, "Car_time": c.car_travel_time_min, "Transit_time": c.transit_travel_time_min}
        for c in BRISBANE_CORRIDORS
    ])
    fig_corr = px.scatter(
        df_corr_plot, x="Distance_km", y="Walk_m", size="Transit_time", color="Walk_m",
        text="Corridor", color_continuous_scale="Viridis",
        labels={"Distance_km": "Corridor Trip Distance (km)" if is_en else "單程物理里程 (km)", "Walk_m": "Distance to Busway Station (m)" if is_en else "第一哩車站步行距離 (m)"},
        title="Spatial Gradient: First-Mile Walking Distance vs Total Trip Length" if is_en else "七大走廊空間梯度：第一哩車站步行距離 vs 總通勤里程"
    )
    fig_corr.update_traces(textposition='top right', marker=dict(size=16, line=dict(width=1, color='white')))
    fig_corr.update_layout(
        template="plotly_dark",
        paper_bgcolor='#0e1117',
        plot_bgcolor='#161b22',
        font=dict(color='#f8fafc'),
        coloraxis_colorbar=dict(title=dict(font=dict(color="#f8fafc")), tickfont=dict(color="#cbd5e1")),
        xaxis=dict(title_font=dict(color="#f8fafc"), tickfont=dict(color="#cbd5e1"), gridcolor="#1e293b"),
        yaxis=dict(title_font=dict(color="#f8fafc"), tickfont=dict(color="#cbd5e1"), gridcolor="#1e293b"),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_corr, use_container_width=True)


    # -------------------------------------------------------------
