"""
Tab 2: Empirical Grounding, Data Sources, and Policy Context
============================================================
Mirrors Chapter 2 of reports/brisbane_transit_report_en.md:
- 2.1 Official Data Sources and Provenance
- 2.2 Corridor Selection Rationale: The Two Springwood Corridors
- 2.3 Policy Evaluation Window (2024-2026)
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px

def render_tab2_grounding(is_en: bool):
    st.markdown("## " + ("Chapter 2: Empirical Grounding, Data Sources & Policy Context" if is_en else "第二章：實證大數據來源、走廊選取依據與政策背景"))
    st.markdown(
        "Grounding the Drosophila Connectome Model into official empirical transport records, big data smart card transactions, and the 2024–2026 Queensland public transport policy timeline."
        if is_en else
        "本章節展示果蠅連接體模型如何紮根於昆士蘭官方實證大數據、數千萬筆智慧卡刷卡記錄，以及 2024–2026 年昆士蘭大眾交通重大政策變革脈絡。"
    )

    # -------------------------------------------------------------------------
    # 2.1 Official Data Sources and Provenance
    # -------------------------------------------------------------------------
    st.markdown("### 2.1 " + ("Official Data Sources and Provenance" if is_en else "官方實證數據來源與科學溯源憑證"))
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Go Card Smart Card Big Data" if is_en else "Go Card 刷卡大數據", "24,772,971", "July vs August 2024" if is_en else "2024 年 7-8 月對比")
    with col_m2:
        st.metric("Longitudinal Patronage" if is_en else "歷程季度客運量", "424 Quarters" if is_en else "424 季度紀錄", "2014 - 2026 (12 Years)" if is_en else "跨度 12 年")
    with col_m3:
        st.metric("TransLink Quarterly Report" if is_en else "TransLink 官方季報", "37 Worksheets" if is_en else "37 張工作表", "Q2 2025-26 Official" if is_en else "Q2 2025-26 官方認證")
    with col_m4:
        st.metric("Outer Suburb Car Ownership" if is_en else "外圍郊區車輛持有率", "95.2%", "ABS 2021 Census (Springwood)" if is_en else "澳洲統計局人口普查")

    data_sources_table = [
        {
            "Dataset / Record" if is_en else "官方資料庫 / 紀錄": "TransLink Origin-Destination Trips (Queensland Open Data)",
            "Coverage / Size" if is_en else "涵蓋範圍 / 筆數": "24.8M Origin-Destination transactions (Jul–Aug 2024)",
            "Role in Model" if is_en else "模型中之用途": "Calibrates baseline mode share and empirical route ridership elasticity",
            "Official Source / Link" if is_en else "認證網址": "data.qld.gov.au/dataset/translink-origin-destination-trips-2022-onwards"
        },
        {
            "Dataset / Record" if is_en else "官方資料庫 / 紀錄": "Translink Division Performance Reports & Dashboard",
            "Coverage / Size" if is_en else "涵蓋範圍 / 筆數": "Quarterly records across Bus, Train, Ferry, Tram (2014-2026)",
            "Role in Model" if is_en else "模型中之用途": "Provides long-term post-COVID trends and 50c policy era benchmarking",
            "Official Source / Link" if is_en else "認證網址": "translink.com.au/about-translink/reports-and-publications/performance"
        },
        {
            "Dataset / Record" if is_en else "官方資料庫 / 紀錄": "PT Performance & Accessibility Report (Q2 2025-26)",
            "Coverage / Size" if is_en else "涵蓋範圍 / 筆數": "37 worksheets, 4,209 rows of OTR reliability and CE satisfaction",
            "Role in Model" if is_en else "模型中之用途": "Ground truth for on-time running (OTR) and passenger experience",
            "Official Source / Link" if is_en else "認證網址": "tmr.qld.gov.au/business-industry/Technical-standards-publications"
        },
        {
            "Dataset / Record" if is_en else "官方資料庫 / 紀錄": "Australian Bureau of Statistics (ABS 2021 Census)",
            "Coverage / Size" if is_en else "涵蓋範圍 / 筆數": "Springwood SAL32635 demographic & vehicle profile",
            "Role in Model" if is_en else "模型中之用途": "Grounds 10,000-agent demographic asset gating (95.2% car ownership)",
            "Official Source / Link" if is_en else "認證網址": "abs.gov.au/census/find-census-data/quickstats/2021/SAL32635"
        },
        {
            "Dataset / Record" if is_en else "官方資料庫 / 紀錄": "FlyWire Whole-Brain Connectome (Nature 2024)",
            "Coverage / Size" if is_en else "涵蓋範圍 / 筆數": "138,327 neurons, 130M+ synapses (FAFB release v783)",
            "Role in Model" if is_en else "模型中之用途": "Biologically grounds PAM reward, PPL1 pain, and central complex compass",
            "Official Source / Link" if is_en else "認證網址": "doi.org/10.1038/s41586-024-07558-y"
        }
    ]
    st.table(pd.DataFrame(data_sources_table))

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 2.2 Corridor Selection Rationale
    # -------------------------------------------------------------------------
    st.markdown("### 2.2 " + ("Corridor Selection Rationale: The Two Springwood Corridors" if is_en else "走廊選取科學依據：兩條對稱且極端的 Springwood 走廊"))
    st.markdown(
        "To test modal elasticity under extreme conditions, the model selected two structurally contrasting commute corridors sharing the same origin (**Springwood, southern outer suburb, 21km from CBD**):"
        if is_en else
        "為了在極端條件下驗證模型之決策彈性，研究特意選取起點相同（**Springwood，布里斯本外環南區，距 CBD 21 公里**）但結構完全相反的兩條走廊："
    )

    c_box1, c_box2 = st.columns(2)
    with c_box1:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 5px solid #ff5252; border-radius: 8px; padding: 16px; height: 100%;">
            <h4 style="margin-top: 0; color: #ff5252;"> Corridor 1: Springwood to Rochedale South (5.24 km)</h4>
            <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.55;">
                <b>Role in Evaluation</b>: Outer Suburb Feeder Test.<br>
                <b>Physical Setup</b>: Low-density residential streets, free parking at shopping plazas, driving takes only 8.5 minutes.<br>
                <b>Crucial Barrier</b>: Taking the bus requires an unshaded <b>2,200m walking access</b> and takes 20 minutes.<br>
                <b>Hypothesis</b>: In subtropical heat, will a $3.05 fare cut ($3.55 -> $0.50) convince suburban drivers to walk 2.2 km?
            </p>
        </div>
        """ if is_en else """
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 5px solid #ff5252; border-radius: 8px; padding: 16px; height: 100%;">
            <h4 style="margin-top: 0; color: #ff5252;"> 走廊 1：Springwood 至 Rochedale South（5.24 km）</h4>
            <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.55;">
                <b>評估目的</b>：外環生活圈微觀抗性測試。<br>
                <b>物理特徵</b>：低密度住宅區、目的地免費停車、自駕僅需 8.5 分鐘。<br>
                <b>致命阻抗</b>：搭公車需在無遮蔭處<b>徒步步行 2,200 公尺接駁</b>，公車需耗時 20 分鐘。<br>
                <b>核心假設</b>：在亞熱帶高溫下，省下 $3.05 票價（$3.55 降至 $0.50）能否說服車主走 2.2 公里？
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c_box2:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 5px solid #00e676; border-radius: 8px; padding: 16px; height: 100%;">
            <h4 style="margin-top: 0; color: #00e676;"> Corridor 2: Springwood to UQ St Lucia (28.78 km)</h4>
            <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.55;">
                <b>Role in Evaluation</b>: Long-Distance Multimodal Trunk Test.<br>
                <b>Physical Setup</b>: Operates along the grade-separated South East Busway, terminating at UQ Lakes.<br>
                <b>Economic Inversion</b>: Campus parking is prohibitive (<b>$26.50/day</b> total cost). Fares dropped 91.9% ($6.16 -> $0.50).<br>
                <b>Infrastructure Boost</b>: Brisbane Metro dedicated busway routing cuts travel time by <b>30%</b> (42 min -> 29.4 min).
            </p>
        </div>
        """ if is_en else """
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 5px solid #00e676; border-radius: 8px; padding: 16px; height: 100%;">
            <h4 style="margin-top: 0; color: #00e676;"> 走廊 2：Springwood 至昆士蘭大學 UQ（28.78 km）</h4>
            <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.55;">
                <b>評估目的</b>：長途多運具幹線大動脈測試。<br>
                <b>物理特徵</b>：行經全立體交叉南區公車專用道（South East Busway），終點為 UQ Lakes 湖畔站。<br>
                <b>經濟反轉</b>：校園停車費高昂（每日總成本 <b>$26.50 AUD</b>），單程票價暴跌 91.9%（$6.16 降至 $0.50）。<br>
                <b>基建提速</b>：Brisbane Metro 專用隧道使行程時間<b>大幅縮短 30%</b>（42 分鐘降至 29.4 分鐘）。
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 2.3 Policy Evaluation Window
    # -------------------------------------------------------------------------
    st.markdown("### 2.3 " + ("Why the 2024–2026 Policy Evaluation Window?" if is_en else "為何鎖定 2024–2026 年政策評估窗口？"))
    
    timeline_steps = [
        {"階段 (Phase)": "1. 政策前基準期 (Pre-Policy)", "時間 (Timeline)": "2024 年 7 月以前", "政策狀態": "舊制多區間里程計費 ($3.55 - $6.16+ AUD)", "系統特徵": "後疫情客流平穩恢復，自駕車佔比高達 73% (外環)。"},
        {"階段 (Phase)": "2. 50-Cent 試辦上路 (50c Trial)", "時間 (Timeline)": "2024 年 8 月 5 日", "政策狀態": "全東南昆士蘭跨區一律 50 Cent", "系統特徵": "刷卡交易暴增 127 萬筆，專用道公車尖峰迅速滿載。"},
        {"階段 (Phase)": "3. Brisbane Metro 專用道啟用", "時間 (Timeline)": "2024 年 10 月 - 2025 年", "政策狀態": "Metro Line 1 & Line 2 雙節電車投入", "系統特徵": "隧道專用路權提速 30%，單車運能提升至 170 人。"},
        {"階段 (Phase)": "4. 政策永久化與常態化", "時間 (Timeline)": "2025 年 2 月 - 2026 年", "政策狀態": "昆士蘭州議會通過 50-Cent 永久實施", "系統特徵": "乘客滿意度破紀錄 (Cost 滿意度 4.88/5)，確立世界級低票價樣本。"}
    ] if not is_en else [
        {"Phase": "1. Pre-Policy Baseline", "Timeline": "Prior to July 2024", "Policy State": "Zonal Distance-Based Tariff ($3.55 - $6.16+ AUD)", "Network Impact": "Stable post-COVID recovery; outer suburban car share ~73%."},
        {"Phase": "2. 50-Cent Trial Launch", "Timeline": "5 August 2024", "Policy State": "Flat $0.50 AUD across all SEQ zones", "Network Impact": "Go Card trips surged by 1.27M in Month 1; busways hit peak crush loads."},
        {"Phase": "3. Brisbane Metro Deployment", "Timeline": "Oct 2024 - 2025", "Policy State": "Metro Line 1 & Line 2 (24m electric bi-articulated)", "Network Impact": "30% travel time reduction via tunnels; vehicle capacity up to 170 passengers."},
        {"Phase": "4. Permanent Policy Legislation", "Timeline": "Feb 2025 - 2026", "Policy State": "Queensland Parliament made 50c permanent", "Network Impact": "Survey satisfaction peaked (4.88/5 on cost); establishes gold-standard dataset."}
    ]
    st.table(pd.DataFrame(timeline_steps))
