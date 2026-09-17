"""
Tab 2: Live Commuter Telemetry Arena (Doomfly Style) and Multi-Modal Archetypes.
"""
import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px

def render_tab2_archetypes(is_en: bool):
    st.markdown("### " + ("🎮 Live Commuter Telemetry Arena (Doomfly Style)" if is_en else "🎮 實時動態果蠅通勤模擬舞台 (Doomfly 遙測風格)"))
    st.info(
        "💡 **Interactive Canvas**: Real-time 60 FPS HTML5 canvas simulating fruit fly commuters across Brisbane. Use buttons beneath canvas to toggle between **Walk, Cycle, 50c Bus, Drive, Stay Home**, or click **'Brain Auto'** to let the Janelia connectome decide! Supports **☀️ Sunny** vs **🌧️ Severe Storm/Heatwave** weather states."
        if is_en else
        "💡 **舞台互動指南**：本動態畫布靈感源自 **Doomfly**。上方即時顯示雙示波器神經電位（PAM 獎勵、PPL1 痛感、時速、淨點數），下方模擬果蠅跨步、踩單車、搭乘冷氣公車與開車。可於下方切換 **晴朗 vs 雨天/高溫**，或點擊 **「自動決策」** 讓 Janelia FlyEM 連接體即時選定運具！"
    )

    _ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    arena_path = os.path.join(_ROOT, "assets", "doomfly_arena.html")
    if not os.path.exists(arena_path):
        arena_path = os.path.join("assets", "doomfly_arena.html")
    if os.path.exists(arena_path):
        with open(arena_path, "r", encoding="utf-8") as f:
            arena_template = f.read()
        # Inject dynamic language: pure 'en' or pure 'zh'
        arena_html = arena_template.replace("___ARENA_LANG___", "en" if is_en else "zh")
        components.html(arena_html, height=800, scrolling=False)
    else:
        st.warning("⚠️ `assets/doomfly_arena.html` not found.")

    st.markdown("---")
    st.markdown("### " + ("🪰 Multi-Modal Commuter Archetypes & Neural Point Economy" if is_en else "🪰 八大多運具通勤角色圖鑑與真實點數天平"))

    subtab_a_title = "🏫 " + ("Scenario A: 5.2 km Suburban Life (Springwood ➔ Rochedale South)" if is_en else "情境 A: 5.2 km 郊區生活圈 (Springwood ➔ Rochedale South 州立小學)")
    subtab_b_title = "🎓 " + ("Scenario B: 28.8 km University Express (Springwood ➔ UQ St Lucia)" if is_en else "情境 B: 28.8 km 大學通勤走廊 (Springwood ➔ 昆士蘭大學 UQ St Lucia)")

    subtab_a, subtab_b = st.tabs([subtab_a_title, subtab_b_title])

    # =========================================================
    # SCENARIO A: 5.2 KM SUBURBAN LIFE
    # =========================================================
    with subtab_a:
        st.markdown("#### 🏫 " + ("Scenario A Archetypes (5.2 km Local Hills)" if is_en else "情境 A 專屬運具角色圖鑑（5.2 km 郊區生活圈）"))

        # 4 cols x 2 rows
        r1_c1, r1_c2, r1_c3, r1_c4 = st.columns(4)
        with r1_c1:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #00ff88;">🛴+🚌 ' + ("Combo Multimodal" if is_en else "複合接駁模式") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 30 min (10m scooter + 20m bus)
                * **Net Score**: **24.0 pts**
                * **Cost**: $0.50 Bus + $5.50 Scooter = **$6.00**
                * **First-Mile**: Avoids 26-min walk in heat
                * **Traffic**: Bypasses local school rush
                * **Connectome**: High comfort, moderate fare penalty
                """)
            else:
                st.markdown("""
                * **耗時**: 30 分鐘 (10分滑板車 + 20分公車)
                * **最終得分**: **24.0 點**
                * **花費**: $0.50 票價 + $5.50 滑板車 = **$6.00**
                * **首哩路**: 避開 26 分鐘步行與上坡體力負擔
                * **路況**: 專用路線免受接送塞車之苦
                * **神經判定**: 高舒適度，滑板車租金適度折減
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        with r1_c2:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #38bdf8;">🚌 ' + ("50¢ Busway Commuter" if is_en else "50¢ 公車專用道族") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 46 min (26m walk + 20m bus)
                * **Net Score**: **14.5 pts**
                * **Cost**: **$0.50** AUD flat fare
                * **First-Mile Walk**: -15.0 pts (2.2km walk)
                * **Weather Protection**: 100% covered in bus
                * **Connectome**: PPL1 rises from walking fatigue
                """)
            else:
                st.markdown("""
                * **耗時**: 46 分鐘 (26分步行 + 20分公車)
                * **最終得分**: **14.5 點**
                * **花費**: **$0.50** 單程超低票價
                * **首哩路**: -15.0 點 (步行 2.2km 到站)
                * **車廂遮蔽**: 車內空調完全防曬避雨
                * **神經判定**: 票價誘因顯著，但受限於第一哩步行阻抗
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        with r1_c3:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #f59e0b;">🚲 ' + ("Bicycle Rider" if is_en else "自行車騎士") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 20 min (5.2km ride)
                * **Net Score**: **24.0 pts**
                * **Cost**: -$2.00 (Gear wear & maintenance)
                * **Effort**: Moderate hill climb (-4.0 pts)
                * **Flexibility**: Door-to-door, zero waiting
                * **Connectome**: High Octopamine motor reward
                """)
            else:
                st.markdown("""
                * **耗時**: 20 分鐘 (5.2km 直騎)
                * **最終得分**: **24.0 點**
                * **花費**: -$2.00 (車輛保養磨損)
                * **體力負擔**: 郊區丘陵爬坡 (-4.0 點)
                * **機動性**: 門到門零等待時間
                * **神經判定**: Octopamine 辛弗林維持正向運動放電
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        with r1_c4:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #e2e8f0;">🛴 ' + ("e-Scooter Direct" if is_en else "微移動滑板客") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 15 min (Direct ride)
                * **Net Score**: **26.0 pts**
                * **Cost**: **$4.00** (15-min rental)
                * **Fatigue**: 0 pts (Effortless breeze)
                * **Suitability**: High efficiency for 5.2km trip
                * **Connectome**: MBON01 **54.2 Hz** (High utility)
                """)
            else:
                st.markdown("""
                * **耗時**: 15 分鐘 (門到門直達)
                * **最終得分**: **26.0 點**
                * **花費**: **$4.00** (15分鐘租金)
                * **體力負擔**: 0 點 (省力便捷)
                * **短途效益**: 5.2km 短程高效接駁選擇
                * **神經判定**: MBON01 **54.2 Hz** (短途淨得分最高)
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4)
        with r2_c1:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #60a5fa;">🚗 ' + ("Private Car" if is_en else "自駕私家車") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 8-12 min
                * **Net Score**: **18.0 pts**
                * **Holding Cost**: -$10.0 (Daily capital/insurance)
                * **Fuel**: -$2.00 (Short distance)
                * **Parking**: Free parking at school zone
                * **Connectome**: Fast trip penalized by holding cost
                """)
            else:
                st.markdown("""
                * **耗時**: 8-12 分鐘
                * **最終得分**: **18.0 點**
                * **持車成本**: -$10.0 (折舊、牌照與保險分攤)
                * **燃油**: -$2.00 (短途油耗低)
                * **停車費**: 學校區域免費停車
                * **神經判定**: 速度快但受持車固定成本折減
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        with r2_c2:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #2dd4bf;">🚙 ' + ("e-Car / Uber" if is_en else "e-租車 / Uber") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 8-12 min
                * **Net Score**: **23.0 pts**
                * **Cost**: **$7.00** (Short-trip on-demand fare)
                * **Zero Ownership**: No insurance, no rego
                * **Role**: Flexible trip option
                * **Connectome**: PPL1 low due to small fare
                """)
            else:
                st.markdown("""
                * **耗時**: 8-12 分鐘
                * **最終得分**: **23.0 點**
                * **花費**: **$7.00** (短途即時車資)
                * **零持有負擔**: 免牌照稅、免保養保險
                * **定位效益**: 短程靈活應急運具
                * **神經判定**: 費用適中，無長期折舊負擔
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        with r2_c3:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #f87171;">🚶 ' + ("Suburban Walker" if is_en else "長程步行者") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 65 min
                * **Net Score**: **-5.0 pts** (Fatigue penalty)
                * **Cost**: $0.00
                * **Fatigue**: -35.0 pts (5.2km uphill walking)
                * **Summer Heat**: TRP channels depolarize
                * **Connectome**: MBON01 suppressed by fatigue
                """)
            else:
                st.markdown("""
                * **耗時**: 65 分鐘
                * **最終得分**: **-5.0 點** (高體能負擔)
                * **花費**: $0.00
                * **步行體能負擔**: -35.0 點 (5.2km 丘陵步行)
                * **氣候效應**: TRP 熱敏離子通道活化
                * **神經判定**: PPL1 負向活化過高，模型抑制此選項
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        with r2_c4:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #ec4899;">🛏️ ' + ("Stay Home" if is_en else "取消行程留在家中") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 0 min
                * **Net Score**: **0.0 pts**
                * **Restoration**: +100% Energy & sleep recovery
                * **Zero Risk**: 0 fatigue, 0 parking, 0 fare
                * **Role**: Default alternative when travel costs exceed benefits
                * **Connectome**: PAM baseline resting state
                """)
            else:
                st.markdown("""
                * **耗時**: 0 分鐘 (取消行程)
                * **最終得分**: **0.0 點**
                * **修復效益**: +100% 精力與睡眠回補
                * **零風險**: 0 疲勞、0 停車、0 車資
                * **定位效益**: 當所有運具淨效用均為負時的替代選擇
                * **神經判定**: PAM 基準靜止放電
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        # Scenario A Dynamic Animation & Point Economy
        col_ctrl1_a, col_ctrl2_a = st.columns([3, 2])
        with col_ctrl1_a:
            st.markdown("#### 🎬 " + ("Wake-Up Time Dynamic Point Economy Animation (07:30 ➔ 09:20 AM)" if is_en else "起床與出發時間推移動畫演繹（07:30 ➔ 09:20 AM 點數消長）"))
            st.caption("點擊下方動畫圖表中的「▶ Play」或拖曳時間軸，觀察隨出發時間延後，各運具淨得分的即時變化與分流演變。" if not is_en else "Click '▶ Play' or drag the animation slider to watch how each mode's points decay or hold as departure time slips later.")
        with col_ctrl2_a:
            sim_weather_a = st.radio(
                "🌦️ Weather Condition (Scenario A):" if is_en else "🌦️ 天候環境條件（情境 A）：",
                ["☀️ Pleasant (22°C)" if is_en else "☀️ 晴朗舒適涼秋 (22°C)", "🌧️ Storm / Heat (35°C)" if is_en else "🌧️ 大雨與高溫氣候 (35°C)"],
                horizontal=True,
                key="radio_weather_a"
            )
            is_rain_a = ("Storm" in sim_weather_a or "大雨" in sim_weather_a)

        # Build Animation Frames DataFrame
        modes_spec_a = [
            {"name": "Combo (🛴+🚌)" if is_en else "複合接駁 (🛴+🚌)", "time": 30, "fee": 6.0, "fatigue": 0.0, "parking": 0.0, "weather": 2.0 if is_rain_a else 0.0, "color": "#00ff88"},
            {"name": "e-Scooter" if is_en else "e-滑板車直騎", "time": 15, "fee": 4.0, "fatigue": 0.0, "parking": 0.0, "weather": 7.0 if is_rain_a else 0.0, "color": "#e2e8f0"},
            {"name": "Bicycle" if is_en else "自行車", "time": 20, "fee": 2.0, "fatigue": 4.0, "parking": 0.0, "weather": 8.0 if is_rain_a else 0.0, "color": "#f59e0b"},
            {"name": "e-Car / Uber" if is_en else "e-租車 / Uber", "time": 12 if is_rain_a else 8, "fee": 7.0, "fatigue": 0.0, "parking": 0.0, "weather": 0.0, "color": "#2dd4bf"},
            {"name": "Private Car" if is_en else "自駕私家車", "time": 12 if is_rain_a else 8, "fee": 2.0, "fatigue": 0.0, "parking": 10.0, "weather": 0.0, "color": "#60a5fa"},
            {"name": "Transit (50c)" if is_en else "50c 公車", "time": 46, "fee": 0.5, "fatigue": 15.0, "parking": 0.0, "weather": 10.0 if is_rain_a else 0.0, "color": "#38bdf8"},
            {"name": "Walking" if is_en else "步行", "time": 65, "fee": 0.0, "fatigue": 35.0, "parking": 0.0, "weather": 25.0 if is_rain_a else 0.0, "color": "#f87171"},
            {"name": "Stay Home" if is_en else "留在家", "time": 0, "fee": 0.0, "fatigue": 0.0, "parking": 0.0, "weather": 0.0, "color": "#ec4899"}
        ]

        anim_records_a = []
        for t in range(450, 565, 5):
            dep_str = f"{t//60:02d}:{t%60:02d} AM"
            for m in modes_spec_a:
                if "Stay Home" in m["name"] or "留在家" in m["name"]:
                    net = 0.0
                    arr_str = "Home" if is_en else "留在家"
                else:
                    arr = t + m["time"]
                    arr_str = f"{arr//60:02d}:{arr%60:02d} AM"
                    late = max(0, arr - 540)
                    base = max(0.0, 30.0 - float(late))
                    net = max(-25.0, base - m["fee"] - m["fatigue"] - m["parking"] - m["weather"])
                anim_records_a.append({
                    "出發時間" if not is_en else "Departure Time": dep_str,
                    "運具選擇" if not is_en else "Transport Mode": m["name"],
                    "最終淨得分" if not is_en else "Net Score": round(net, 1),
                    "預計抵達" if not is_en else "Arrival": arr_str
                })

        df_anim_a = pd.DataFrame(anim_records_a)
        time_col = "出發時間" if not is_en else "Departure Time"
        mode_col = "運具選擇" if not is_en else "Transport Mode"
        net_col = "最終淨得分" if not is_en else "Net Score"

        col_anim_left, col_anim_right = st.columns([3, 2])
        with col_anim_left:
            fig_anim_a = px.bar(
                df_anim_a,
                x=mode_col,
                y=net_col,
                color=mode_col,
                animation_frame=time_col,
                range_y=[-25, 32],
                title="🎬 出發時間推移動畫演繹 (點擊 Play 觀察積分變動)" if not is_en else "🎬 Commute Point Race over Wake-up Time (Click Play)",
                color_discrete_map={m["name"]: m["color"] for m in modes_spec_a}
            )
            fig_anim_a.update_layout(
                paper_bgcolor="#0e1117",
                plot_bgcolor="#161b22",
                font=dict(color="#e0e0e0"),
                showlegend=False,
                height=360,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            if fig_anim_a.layout.updatemenus:
                fig_anim_a.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 400
                fig_anim_a.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 250
            st.plotly_chart(fig_anim_a, use_container_width=True)

        with col_anim_right:
            # Multi-line decay curve
            fig_line_a = px.line(
                df_anim_a,
                x=time_col,
                y=net_col,
                color=mode_col,
                title="📈 各運具遲到衰退軌跡 (開車/Uber 之防守緩衝區間)" if not is_en else "📈 Lateness Decay Curves (Car/Uber Buffer Plateau)",
                color_discrete_map={m["name"]: m["color"] for m in modes_spec_a}
            )
            fig_line_a.update_layout(
                paper_bgcolor="#0e1117",
                plot_bgcolor="#161b22",
                font=dict(color="#e0e0e0"),
                height=360,
                margin=dict(l=10, r=10, t=40, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5, font=dict(size=10))
            )
            st.plotly_chart(fig_line_a, use_container_width=True)

        # -----------------------------------------------------
        # SCENARIO A CONCLUSION CARD
        # -----------------------------------------------------
        st.markdown('<div style="background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); border: 1px solid #4338ca; border-left: 5px solid #38bdf8; border-radius: 10px; padding: 18px; margin-top: 15px;">', unsafe_allow_html=True)
        st.markdown("### 💡 " + ("Scenario A Engineering Conclusion: The 'Late-Riser Car Dependency Lock-in'" if is_en else "情境 A 核心工程結論：晚起誘發的自駕鎖定效應（The Late-Riser Car Lock-in）"))
        if is_en:
            st.markdown("""
            * **1. Early-Bird Green Mobility Dominance (07:30 - 08:15 AM)**:
              * When departing before 08:15 AM, **e-Scooter (26.0 pts)**, **Bicycle (24.0 pts)**, and **Combo (24.0 pts)** outperform private driving (18.0 pts).
              * Low operating costs and zero parking anxiety give active/micromobility positive dopamine (PAM) rewards.
            * **2. The Asymmetric 'Defensive Plateau' of the Car (08:15 - 08:52 AM)**:
              * The moment departure slips past 08:15 AM, public transit and walking trigger lateness penalties. **50¢ Bus (46 min) drops from 14.5 pts down to 0 pts**, and Combo incurs lateness penalties after 08:30 AM.
              * **Key Finding**: Because **Private Car and e-Car/Uber take only 8 minutes**, they maintain their peak scores (**18.0 pts and 23.0 pts**) for an extra **37 minutes** (until 08:52 AM).
              * During this time window, Uber and Private Car maintain the highest net utility.
            * **3. Transport Policy Insight**:
              * Suburban car dependency is strongly influenced by the **circadian morning sleep buffer (PDF clock neurons)**.
              * A 10-minute departure delay causes a 46-minute bus trip to miss the arrival target, prompting a shift toward private driving or on-demand rides. Subsidizing fares alone does not resolve the competitiveness gap caused by long door-to-door transit times.
            """)
        else:
            st.markdown("""
            * **1. 晨間提早出發時主動式交通之效用優勢（07:30 ～ 08:15 AM）**：
              * 在 08:15 AM 前出發時，**e-滑板車直騎（26.0 點）**、**自行車（24.0 點）** 與 **複合接駁（24.0 點）** 淨效用高於私家車（18.0 點）。
              * 這顯示在時間充裕的條件下，免停車焦慮與運動健康效益能有效促使通勤者採用綠色出行。
            * **2. 私家車與 Uber 的「時間緩衝區間」（08:15 ～ 08:52 AM）**：
              * 一旦出發時間推遲至 08:15 之後，大眾運輸與步行因總時長較長，開始產生每分鐘的遲到扣分。**50¢ 公車（46分鐘車程）淨得分自 14.5 點降至 0 點**，複合接駁（30分鐘）亦於 08:30 後轉為負分。
              * **關鍵工程發現**：因為 **開車與 Uber 僅需 8 分鐘**，它們享有多達 **37 分鐘的時間緩衝區間**（積分維持在 **18.0 點與 23.0 點**）。
              * 在此窗口期內，大眾運輸淨得分因遲到罰分而顯著降低，而耗時僅 8 分鐘的自駕與共享汽車則保持最高效用。
            * **3. 交通政策深度啟示**：
              * 郊區居民依賴汽車，核心驅動力除了票價之外，亦包含 **PDF 晝夜時鐘神經元所反映的晨間作息時間約束**。
              * 只要出發時間延後 10 分鐘，46 分鐘的公車即可能面臨遲到罰分，促使通勤者轉向自駕或 Uber。單純補貼票價，難以改善因第一哩路步行耗時過長所導致的郊區大眾運輸競爭力差距。
            """)
        st.markdown('</div>', unsafe_allow_html=True)
    # =========================================================
    # SCENARIO B: 28.8 KM UNIVERSITY CORRIDOR (UQ)
    # =========================================================
    with subtab_b:
        st.markdown("#### 🎓 " + ("Scenario B Archetypes (28.8 km UQ St Lucia Express)" if is_en else "情境 B 專屬運具角色圖鑑（28.8 km 昆士蘭大學長途走廊）"))

        # 4 cols x 2 rows
        r1_c1_b, r1_c2_b, r1_c3_b, r1_c4_b = st.columns(4)
        with r1_c1_b:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #00ff88;">🛴+🚌 ' + ("Combo Multimodal" if is_en else "複合接駁模式") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 52 min (10m scooter + 42m bus)
                * **Net Score**: **24.0 pts**
                * **Cost**: $0.50 Bus + $5.50 Scooter = **$6.00**
                * **Busway Direct**: Crosses Eleanor Schonell Bridge
                * **Traffic Advantage**: Avoids M1 motorway peak delays
                * **Connectome**: High approach response for UQ
                """)
            else:
                st.markdown("""
                * **耗時**: 52 分鐘 (10分滑板車 + 42分公車)
                * **最終得分**: **24.0 點**
                * **花費**: $0.50 票價 + $5.50 滑板車 = **$6.00**
                * **專用橋梁**: 直通 Eleanor Schonell 綠橋
                * **專用道優勢**: 避開 M1 高速早晨壅塞
                * **神經判定**: 跨區長途高淨效用選項
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        with r1_c2_b:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #38bdf8;">🚌 ' + ("50¢ Busway Commuter" if is_en else "50¢ 公車專用道族") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 68 min (26m walk + 42m bus)
                * **Net Score**: **11.5 pts**
                * **Cost**: **$0.50** AUD flat fare
                * **Walking Burden**: -15.0 pts (2.2km morning walk)
                * **Cost-Effective**: Highly beneficial for budget-conscious students
                * **Connectome**: High NPF (budget constraint) offsets fatigue
                """)
            else:
                st.markdown("""
                * **耗時**: 68 分鐘 (26分步行 + 42分公車)
                * **最終得分**: **11.5 點**
                * **花費**: **$0.50** 超低單程票價
                * **第一哩路**: -15.0 點 (步行 2.2km 到站牌)
                * **經濟性**: 大專學生（高 NPF 預算約束）優選
                * **神經判定**: 票價獎勵抵銷部分步行阻抗
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        with r1_c3_b:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #f59e0b;">🚲 ' + ("V1 Veloway Cyclist" if is_en else "V1 專用道自行車騎士") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 85 min (28.8km ride)
                * **Net Score**: **13.0 pts**
                * **Cost**: -$2.00 (Tire & chain wear)
                * **Physical Exertion**: -15.0 pts (58km round trip)
                * **End of Trip**: Requires shower facilities
                * **Connectome**: Requires Octopamine > 0.85
                """)
            else:
                st.markdown("""
                * **耗時**: 85 分鐘 (28.8km 專用道)
                * **最終得分**: **13.0 點**
                * **花費**: -$2.00 (輪胎與鏈條消耗)
                * **體能消耗**: -15.0 點 (來回 58km 體力需求高)
                * **旅程終點設施**: 需使用到站梳洗淋浴設施
                * **神經判定**: 需較高體力耐受度 (Octopamine > 0.85)
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        with r1_c4_b:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #e2e8f0;">🛴 ' + ("e-Scooter Direct" if is_en else "e-滑板車長途") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 90 min
                * **Net Score**: **-5.0 pts**
                * **Rental Cost**: **$25.00** (High duration-based rental)
                * **Battery Limit**: Exceeds practical range of shared fleets
                * **Feasibility**: Low practicality for 28.8km
                * **Connectome**: High PPL1 cost and delay penalties
                """)
            else:
                st.markdown("""
                * **耗時**: 90 分鐘
                * **最終得分**: **-5.0 點**
                * **租金成本**: **$25.00** (時租費用偏高)
                * **電量上限**: 超出多數共享滑板車實用續航
                * **可行性**: 跨區長途實用性較低
                * **神經判定**: 高額費用與行車時間引發較高 PPL1 負向活化
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        r2_c1_b, r2_c2_b, r2_c3_b, r2_c4_b = st.columns(4)
        with r2_c1_b:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #60a5fa;">🚗 ' + ("Private Car" if is_en else "自駕私家車") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 42-50 min (M1 traffic peak)
                * **Net Score**: **12.5 pts**
                * **Daily Cost**: $8.60 Fuel + $14.50 UQ Parking = **$23.10**
                * **Green Bridge Barred**: Must detour via city arterials
                * **Parking**: Requires campus parking search
                * **Connectome**: PPL1 cost penalty suppresses choice
                """)
            else:
                st.markdown("""
                * **耗時**: 42-50 分鐘 (M1 尖峰壅塞)
                * **最終得分**: **12.5 點**
                * **每日開銷**: 油耗 $8.60 + UQ 停車 $14.50 = **$23.10**
                * **綠橋禁行**: 私家車需繞行市區幹道
                * **停車搜尋**: 尖峰校內尋找車位耗時
                * **神經判定**: 高額停車與油費帶來顯著 PPL1 成本折減
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        with r2_c2_b:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #2dd4bf;">🚙 ' + ("e-Car / Uber" if is_en else "e-租車 / Uber") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 42-50 min
                * **Net Score**: **0.0 pts** (High fare penalty)
                * **Cost**: **$55.00+** single trip
                * **Barrier**: High expense for regular commutes
                * **Role**: Occasional urgent travel only
                * **Connectome**: PPL1 **65.0 Hz** (High cost penalty)
                """)
            else:
                st.markdown("""
                * **耗時**: 42-50 分鐘
                * **最終得分**: **0.0 點** (高額車資扣分)
                * **單趟車資**: **$55.00+**
                * **族群門檻**: 日常通勤成本過高
                * **定位效益**: 僅適合偶發緊急出行需求
                * **神經判定**: PPL1 負向活化達 65.0 Hz (高額乘車開銷)
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        with r2_c3_b:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #f87171;">🚶 ' + ("Suburban Walker" if is_en else "長程步行者") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 340 min (5.6 hrs)
                * **Net Score**: **0.0 pts** (Arrival delay)
                * **Arrival**: Arrives at 1:40 PM (Exceeds morning window)
                * **Distance**: Unrealistic walking distance
                * **Feasibility**: Beyond human walking threshold
                * **Connectome**: MBON01 **5.0 Hz** (Suppressed)
                """)
            else:
                st.markdown("""
                * **耗時**: 340 分鐘 (5.6 小時)
                * **最終得分**: **0.0 點** (遲到扣分歸零)
                * **抵達時刻**: 下午 1:40 (超出早晨時段)
                * **體能限制**: 步行距離超出合理範圍
                * **可行性**: 超出日常通勤可行臨界
                * **神經判定**: MBON01 **5.0 Hz** (極度抑制)
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        with r2_c4_b:
            st.markdown('<div class="character-card">', unsafe_allow_html=True)
            st.markdown('<div class="character-title" style="color: #ec4899;">🛏️ ' + ("Stay Home" if is_en else "取消行程留在家中") + '</div>', unsafe_allow_html=True)
            if is_en:
                st.markdown("""
                * **Duration**: 0 min
                * **Net Score**: **0.0 pts** (Remote study / rest)
                * **Restoration**: +100% sleep restoration
                * **Late Threshold**: Preferred option when waking past 08:30 AM
                * **Role**: Commute cancellation when delay penalty exceeds utility
                * **Connectome**: Avoids all travel stress
                """)
            else:
                st.markdown("""
                * **耗時**: 0 分鐘 (線上學習 / 休息)
                * **最終得分**: **0.0 點**
                * **睡眠恢復**: +100% 體力精力儲備
                * **遲到門檻**: 超過 08:30 起床時之最高效用選項
                * **角色**: 當通勤延誤折減超過出行效用時的取消選擇
                * **神經判定**: 完全規避所有通勤阻抗
                """)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        # Scenario B Dynamic Animation & Point Economy
        col_ctrl1_b, col_ctrl2_b = st.columns([3, 2])
        with col_ctrl1_b:
            st.markdown("#### 🎬 " + ("Wake-Up Time Dynamic Point Economy Animation (07:15 ➔ 08:45 AM)" if is_en else "長途通勤時間推移動畫演繹（07:15 ➔ 08:45 AM 點數消長）"))
            st.caption("點擊下方動畫圖表中的「▶ Play」或拖曳時間軸，觀察 28.8km 長途走廊隨出發時間延後，綠橋大眾運輸優勢與 08:18 全體行程取消臨界線。" if not is_en else "Click '▶ Play' or drag the slider to watch how 28.8km UQ corridor points evolve and reach the 08:18 AM cancellation cutoff.")
        with col_ctrl2_b:
            sim_weather_b = st.radio(
                "🌦️ Weather Condition (Scenario B):" if is_en else "🌦️ 天候環境條件（情境 B）：",
                ["☀️ Pleasant (22°C)" if is_en else "☀️ 晴朗舒適涼秋 (22°C)", "🌧️ Storm / Heat (35°C)" if is_en else "🌧️ 大雨與高溫氣候 (35°C)"],
                horizontal=True,
                key="radio_weather_b"
            )
            is_rain_b = ("Storm" in sim_weather_b or "大雨" in sim_weather_b)

        # Build Animation Frames DataFrame for Scenario B
        modes_spec_b = [
            {"name": "Combo (🛴+🚌)" if is_en else "複合接駁 (🛴+🚌)", "time": 52, "fee": 6.0, "fatigue": 0.0, "parking": 0.0, "weather": 1.0 if is_rain_b else 0.0, "color": "#00ff88"},
            {"name": "Transit (50c)" if is_en else "50c 公車", "time": 68, "fee": 0.5, "fatigue": 15.0, "parking": 0.0, "weather": 10.0 if is_rain_b else 0.0, "color": "#38bdf8"},
            {"name": "Private Car" if is_en else "自駕私家車", "time": 50 if is_rain_b else 42, "fee": 8.6, "fatigue": 0.0, "parking": 14.5, "weather": 4.0 if is_rain_b else 0.0, "color": "#60a5fa"},
            {"name": "Bicycle (V1)" if is_en else "自行車 (V1專用道)", "time": 85, "fee": 2.0, "fatigue": 15.0, "parking": 0.0, "weather": 15.0 if is_rain_b else 0.0, "color": "#f59e0b"},
            {"name": "e-Scooter" if is_en else "e-滑板車直騎", "time": 90, "fee": 25.0, "fatigue": 10.0, "parking": 0.0, "weather": 15.0 if is_rain_b else 0.0, "color": "#e2e8f0"},
            {"name": "e-Car / Uber" if is_en else "e-租車 / Uber", "time": 50 if is_rain_b else 42, "fee": 55.0, "fatigue": 0.0, "parking": 0.0, "weather": 0.0, "color": "#2dd4bf"},
            {"name": "Walking" if is_en else "步行", "time": 340, "fee": 0.0, "fatigue": 100.0, "parking": 0.0, "weather": 50.0 if is_rain_b else 0.0, "color": "#f87171"},
            {"name": "Stay Home" if is_en else "留在家", "time": 0, "fee": 0.0, "fatigue": 0.0, "parking": 0.0, "weather": 0.0, "color": "#ec4899"}
        ]

        anim_records_b = []
        for t in range(435, 545, 5):
            dep_str = f"{t//60:02d}:{t%60:02d} AM"
            for m in modes_spec_b:
                if "Stay Home" in m["name"] or "留在家" in m["name"]:
                    net = 0.0
                    arr_str = "Home" if is_en else "留在家"
                else:
                    arr = t + m["time"]
                    arr_str = f"{arr//60:02d}:{arr%60:02d} AM"
                    late = max(0, arr - 540)
                    base = max(0.0, 30.0 - float(late))
                    net = max(-25.0, base - m["fee"] - m["fatigue"] - m["parking"] - m["weather"])
                anim_records_b.append({
                    "出發時間" if not is_en else "Departure Time": dep_str,
                    "運具選擇" if not is_en else "Transport Mode": m["name"],
                    "最終淨得分" if not is_en else "Net Score": round(net, 1),
                    "預計抵達" if not is_en else "Arrival": arr_str
                })

        df_anim_b = pd.DataFrame(anim_records_b)
        time_col_b = "出發時間" if not is_en else "Departure Time"
        mode_col_b = "運具選擇" if not is_en else "Transport Mode"
        net_col_b = "最終淨得分" if not is_en else "Net Score"

        col_anim_left_b, col_anim_right_b = st.columns([3, 2])
        with col_anim_left_b:
            fig_anim_b = px.bar(
                df_anim_b,
                x=mode_col_b,
                y=net_col_b,
                color=mode_col_b,
                animation_frame=time_col_b,
                range_y=[-25, 32],
                title="🎬 28.8km UQ 走廊時間推移動畫 (點擊 Play 觀察積分變動)" if not is_en else "🎬 28.8km UQ Corridor Point Race (Click Play)",
                color_discrete_map={m["name"]: m["color"] for m in modes_spec_b}
            )
            fig_anim_b.update_layout(
                paper_bgcolor="#0e1117",
                plot_bgcolor="#161b22",
                font=dict(color="#e0e0e0"),
                showlegend=False,
                height=360,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            if fig_anim_b.layout.updatemenus:
                fig_anim_b.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 400
                fig_anim_b.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 250
            st.plotly_chart(fig_anim_b, use_container_width=True)

        with col_anim_right_b:
            fig_line_b = px.line(
                df_anim_b,
                x=time_col_b,
                y=net_col_b,
                color=mode_col_b,
                title="📈 28.8km 各運具遲到衰退軌跡 (08:18 行程取消臨界線)" if not is_en else "📈 28.8km Lateness Decay Curves (08:18 Cancellation Cutoff)",
                color_discrete_map={m["name"]: m["color"] for m in modes_spec_b}
            )
            fig_line_b.update_layout(
                paper_bgcolor="#0e1117",
                plot_bgcolor="#161b22",
                font=dict(color="#e0e0e0"),
                height=360,
                margin=dict(l=10, r=10, t=40, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5, font=dict(size=10))
            )
            st.plotly_chart(fig_line_b, use_container_width=True)

        # -----------------------------------------------------
        # SCENARIO B CONCLUSION CARD
        # -----------------------------------------------------
        st.markdown('<div style="background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); border: 1px solid #4338ca; border-left: 5px solid #00ff88; border-radius: 10px; padding: 18px; margin-top: 15px;">', unsafe_allow_html=True)
        st.markdown("### 💡 " + ("Scenario B Engineering Conclusion: Busway Priority & The 08:18 Transit Cutoff" if is_en else "情境 B 核心工程結論：大眾運輸專用道效用優勢與「08:18 決策臨界線」"))
        if is_en:
            st.markdown("""
            * **1. Busway & Green Bridge Priority (07:15 - 08:08 AM)**:
              * On this 28.8km corridor, **Private Cars are barred from the Eleanor Schonell Green Bridge**, requiring cars to detour through congested arterials and pay **$14.50 daily UQ parking**.
              * When departing before 08:08 AM, **Combo (24.0 pts)** outperforms Private Driving (6.9 - 12.5 pts). Dedicated transit infrastructure in long corridors significantly enhances transit competitiveness.
            * **2. The First-Mile Walking Penalty Threat (07:52 AM Threshold)**:
              * Standard 50¢ Transit requires walking 2.2km, taking 68 minutes in total.
              * A commuter walking to the bus must leave before **07:52 AM**. Departing after 07:52 causes arrival delay, eroding the 50¢ fare benefit.
            * **3. The '08:18 Cancellation Cutoff'**:
              * On a 28.8km trip, driving takes 42 minutes.
              * Once departure passes **08:18 AM**, **no transport mode can reach UQ on time**.
              * Every active, transit, and driving mode incurs negative lateness penalties. At this point, **'Stay Home' (0.0 pts)** yields the highest net utility. This provides an analytical explanation for why commuters opt to cancel morning trips when wake-up delay exceeds 08:18 AM.
            """)
        else:
            st.markdown("""
            * **1. 公車專用道與綠橋在長途走廊之相對優勢（07:15 ～ 08:08 AM）**：
              * 在這條近 29 公里的跨區走廊上，**私家車禁行 Eleanor Schonell 綠橋**，自駕車必須繞行市區平面幹道忍受早晨回堵，並在校內支付高達 **$14.50 的每日停車費**。
              * 只要在 08:08 AM 前出發，**複合接駁（24.0 點）** 憑藉專用公車道直通綠橋，淨效用顯著高於自駕私家車（僅得 6.9 ～ 12.5 點）。專用基礎設施在長途走廊有效提升了大眾運輸之競爭力。
            * **2. 第一哩路步行時間門檻（07:52 AM）**：
              * 純 50¢ 公車需從家門口步行 2.2 公里到車站，總通勤長達 68 分鐘。
              * 步行接駁的通勤者**最晚須於 07:52 AM 前出發**。若超過 07:52，公車行程將超過 09:00 門檻而產生遲到扣分，淨得分迅速下降。
            * **3. 「08:18 全體行程取消臨界線」（The 08:18 Cancellation Cutoff）**：
              * 在 28.8km 長途走廊，開車亦需要約 42 分鐘。
              * 只要出發時間越過 **08:18 AM**，**任何運具均無法在 09:00 前抵達昆士蘭大學**。
              * 所有交通運具之淨得分均受遲到懲罰而轉為負值。此時 **「🛏️ 取消行程留在家中（0.0 點）」成為淨效用最高之選項**。這從決策動力學解釋了：當出發時間延誤過久而無法準時抵達時，通勤者傾向直接取消行程。
            """)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")

    # -------------------------------------------------------------
