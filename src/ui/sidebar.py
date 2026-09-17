"""
Sidebar controls and parameter state for the Drosophila Transit Choice Dashboard.
"""
from dataclasses import dataclass
from typing import List, Dict, Any
import streamlit as st

from src.core import InternalNeuromodulatorState, CommuteOption, DrosophilaCommuteBrain
from src.simulation import BRISBANE_CORRIDORS, CommuteCorridor


@dataclass
class SidebarInputs:
    """Encapsulates all user selections and calculated neural states from the sidebar."""
    lang: str
    is_en: bool
    preset: str
    npf_val: float
    oa_val: float
    ser_val: float
    pdf_val: float
    selected_corridor: CommuteCorridor
    fare_val: float
    parking_val: float
    weather_val: float
    transit_prod: float
    current_state: InternalNeuromodulatorState
    current_options: List[CommuteOption]
    brain: DrosophilaCommuteBrain
    eval_res: Dict[str, Any]


def render_sidebar() -> SidebarInputs:
    """Render the sidebar controls and return the active configuration state."""
    # -------------------------------------------------------------
    # Sidebar Language Toggle (Top of Sidebar)
    # -------------------------------------------------------------
    st.sidebar.markdown("### Language / 語言選擇")
    lang = st.sidebar.radio(
        "Select Language / 選擇語言",
        ["繁體中文", "English (AU)"],
        index=0,
        label_visibility="collapsed"
    )
    is_en = (lang == "English (AU)")

    # -------------------------------------------------------------
    # Parameters & Presets
    # -------------------------------------------------------------
    st.sidebar.markdown("---")
    st.sidebar.title(" " + ("Commuter Control Panel" if is_en else "通勤參數控制台"))

    preset_options = [
        ("Custom Parameters", "自訂參數"),
        (" Tertiary / University Student", " 大專院校學生 (學生族群)"),
        (" CBD Corporate Executive", " CBD 高薪主管"),
        (" Fitness Cyclist", " 運動狂熱者"),
        (" Suburban Commuter Family", " 郊區通勤家庭")
    ]
    preset_choices = [p[0] if is_en else p[1] for p in preset_options]
    preset = st.sidebar.selectbox(
        "Choose Commuter Archetype:" if is_en else "選擇通勤者原型：",
        preset_choices
    )

    default_npf, default_oa, default_ser, default_pdf = 0.50, 0.50, 0.50, 0.50

    if "Student" in preset or "學生" in preset:
        default_npf, default_oa, default_ser, default_pdf = 0.95, 0.30, 0.65, 0.40
    elif "Executive" in preset or "主管" in preset:
        default_npf, default_oa, default_ser, default_pdf = 0.10, 0.25, 0.20, 0.90
    elif "Cyclist" in preset or "運動" in preset:
        default_npf, default_oa, default_ser, default_pdf = 0.40, 0.95, 0.50, 0.15
    elif "Suburban" in preset or "郊區" in preset:
        default_npf, default_oa, default_ser, default_pdf = 0.60, 0.35, 0.50, 0.55

    st.sidebar.markdown("### " + ("Neuromodulator State" if is_en else "果蠅神經調控劑濃度"))
    npf_val = st.sidebar.slider(
        "NPF: Budget Pressure & Price Sensitivity" if is_en else "NPF 財務飢餓度 (省錢渴望 / 預算壓力)",
        0.0, 1.0, default_npf, 0.05,
        help="High NPF drives intense desire to save money" if is_en else "高 NPF 代表極度渴望省錢 (如同果蠅飢餓渴望吃糖)"
    )
    oa_val = st.sidebar.slider(
        "Octopamine: Motor Vigor & Physical Drive" if is_en else "Octopamine 辛弗林 (體能活力 / 運動耐力)",
        0.0, 1.0, default_oa, 0.05,
        help="Octopamine stimulates flight muscles and reduces fatigue aversion" if is_en else "辛弗林刺激飛行肌耐力，降低騎車乳酸疲勞抗拒"
    )
    ser_val = st.sidebar.slider(
        "Serotonin: Transit Delay Patience" if is_en else "Serotonin 血清素 (等待耐心 / 延遲容忍)",
        0.0, 1.0, default_ser, 0.05,
        help="Serotonin dampens delay discounting and impulse" if is_en else "血清素抑制衝動，提高在慢車上的耐心"
    )
    pdf_val = st.sidebar.slider(
        "PDF: Circadian Morning Sleep Debt" if is_en else "PDF 晝夜睡眠負債 (晨間賴床傾向)",
        0.0, 1.0, default_pdf, 0.05,
        help="High sleep debt makes 7:00 AM departures painful, favoring driving" if is_en else "高睡眠負債使早起極度痛苦，偏好開車"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### " + ("Brisbane Environment" if is_en else "布里斯本走廊與環境"))
    corridor_names = [c.name for c in BRISBANE_CORRIDORS]
    selected_corridor_name = st.sidebar.selectbox("Commuter Corridor:" if is_en else "通勤走廊：", corridor_names, index=0)
    selected_corridor = next(c for c in BRISBANE_CORRIDORS if c.name == selected_corridor_name)

    fare_val = st.sidebar.slider(
        "Transit One-Way Fare (AUD):" if is_en else "大眾運輸單程票價 (AUD)：",
        0.0, 8.0, 0.50, 0.50,
        help="Queensland Translink 50-cent fare is $0.50" if is_en else "昆士蘭 Translink 50-cent 政策設為 0.50"
    )
    parking_val = st.sidebar.slider(
        "CBD Parking + Fuel (AUD):" if is_en else "CBD 每日停車費 + 油資 (AUD)：",
        10.0, 45.0, float(selected_corridor.car_parking_fuel_cost), 1.0
    )
    weather_val = st.sidebar.slider(
        "Weather Heat Index:" if is_en else "天氣氣溫/熱浪指數 (Heat Index)：",
        0.0, 1.0, 0.25, 0.05,
        help="0.0 = Pleasant 20°C; 1.0 = 36°C humid summer storm" if is_en else "0.0 = 舒適涼秋 20°C；1.0 = 酷暑雷雨 36°C"
    )
    transit_prod = st.sidebar.slider(
        "In-Transit Productivity (Reading/Relaxing):" if is_en else "大眾運輸可利用生產力 (讀書/放鬆)：",
        0.0, 1.0, 0.60, 0.05
    )

    # Evaluate Current State for Real-Time Tabs
    current_state = InternalNeuromodulatorState(npf_val, oa_val, ser_val, pdf_val)
    t_car = selected_corridor.car_travel_time_min
    t_transit = selected_corridor.transit_travel_time_min
    t_bike = selected_corridor.bike_travel_time_min

    current_options = [
        CommuteOption(
            name="Car",
            travel_time_min=t_car,
            monetary_cost_aud=parking_val,
            physical_effort=0.05,
            departure_time_hr=9.0 - (t_car / 60.0),
            comfort_index=0.95
        ),
        CommuteOption(
            name="Transit_50c",
            travel_time_min=t_transit,
            monetary_cost_aud=fare_val * 2.0,
            physical_effort=0.15,
            departure_time_hr=9.0 - (t_transit / 60.0),
            comfort_index=0.75
        ),
        CommuteOption(
            name="Bicycle",
            travel_time_min=t_bike,
            monetary_cost_aud=2.0,
            physical_effort=0.85,
            departure_time_hr=9.0 - (t_bike / 60.0),
            comfort_index=0.45
        )
    ]

    brain = DrosophilaCommuteBrain(target_arrival_hr=9.0)
    eval_res = brain.decide_commute(
        current_options, current_state,
        weather_heat_index=weather_val,
        transit_productivity=transit_prod
    )

    return SidebarInputs(
        lang=lang,
        is_en=is_en,
        preset=preset,
        npf_val=npf_val,
        oa_val=oa_val,
        ser_val=ser_val,
        pdf_val=pdf_val,
        selected_corridor=selected_corridor,
        fare_val=fare_val,
        parking_val=parking_val,
        weather_val=weather_val,
        transit_prod=transit_prod,
        current_state=current_state,
        current_options=current_options,
        brain=brain,
        eval_res=eval_res
    )
