"""
Tab 3: Calibration Rigor, Parameter Settings, and TMR Forecasting Methodology & Limitations
==========================================================================================
Mirrors Chapter 3 of reports/brisbane_transit_report_en.md:
- 3.1 Why Calibration is Essential (Inverse Loss & SciPy L-BFGS-B Optimization)
- 3.2 Configured Parameters & Why (Corridors, Archetypes, Synaptic Weights)
- 3.3 How Brisbane TMR Currently Forecasts Patronage (BSTM-MM Incremental Pivot Logit)
- 3.4 Mathematical Limitations of BSTM-MM and Contrast with the Drosophila Model
"""

import os
import streamlit as st
import pandas as pd
from src.core import get_calibration_provenance

def render_tab3_calibration_tmr(is_en: bool):
    st.markdown("## " + ("Chapter 3: Calibration Rigor & TMR Forecasting Limitations" if is_en else "第三章：參數校準嚴謹度、模型設定與傳統 TMR 預測方法之局限"))
    st.markdown(
        "Detailing the inverse calibration methodology, parameter definitions, and an in-depth mathematical critique of Queensland's traditional **BSTM-MM Incremental Pivot Logit** against the **Drosophila Connectome Model**."
        if is_en else
        "深入探討反向校準數學方法、生物神經權重設定，並深度對比昆士蘭官方現行 **BSTM-MM 增量樞紐羅吉特模型** 的數學極限與果蠅大腦連接體模型的突破。"
    )

    # -------------------------------------------------------------------------
    # 3.1 Why Calibration is Essential
    # -------------------------------------------------------------------------
    st.markdown("### 3.1 " + ("Why Calibration is Essential (MLE / MAP Bayesian Optimization)" if is_en else "為何參數校準至關重要：排除主觀臆測的數值反向擬合"))
    
    col_l1, col_l2, col_l3, col_l4 = st.columns(4)
    with col_l1:
        st.metric("Prior Objective Loss" if is_en else "校準前先驗損失 (Prior)", "114.86", "Initial Heuristics" if is_en else "文獻先驗值")
    with col_l2:
        st.metric("Calibrated Objective Loss" if is_en else "校準後目標損失 (Calibrated)", "31.60", "-72.5% Error Reduction" if is_en else "誤差縮減 72.5%", delta_color="normal")
    with col_l3:
        st.metric("RMSE Before Calibration" if is_en else "校準前均方根誤差 (RMSE)", "3.92%", "Literature Baseline" if is_en else "基準誤差")
    with col_l4:
        st.metric("RMSE After Calibration" if is_en else "校準後均方根誤差 (RMSE)", "1.99%", "-49.2% Precision Gain" if is_en else "精度提升一倍", delta_color="normal")

    st.markdown(r"""
    **1. 損失函數公式 (Objective Loss Function Formulation)**:
    $$\min_{\boldsymbol{\theta}} \mathcal{L}(\boldsymbol{\theta}) = \sum_{k=1}^{K} w_k \cdot \left[ Y_k^{\text{empirical}} - \hat{Y}_k(\boldsymbol{\theta}) \right]^2 + \lambda \sum_{j} \left( \frac{\theta_j - \theta_{j,0}}{\sigma_{j,0}} \right)^2$$
    * **$Y_k^{\text{empirical}}$**: 昆士蘭開放資料庫 2,477 萬筆真實刷卡紀錄觀察到的路線客流增幅標的。
    * **$\hat{Y}_k(\boldsymbol{\theta})$**: 10,000 名虛擬市民在突觸權重向量 $\boldsymbol{\theta}$ 下的蒙地卡羅分流預測。
    * **Prior Regularizer $\lambda$**: 貝氏先驗正則化項（Ridge penalty），防止數值優化過度擬合。
    * **優化演算法 (Optimizer)**: 採用限制性擬牛頓法 **SciPy `L-BFGS-B`** 進行多維度數值收斂。
    """ if not is_en else r"""
    **1. Optimization Loss Formulation**:
    $$\min_{\boldsymbol{\theta}} \mathcal{L}(\boldsymbol{\theta}) = \sum_{k=1}^{K} w_k \cdot \left[ Y_k^{\text{empirical}} - \hat{Y}_k(\boldsymbol{\theta}) \right]^2 + \lambda \sum_{j} \left( \frac{\theta_j - \theta_{j,0}}{\sigma_{j,0}} \right)^2$$
    * **$Y_k^{\text{empirical}}$**: Observed empirical ridership growth from 24.8M Go Card tap transactions.
    * **$\hat{Y}_k(\boldsymbol{\theta})$**: Monte Carlo mode-shift forecast simulated with synaptic weight vector $\boldsymbol{\theta}$.
    * **Prior Regularizer $\lambda$**: Bayesian MAP shrinkage term preventing sample noise overfitting.
    * **Optimizer**: Constrained **SciPy `L-BFGS-B`** quasi-Newton solver with physiological bounds.
    """)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 3.2 What Parameters Are Configured and Why
    # -------------------------------------------------------------------------
    st.markdown("### 3.2 " + ("What Parameters Are Configured and Why" if is_en else "模型設定了哪些參數？為何設定這些參數？"))
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("#### " + ("Category B: 5 Commuter Archetypes" if is_en else "類別 B：五大市民通勤族群設定"))
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

    with col_p2:
        st.markdown("#### " + ("Category C: Calibrated Synaptic Weights" if is_en else "類別 C：校準後神經突觸權重位移"))
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
        st.table(pd.DataFrame(param_table))

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 3.3 How Brisbane TMR Currently Forecasts Patronage
    # -------------------------------------------------------------------------
    st.markdown("### 3.3 " + ("How Brisbane TMR Currently Forecasts Patronage (BSTM-MM)" if is_en else "昆士蘭交通局（TMR）現行預測方法：BSTM-MM 增量樞紐羅吉特模型"))
    
    st.markdown(r"""
    昆士蘭交通與主幹道路部（TMR）使用 **布里斯本策略交通模型（BSTM-MM）** 中的 **增量樞紐羅吉特公式（Incremental Pivot Logit）** 預測票價政策影響：
    $$\Delta U = \beta_{\text{cost}} \cdot \Delta \text{Fare} + \beta_{\text{ivtt}} \cdot \Delta \text{IVTT} + \beta_{\text{wait}} \cdot \Delta \text{Wait}$$
    $$P_{\text{new}} = \frac{P_0 \cdot e^{\Delta U}}{(1 - P_0) + P_0 \cdot e^{\Delta U}}$$
    * **官方參數依據 (TMR Transport Modelling Guidelines)**：
      * 車內行程時間係數：$\beta_{\text{ivtt}} = -0.035 \text{ min}^{-1}$
      * 等候時間係數：$\beta_{\text{wait}} = -0.070 \text{ min}^{-1}$（等候時間權重為車內時間的 2.0 倍）
      * 票價成本係數：$\beta_{\text{cost}} = -0.1136 \text{ AUD}^{-1}$（基於東南昆士蘭旅行時間價值 VTTS = \$18.50 AUD/小時）
      * 尖峰容量阻尼係數：$\phi \approx 0.60$（專用道幹線）至 $\phi \approx 0.65$（郊區路網）。
    """ if not is_en else r"""
    The Queensland Department of Transport and Main Roads (TMR) forecasts travel demand using the **Brisbane Strategic Transport Model (BSTM-MM Incremental Pivot Logit)**:
    $$\Delta U = \beta_{\text{cost}} \cdot \Delta \text{Fare} + \beta_{\text{ivtt}} \cdot \Delta \text{IVTT} + \beta_{\text{wait}} \cdot \Delta \text{Wait}$$
    $$P_{\text{new}} = \frac{P_0 \cdot e^{\Delta U}}{(1 - P_0) + P_0 \cdot e^{\Delta U}}$$
    * **Official Parameter References (TMR Transport Modelling Guidelines)**:
      * In-vehicle travel time: $\beta_{\text{ivtt}} = -0.035 \text{ min}^{-1}$
      * Out-of-vehicle wait time: $\beta_{\text{wait}} = -0.070 \text{ min}^{-1}$ (valued at 2.0x in-vehicle time)
      * Fare cost: $\beta_{\text{cost}} = -0.1136 \text{ AUD}^{-1}$ (based on an SEQ Value of Travel Time Savings of \$18.50 AUD/hour)
      * Capacity dampening factors: $\phi \approx 0.60$ (busways) and $\phi \approx 0.65$ (suburban streets).
    """)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # 3.4 Six Core Mathematical Limitations of BSTM-MM vs Drosophila Model
    # -------------------------------------------------------------------------
    st.markdown("### 3.4 " + ("Six Core Mathematical Limitations of BSTM-MM and Contrast with Drosophila Model" if is_en else "昆士蘭傳統預測方法的六大數學缺陷與果蠅連接體模型之對比突破"))
    
    st.markdown(
        "Why does BSTM-MM fail under disruptive policies like 50-cent fares? As transport engineers, we identify six structural bottlenecks:"
        if is_en else
        "為何傳統 BSTM-MM 在面對 50-Cent 這種破壞性價格衝擊時會發生嚴重失真？身為交通工程師，我們歸納出以下六大核心數學缺陷："
    )

    col_flaw1, col_flaw2 = st.columns(2)
    with col_flaw1:
        st.markdown(r"""
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #ff5252; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
            <h5 style="color: #ff5252; margin: 0 0 4px 0;">1. IIA Property (Red-Bus / Blue-Bus Paradox)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.5;">
                MNL assumes error terms are independent. When fares drop, it draws market share proportionally from all other modes based on prior share, failing to reflect true vehicle substitution patterns.
            </p>
        </div>
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #ff5252; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
            <h5 style="color: #ff5252; margin: 0 0 4px 0;">2. Linear-in-Parameters Utility & Constant VTTS</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.5;">
                Linear utility assumes constant slope ($V = \beta \cdot Cost$). Under an 88% fare cut, it fails to model diminishing marginal dopamine returns and the zero-price threshold effect.
            </p>
        </div>
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #ff5252; border-radius: 8px; padding: 14px;">
            <h5 style="color: #ff5252; margin: 0 0 4px 0;">3. TAZ Centroid Aggregation (~400m Uniform)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.5;">
                Averaging commuters into zone centroids wipes out the 2,200m walking barrier under 30°C Queensland sun, causing BSTM-MM to overpredict suburban feeder shifts (+31.9% vs +3.75% real).
            </p>
        </div>
        """ if is_en else r"""
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #ff5252; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
            <h5 style="color: #ff5252; margin: 0 0 4px 0;">1. IIA 特性與紅藍公車悖論 (Red-Bus / Blue-Bus Paradox)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.5;">
                MNL 假設隨機誤差獨立。票價暴跌時，模型按原有比例從自駕車、步行、自行車中等比例抽走客源，完全脫離現實中跨運具的結構性替代規律。
            </p>
        </div>
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #ff5252; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
            <h5 style="color: #ff5252; margin: 0 0 4px 0;">2. 線性效用函數與恆定時間價值 (Linear Utility & Constant VTTS)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.5;">
                線性效用假設票價敏感度是一條死板的直線。面對票價暴跌 88%，傳統模型無法反映金錢多巴胺的邊際飽和曲線與零價心理效應。
            </p>
        </div>
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #ff5252; border-radius: 8px; padding: 14px;">
            <h5 style="color: #ff5252; margin: 0 0 4px 0;">3. TAZ 空間分區質心平均化 (~400m 固定接駁)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.5;">
                將整個小區簡化為一個點，直接抹平了外環郊區在昆士蘭 30°C 豔陽下走 2,200 公尺的體能阻抗，導致傳統模型嚴重高估郊區轉移率 (+31.9% vs 實測僅 +3.75%)。
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_flaw2:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #ff5252; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
            <h5 style="color: #ff5252; margin: 0 0 4px 0;">4. Static Assignment without Dynamic Crush-Load Rejection</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.5;">
                Treats transit lines as having smooth volume-delay penalties. In reality, morning peak buses hit 100% capacity and pass full; commuters experience refusal and switch back to driving.
            </p>
        </div>
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #ff5252; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
            <h5 style="color: #ff5252; margin: 0 0 4px 0;">5. The Compensatory Error (Peak vs. Leisure Conflation)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.5;">
                Applies a fixed peak-to-daily expansion factor. It overpredicts morning peak shift (+36.8% vs +25.7% real) while completely missing the +160% weekend night leisure boom.
            </p>
        </div>
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #ff5252; border-radius: 8px; padding: 14px;">
            <h5 style="color: #ff5252; margin: 0 0 4px 0;">6. Static Reversibility vs. Sunk Cost Hysteresis</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.5;">
                Assumes symmetric choices. Suburban households already paid $1,200/year for car registration and insurance; these sunk costs anchor them to driving despite temporary 50c fares.
            </p>
        </div>
        """ if is_en else """
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #ff5252; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
            <h5 style="color: #ff5252; margin: 0 0 4px 0;">4. 靜態配流忽視實體滿載拒載 (Crush-Load Capacity Veto)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.5;">
                將公車容量視為柔性延誤曲線。現實中專用道早尖峰公車塞爆過站不停，上班族經歷拒載後會直接啟動否決機制，回流開私家車。
            </p>
        </div>
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #ff5252; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
            <h5 style="color: #ff5252; margin: 0 0 4px 0;">5. 補償性預測偏誤 (Compensatory Error: 尖峰離峰混淆)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.5;">
                以固定係數（約 3.0）推算全日。早尖峰嚴重高估上班族棄車意願，但夜間卻完全漏算規避 Uber 動態加價引發的 +160% 週末深夜狂潮。
            </p>
        </div>
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-left: 4px solid #ff5252; border-radius: 8px; padding: 14px;">
            <h5 style="color: #ff5252; margin: 0 0 4px 0;">6. 靜態可逆性忽略汽車持有沉沒成本 (Sunk Cost Hysteresis)</h5>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.5;">
                假設行為對稱可逆。郊區家庭早已購車並預繳每年逾 $1,200 牌照稅與保險，沉沒成本牢牢錨定自駕習慣，不會因 50c 試辦就變賣車輛。
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### " + ("Side-by-Side Methodology Benchmarking Matrix" if is_en else "傳統 BSTM-MM 與果蠅連接體模型對決矩陣"))
    matrix_data = [
        {"評估維度 (Dimension)": "1. 票價敏感度數學架構", "昆士蘭傳統 BSTM-MM (4-Step)": "固定線性效用 (V = β·Cost)", "果蠅大腦連接體模型": "雙曲正切非線性飽和曲線 (tanh)", "實務預測衝擊": "傳統法高估極端降價效益；果蠅模型誤差僅 0.03 pp"},
        {"評估維度 (Dimension)": "2. 最後一哩路步行阻抗", "昆士蘭傳統 BSTM-MM (4-Step)": "TAZ 質心平均化 (~400m 固定)", "果蠅大腦連接體模型": "真實微觀步行距離 + 氣候疲勞指數 (d^1.51)", "實務預測衝擊": "傳統法預測外環客流大爆死；果蠅重現車主自駕抗拒"},
        {"評估維度 (Dimension)": "3. 運具容量與拒載機制", "昆士蘭傳統 BSTM-MM (4-Step)": "靜態平滑分配 (無排隊實體拒載)", "果蠅大腦連接體模型": "物理滿載約束 + 迴避否決迴路 (MBON11)", "實務預測衝擊": "傳統法過度分配上班族；果蠅模型封頂於實體容量"},
        {"評估維度 (Dimension)": "4. 全日動態與夜間休閒", "昆士蘭傳統 BSTM-MM (4-Step)": "單一早尖峰膨脹係數 (固定 3.0)", "果蠅大腦連接體模型": "晝夜時鐘神經元 (PDF) + Uber 錨點替代", "實務預測衝擊": "傳統法漏算夜間爆發；果蠅模型精準捕獲 +160% 潮"},
        {"評估維度 (Dimension)": "5. 人群異質性與門檻", "昆士蘭傳統 BSTM-MM (4-Step)": "固定代表性階層 (單一理性人)", "果蠅大腦連接體模型": "10,000 名多樣性虛擬市民 + 載具資產門檻閘控", "實務預測衝擊": "解釋為何學生為 50c 狂喜，而專業人士只在乎提速"},
        {"評估維度 (Dimension)": "6. 決策透明度與可解釋性", "昆士蘭傳統 BSTM-MM (4-Step)": "黑箱迴歸係數 (無法拆解原因)", "果蠅大腦連接體模型": "白箱生物神經放電 (PAM獎勵 vs PPL1痛感)", "實務預測衝擊": "明確指引政府該補貼票價、提速還是改善遮蔭"}
    ] if not is_en else [
        {"Dimension": "1. Price Sensitivity Formulation", "Queensland Traditional BSTM-MM": "Fixed linear utility (V = β·Cost)", "Drosophila Connectome Model": "Non-linear tanh S-curve with car anchor", "Practical Forecasting Impact": "BSTM-MM overpredicts extreme fare cuts; Drosophila hits within 0.03 pp"},
        {"Dimension": "2. Pedestrian Access Impedance", "Queensland Traditional BSTM-MM": "TAZ centroid average (~400m uniform)", "Drosophila Connectome Model": "Continuous walk distance with exponent d^1.51", "Practical Forecasting Impact": "BSTM-MM predicted +31.9% on Route 1; Drosophila reproduced car resistance (+3.75%)"},
        {"Dimension": "3. Capacity and Crowding", "Queensland Traditional BSTM-MM": "Smooth volume-delay (no physical rejection)", "Drosophila Connectome Model": "Hard seat limits & avoidance veto (MBON11)", "Practical Forecasting Impact": "BSTM-MM over-allocates peak drivers; Drosophila bounds growth to physical seats"},
        {"Dimension": "4. Time-of-Day Dynamics", "Queensland Traditional BSTM-MM": "Uniform daily expansion factor (fixed 3.0)", "Drosophila Connectome Model": "Circadian clock state (PDF) + Uber anchor", "Practical Forecasting Impact": "BSTM-MM missed +160% night boom; Drosophila captured both peak and leisure"},
        {"Dimension": "5. Demographic Diversity", "Queensland Traditional BSTM-MM": "Fixed representative groups", "Drosophila Connectome Model": "10,000 heterogeneous agents + asset gating", "Practical Forecasting Impact": "Explains why students switch for fares while professionals need speed"},
        {"Dimension": "6. Model Explainability", "Queensland Traditional BSTM-MM": "Opaque regression parameters", "Drosophila Connectome Model": "Traceable neural circuits (PAM reward vs PPL1 pain)", "Practical Forecasting Impact": "Tells planners whether a project fails from delay, walking, or fares"}
    ]
    st.table(pd.DataFrame(matrix_data))
