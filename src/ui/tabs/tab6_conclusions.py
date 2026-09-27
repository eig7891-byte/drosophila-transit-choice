"""
Tab 6: Engineering Conclusions and Strengths of the Drosophila Connectome Model
==============================================================================
Mirrors Chapter 6 of reports/brisbane_transit_report_en.md:
- 6.1 Main Findings
- 6.2 Critical Divergence: Weekday Morning Peak vs. Gross Annual Ridership (The Compensatory Error)
- 6.3 Core Strengths of the Drosophila Connectome Framework
- 6.4 Honest Engineering Limitations and Future Roadmap
- 6.5 10,000-Agent Macro Policy Scenario Simulation Results
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px

def render_tab6_conclusions(study_data: dict, is_en: bool):
    st.markdown("## " + ("Chapter 6: Engineering Conclusions & Model Strengths" if is_en else "第六章：交通工程總結、模型優勢與偏誤診斷"))
    st.markdown(
        "Synthesizing the core findings across all 4 corridors, unpacking the **Compensatory Error** in traditional models, evaluating macro policy scenarios, and outlining honest engineering limitations."
        if is_en else
        "彙整四大走廊的關鍵實證結論，深度拆解傳統模型的「補償性預測偏誤」，呈現萬人微觀模擬四大政策情境之宏觀效益，並誠實剖析模型的工程界限與未來展望。"
    )

    # -------------------------------------------------------------------------
    # 6.1 Main Findings
    # -------------------------------------------------------------------------
    st.markdown("### 6.1 " + ("Main Findings Across All Tested Corridors" if is_en else "四大走廊核心實證結論"))
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 5px solid #00e676; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;">
            <h5 style="color: #00e676; margin: 0 0 6px 0;">1. Definitive Proof Against Overfitting</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.55;">
                With 100% frozen synaptic weights, the model predicted +22.96% on Route 60 (vs +25.0% official) and +58.40% on Route 66 (vs +60.71% council records), proving genuine generalizability across diverse corridors without back-fitting.
            </p>
        </div>
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 5px solid #38bdf8; border-radius: 8px; padding: 14px 18px;">
            <h5 style="color: #38bdf8; margin: 0 0 6px 0;">2. Exceptional Accuracy on Multimodal Trunks</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.55;">
                On Route 2 (Springwood to UQ), combining a 91.9% fare cut, $26.50 parking fee avoidance, and Metro 30% speedup produced +8.53 pp in the model vs +8.50 pp in real counts (error only 0.03 pp).
            </p>
        </div>
        """ if is_en else """
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 5px solid #00e676; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;">
            <h5 style="color: #00e676; margin: 0 0 6px 0;">1. 徹底排除「過度擬合」疑慮 (Proof Against Overfitting)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.55;">
                在神經權重完全凍結下，Route 60 預測 +22.96%（實測 +25.0%）、Route 66 預測 +58.40%（市議會公布 +60.71%），證實模型具備卓越的泛化預測力。
            </p>
        </div>
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 5px solid #38bdf8; border-radius: 8px; padding: 14px 18px;">
            <h5 style="color: #38bdf8; margin: 0 0 6px 0;">2. 長途多運具幹線高精度吻合 (Trunk Accuracy)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.55;">
                在 Springwood 至 UQ 幹線上，91.9% 票價暴跌、Metro 專用道提速 30% 與規避 $26.50 停車費，果蠅模型以 +8.53 pp 完美命中真實世界 +8.50 pp（誤差僅 0.03 個百分點）。
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_f2:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 5px solid #ff5252; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;">
            <h5 style="color: #ff5252; margin: 0 0 6px 0;">3. Suburban Driver Resistance to Cheap Fares</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.55;">
                On Route 1, reducing fares from $3.55 to $0.50 shifted transit share by only +0.66 pp (+3.75%). TMR's linear formula severely overpredicted (+31.9%), failing to recognize that suburban car drivers refuse to walk 2.2 km in Queensland heat.
            </p>
        </div>
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 5px solid #a855f7; border-radius: 8px; padding: 14px 18px;">
            <h5 style="color: #a855f7; margin: 0 0 6px 0;">4. Infrastructure Outperforms Fares for Drivers</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.55;">
                Dropping fares converts budget-constrained students, but leaves half of suburban commuters driving. Rapid transit speedups via dedicated busways generate 2.6x higher mode shift among car-owning commuters than fare discounts alone.
            </p>
        </div>
        """ if is_en else """
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 5px solid #ff5252; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;">
            <h5 style="color: #ff5252; margin: 0 0 6px 0;">3. 郊區車主對低票價之自駕抗拒 (Suburban Car Resistance)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.55;">
                在走廊 1 上，降價至 50c 僅帶來 +0.66 pp（+3.75%）微弱分流。TMR 線性模型嚴重高估（+31.88%），完全忽視了 2,200 公尺高溫步行對開車族的巨大阻抗。
            </p>
        </div>
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 5px solid #a855f7; border-radius: 8px; padding: 14px 18px;">
            <h5 style="color: #a855f7; margin: 0 0 6px 0;">4. 專用道提速效益遠勝單純票價補貼 (Speed > Fares)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.55;">
                票價補貼主要吸引學生與無車族；對有車上班族而言，專用路權提速 30% 帶來的轉移效應是單純票價折扣的 <b>2.6 倍</b>。
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 6.2 The Compensatory Error Deep-Dive
    # -------------------------------------------------------------------------
    st.markdown("### 6.2 " + ("Critical Divergence: The Compensatory Error in Traditional Models" if is_en else "關鍵分歧：傳統交通模型的「補償性預測偏誤」機理診斷"))
    st.markdown("""
    ```
    ┌────────────────────────────────────────────────────────────────────────┐
    │                        THE COMPENSATORY ERROR                          │
    ├────────────────────────────────────────────────────────────────────────┤
    │  TRADITIONAL LINEAR LOGIT (TMR BSTM-MM):                               │
    │  • Overpredicts AM Peak Shift: Assumes motorists shift en masse (+56%) │
    │  • Underpredicts Off-Peak Leisure: Assumes flat linear elasticity      │
    │  • Net Result: Reaches ~40% gross annual growth via offsetting errors  │
    │                                                                        │
    │  DROSOPHILA CONNECTOME MODEL (REALITY MATCH):                          │
    │  • AM Peak Commuter Shift is Capped: +32.35% growth (+8.53 pp)         │
    │    -> Limited by car ownership habits and morning busway seat capacity │
    │  • Off-Peak & Weekend Leisure Surges: +60% to +160% weekend night trips │
    │  • Net Result: Correctly isolates the physical limits of morning peak  │
    └────────────────────────────────────────────────────────────────────────┘
    ```
    """ if is_en else """
    ```
    ┌────────────────────────────────────────────────────────────────────────┐
    │                    傳統交通模型的「補償性預測偏誤」診斷                │
    ├────────────────────────────────────────────────────────────────────────┤
    │  昆士蘭交通局傳統線性模型 (TMR BSTM-MM)：                              │
    │  • 早尖峰嚴重過度高估：盲目假設自駕上班族會集體棄車 (+36% ~ +56%)      │
    │  • 離峰與夜間嚴重低估：忽略夜間 Uber 加價與社交誘因，套用同一平淡彈性 │
    │  • 總結算假象：全年總量靠著「一邊高估、一邊低估」互相抵消達到 ~40%    │
    │                                                                        │
    │  果蠅大腦連接體模型 (Drosophila Connectome - 吻合真實)：               │
    │  • 早尖峰硬性封頂：增幅受限於專用道物理座位與私家車慣性 (+25.7% ~ 32%) │
    │  • 週末與夜間爆發：精準推導出夜間規避加價 Uber 誘發之 +105% ~ +160%   │
    │  • 總結算真理：完全符合布里斯本市議會官方公布之 M2 全年 +60.71% 實績   │
    └────────────────────────────────────────────────────────────────────────┘
    ```
    """)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 6.4 Honest Engineering Limitations
    # -------------------------------------------------------------------------
    st.markdown("### 6.4 " + ("Honest Engineering Trade-offs and Limitations of Our Method" if is_en else "專業工程師的自我審計：我們模型的局限與工程挑戰"))
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.markdown("""
        * **1. Regional Network Scalability**:
          * BSTM-MM assigns 20,000 regional road links in 1-2 hours via static matrix equilibrium.
          * Simulating 2.5M individual neural agent brains with stochastic Monte Carlo across every street has high computational complexity. The Drosophila model is built for corridor-level and policy-level diagnosis, not regional network assignment.
        * **2. Dynamic Traffic Feedback Loops**:
          * Current corridor travel times are exogenous engineering inputs.
          * When 1,000 commuters shift to transit, highway congestion drops and driving becomes faster (rebound effect). Our model does not yet include dynamic real-time traffic flow loop feedback.
        """ if is_en else """
        * **1. 全路網計算規模瓶頸 (Scalability)**：
          * 傳統 BSTM-MM 能在 1–2 小時內完成全東南昆士蘭 20,000 條道路的靜態均衡指派。
          * 蒙地卡羅個體微觀神經模擬若要擴展至全布里斯本 250 萬人口的每一條街道，運算複雜度極高。本模型定位於**重點走廊與重大政策之定點深度診斷**，非取代宏觀長程路網底層。
        * **2. 缺乏動態交通流反饋 (Traffic Feedback Loop)**：
          * 目前走廊行車時間為外生固定參數。
          * 當大量車主改搭公車，公路變順暢可能誘發部分人回流開車（反彈效應 Rebound Effect）。本模型尚未與動態交通微觀模擬器（如 Aimsun/SUMO）即時閉環反饋。
        """)

    with col_l2:
        st.markdown("""
        * **3. Institutional Review & Acceptance**:
          * Government transport departments operate under statutory guidelines (ATAP, Austroads).
          * Proposing a biological connectome requires extensive peer-reviewed proof that insect dopamine reinforcement learning maps directly to microeconomic discrete choice principles.
        * **4. Geographic Re-Calibration**:
          * Transferring to Sydney or Melbourne requires re-running Bayesian MAP calibration against local smart card data due to climate and demographic differences.
        """ if is_en else """
        * **3. 行政審查與制度接受度 (Institutional Acceptance)**：
          * 官方交通局依循法定準則（如 ATAP 準則與 Austroads 手冊）。
          * 向公務體系證明「昆蟲多巴胺迴路就是前景理論的生理實現」需要花費顯著的學術溝通與審查成本。
        * **4. 跨城市參數可轉移性 (Transferability)**：
          * 若要轉移至雪梨或墨爾本，因氣候（無昆士蘭酷暑）與生活習慣不同，需以當地智慧卡大數據重新進行 Bayesian MAP 校準。
        """)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 6.5 Macro Policy Simulation Results (10,000 Commuters)
    # -------------------------------------------------------------------------
    st.markdown("### 6.5 " + ("10,000-Commuter Macro Policy Scenario Simulation Results" if is_en else "萬人微型社會四大交通政策情境模擬成果"))
    
    scenarios = study_data.get('scenarios', {})
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
        if key in scenarios:
            data = scenarios[key]
            shares = data.get('mode_shares', {})
            m_counts = data.get('mode_counts', {})
            with col:
                st.markdown(f"""
                <div class="metric-box" style="border-left-color: {color};">
                    <h4 style="margin: 0; color: #fff;">{title}</h4>
                    <p style="margin: 0.2rem 0; color: #cbd5e1; font-size: 0.85rem;">{"Fare" if is_en else "單程票價"}: <b>${data.get('transit_fare_aud', 0.5):.2f} AUD</b></p>
                    <hr style="margin: 0.4rem 0; border-color: #334155;">
                    <p style="margin: 0;"> <b>{"Car" if is_en else "自駕車"}: {shares.get('Car', 0):.1f}%</b> ({m_counts.get('Car', 0)}{" commuters" if is_en else "人"})</p>
                    <p style="margin: 0;"> <b>{"Transit" if is_en else "大眾運輸"}: {shares.get('Transit', 0):.1f}%</b> ({m_counts.get('Transit_Walk', 0) + m_counts.get('Transit_Scooter', 0)}{" commuters" if is_en else "人"})</p>
                    <p style="margin: 0;"> <b>{"Bicycle" if is_en else "自行車"}: {shares.get('Bicycle', 0):.1f}%</b> ({m_counts.get('Bicycle', 0)}{" commuters" if is_en else "人"})</p>
                    <p style="margin: 0.4rem 0 0 0; color: #38bdf8; font-size: 0.85rem;"> {"Daily CO2 Saved" if is_en else "每日減碳"}: <b>{data.get('daily_co2_saved_kg', 0)/1000:.1f} {"t" if is_en else "噸"}</b></p>
                </div>
                """, unsafe_allow_html=True)
