"""
Tab 7: Future Urban Horizons (2032/2040/2050 Settings and Master Plans).
"""
import streamlit as st
import pandas as pd

def render_tab7_future(is_en: bool):
    st.markdown("## " + (" Future Urban Horizons: Multi-Decadal Urban Visions & Engineering Parameters" if is_en else " 未來路網願景規劃：多年代城市規劃與工程參數矩陣"))
    st.markdown(
        "Transportation systems cannot be evaluated solely on current physical constraints. This module incorporates official statutory master plans from the **Queensland Department of Transport and Main Roads (TMR)**, **Translink**, and **Brisbane City Council (BCC)** to establish physical infrastructure parameters across four distinct eras (2026, 2032, 2040, and 2050)."
        if is_en else
        "城市交通決策無法單憑當前既有的物理瓶頸作為終極定論。本模組完整導入**昆士蘭州交通與主幹道部 (TMR)**、**Translink** 及 **布里斯本市政府 (BCC)** 之法定總體規劃，建立橫跨四大年代（2026、2032、2040 與 2050）的實體工程參數矩陣："
    )

    st.markdown("### " + (" Statutory Document Foundations & Major Infrastructure Upgrades" if is_en else " 法定規劃文件依據與重大工程升級指標"))

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown('<div class="character-card" style="text-align: left; padding: 16px;">', unsafe_allow_html=True)
        st.markdown('#### ' + ("2032 Olympic Games Legacy" if is_en else "2032 奧運與帕運遺產期"))
        if is_en:
            st.markdown("""
            * **Official Basis**:
              * *Cross River Rail Delivery Authority*
              * *Brisbane Metro Business Case (BCC)*
              * *Green Bridges Program (BCC)*
            * **Infrastructure Targets**:
              * **Cross River Rail (CRR)**: 10.2 km line, 5.9 km twin tunnels, 4 new underground stations (Albert St CBD core, Boggo Rd, Woolloongabba, Roma St). Expands core rail capacity to 24 trains/hour/track (+50%).
              * **Brisbane Metro Phase 1 & 2**: 60 electric 24m bi-articulated vehicles. Turn-up-and-go 3-min peak headways with Northern Busway extension to Chermside.
              * **Green Bridges**: Kangaroo Point Green Bridge cuts pedestrian/cyclist trip to CBD Alice St from 25 min to **6 min**.
            """)
        else:
            st.markdown("""
            * **法定規劃依據**：
              * *Cross River Rail Delivery Authority*
              * *Brisbane Metro Project Business Case*
              * *BCC 綠色天橋綱領 (Green Bridges Program)*
            * **核心實體工程指標**：
              * **Cross River Rail (CRR)**：長 10.2 公里、含 5.9 公里雙孔地底隧道，新增四大深層地下車站（Albert St CBD 正核心、Boggo Rd、Woolloongabba、Roma St）。軌道尖峰容量提升至每小時 24 班 (+50%)。
              * **Brisbane Metro Phase 1 & 2**：60 輛 24 公尺雙節閃充電動公車，尖峰班距 3 分鐘，延伸至北部 Chermside 專用路權。
              * **綠色天橋群**：袋鼠角天橋完工，步行與騎車進 CBD 由繞行 Story Bridge 25 分鐘壓縮至 **6 分鐘**。
            """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_f2:
        st.markdown('<div class="character-card" style="text-align: left; padding: 16px;">', unsafe_allow_html=True)
        st.markdown('#### ' + ("2040 SEQ Regional Plan 2041" if is_en else "2040 東南昆士蘭區域路網期"))
        if is_en:
            st.markdown("""
            * **Official Basis**:
              * *TMR South East Queensland Regional Transport Plan 2041 (SEQ RTP)*
              * *Queensland Cycling Strategy 2017–2027*
              * *BCC Clean, Green, Sustainable 2031*
            * **Infrastructure Targets**:
              * **100% Zero Emission Buses (ZEB)**: Complete electric/hydrogen transition across Translink SEQ. Cabin noise & vibration eliminated; Comfort Index reaches **0.95**.
              * **Principal Cycle Network Plan (PCNP)**: 100% continuous grade-separated priority bikeways.
              * **50% Native Canopy Coverage**: Dense Jacaranda/Poinciana shading reduces surface radiant heat by 5°C, suppressing heat stress.
              * **SEQ Faster Rail**: 160 km/h express services to Gold Coast (35 min) and Sunshine Coast (45 min).
            """)
        else:
            st.markdown("""
            * **法定規劃依據**：
              * *TMR 東南昆士蘭區域交通規劃 2041 (SEQ RTP)*
              * *昆士蘭自行車戰略 (PCNP 2017–2027)*
              * *布里斯本綠色永續綱領 2031*
            * **核心實體工程指標**：
              * **100% 零排放公車 (ZEB)**：Translink 全面汰換為純電與氫能巴士，車廂噪音與柴油震動歸零，舒適度指標達到 **0.95**。
              * **PCNP 連續隔離自行車網**：外圍走廊全線消除斷裂點，實現 100% 實體隔離專用車道。
              * **50% 原生林蔭遮蔭率**：廣植藍花楹與鳳凰木林蔭，將路面熱輻射降低 5°C，消除夏日高溫熱浪威脅。
              * **SEQ 提速鐵路**：布里斯本至黃金海岸縮短至 35 分鐘，至陽光海岸縮短至 45 分鐘。
            """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_f3:
        st.markdown('<div class="character-card" style="text-align: left; padding: 16px;">', unsafe_allow_html=True)
        st.markdown('#### ' + ("2050 Net-Zero Autonomous Mobility" if is_en else "2050 淨零自駕與微移動期"))
        if is_en:
            st.markdown("""
            * **Official Basis**:
              * *Queensland Climate Action Plan 2050 (Net Zero Target)*
              * *Infrastructure Australia 2021 Plan (Future CAV Mobility)*
            * **Infrastructure Targets**:
              * **Connected & Autonomous Electric Vehicles (CAVs)**: On-demand multi-passenger shared pods serve suburban feeder routes.
              * **Dynamic Road User Charging (RUC)**: $20 peak congestion pricing applied to single-occupancy private pods entering CBD.
              * **50¢ Integrated Autonomous Feeders**: Zero-wait micro-transit connecting suburban doorsteps to rapid transit hubs.
              * **National High-Speed Rail (HSRA)**: 300+ km/h inter-city link operational along the east coast.
            """)
        else:
            st.markdown("""
            * **法定規劃依據**：
              * *昆士蘭氣候行動計畫 2050 淨零碳排目標*
              * *澳洲國家基礎設施機構 (Infrastructure Australia) 自駕載具願景*
            * **核心實體工程指標**：
              * **自駕聯網電動載具 (CAV)**：隨選多乘員自駕接駁艙普及於外圍社區最後一哩。
              * **尖峰動態道路擁擠收費 (RUC)**：針對進入 CBD 之單人自駕車課徵 $20 尖峰擁擠費，杜絕空車壅塞。
              * **50¢ 一體化自駕接駁微移動**：住家門口至 Busway/捷運站點實現 2 分鐘隨叫隨到零等候銜接。
              * **東海岸高鐵 (HSRA)**：時速 300 公里以上城際高鐵全線貫通。
            """)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### " + ("Multi-Decadal Physical Corridor Parameter Matrix (2026 vs 2032 vs 2040 vs 2050)" if is_en else "多年代實體走廊參數矩陣對比（2026 vs 2032 vs 2040 vs 2050）"))

    matrix_df = pd.DataFrame([
        {
            "Corridor / Parameter": "Logan Central (26.5 km) - Transit Time" if is_en else "Logan Central 走廊 (26.5 km) - 公車耗時",
            "2026 Baseline": "75 - 85 min (Mixed)" if is_en else "75 - 85 分 (混流慢車)",
            "2032 Olympics": "48 min (CRR Express)" if is_en else "48 分 (CRR 地底特快)",
            "2040 SEQ Plan": "38 min (Faster Rail + ZEB)" if is_en else "38 分 (提速鐵路+ZEB)",
            "2050 Net-Zero": "32 min (Integrated MaaS)" if is_en else "32 分 (自駕整合 MaaS)"
        },
        {
            "Corridor / Parameter": "Chermside (10.5 km) - Transit Time" if is_en else "Chermside 走廊 (10.5 km) - 公車耗時",
            "2026 Baseline": "50 min (Gympie Rd Queue)" if is_en else "50 分 (車陣回堵)",
            "2032 Olympics": "32 min (Metro Busway)" if is_en else "32 分 (Metro 專用路權)",
            "2040 SEQ Plan": "25 min (Metro + TSP)" if is_en else "25 分 (全線號誌優先)",
            "2050 Net-Zero": "20 min (Full Segregation)" if is_en else "20 分 (全實體立體路權)"
        },
        {
            "Corridor / Parameter": "Transit Cabin Comfort Index (0 to 1)" if is_en else "大眾運輸車室舒適度指標 (0 至 1)",
            "2026 Baseline": "0.75 (Standard Diesel)" if is_en else "0.75 (常態柴油公車)",
            "2032 Olympics": "0.85 (Metro Flash-Charge)" if is_en else "0.85 (Metro 雙節電動車)",
            "2040 SEQ Plan": "0.95 (100% ZEB Silent)" if is_en else "0.95 (100% 靜音純電 ZEB)",
            "2050 Net-Zero": "1.00 (Autonomous Pod)" if is_en else "1.00 (零晃動智慧自駕艙)"
        },
        {
            "Corridor / Parameter": "Suburban Bikeway Infrastructure Effort" if is_en else "郊區自行車基礎設施努力度阻力",
            "2026 Baseline": "0.95 (Fragmented / Heavy Trucks)" if is_en else "0.95 (斷裂路網 / 砂石車混流)",
            "2032 Olympics": "0.75 (Green Bridges Active)" if is_en else "0.75 (綠色天橋群完工)",
            "2040 SEQ Plan": "0.50 (100% PCNP Dedicated)" if is_en else "0.50 (100% PCNP 實體隔離)",
            "2050 Net-Zero": "0.40 (Continuous Grade-Sep)" if is_en else "0.40 (全立體林蔭綠道)"
        },
        {
            "Corridor / Parameter": "Summer Heatwave Penalty Reduction" if is_en else "夏季熱浪體感熱壓力折減率",
            "2026 Baseline": "0% (Unshaded Black Asphalt)" if is_en else "0% (無遮陰柏油曝曬)",
            "2032 Olympics": "20% (Early Canopy Growth)" if is_en else "20% (初期林蔭廊道)",
            "2040 SEQ Plan": "60% (50% Mature Tree Canopy)" if is_en else "60% (50% 成熟樹冠覆蓋降溫5°C)",
            "2050 Net-Zero": "75% (Microclimate Misting)" if is_en else "75% (微氣候噴霧降溫路網)"
        },
        {
            "Corridor / Parameter": "CBD Car Parking + Access Cost (AUD)" if is_en else "私家車 CBD 停車 + 進城通行成本 (AUD)",
            "2026 Baseline": "$28.00 (Market Parking)" if is_en else "$28.00 (市價停車費)",
            "2032 Olympics": "$34.00 (Olympic Zones)" if is_en else "$34.00 (奧運管制區加成)",
            "2040 SEQ Plan": "$38.00 (Space Consolidation)" if is_en else "$38.00 (車位總量管制縮減)",
            "2050 Net-Zero": "$48.00 ($20 RUC + Parking)" if is_en else "$48.00 (包含 $20 動態擁擠費)"
        }
    ])
    st.table(matrix_df)



    # -------------------------------------------------------------
