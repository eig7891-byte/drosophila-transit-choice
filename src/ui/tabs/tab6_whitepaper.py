"""
Tab 6: Transit Policy and Engineering White Paper.
"""
import streamlit as st

def render_tab6_whitepaper(is_en: bool):
    st.markdown("### 🏛️ " + ("Brisbane Transit Policy & Engineering White Paper" if is_en else "布里斯本大眾交通工程規劃建議書"))

    if is_en:
        st.markdown(r"""
        Based on multi-objective valence arbitration in the Drosophila connectome (Kenyon Cells - MBON - DAN) and 10,000 Monte Carlo commuter traces across Brisbane corridors, this white paper presents three engineering recommendations for the **Queensland Department of Transport and Main Roads (TMR)**, **Translink**, and the **Brisbane City Council (BCC)**.

        Parking rates in the Brisbane CBD already rank among the highest in Australia ($24 to $38 per day). Instead of adding extra parking charges, this framework focuses on three engineering priorities: **Mobility (Speed)**, **Flexibility (Frequency)**, and **Accessibility (First/Last Mile Micro-Mobility)**.

        ---

        #### 1. Mobility (Speed Optimization): Mitigating Travel Delay via Dedicated Busways
        * **Simulation Findings**:
          * Dropping fare from $4.50 to $0.50 increases transit mode share from **35.1% to 39.6%**, but leaves **47.3% of commuters driving** due to high suburban car ownership and lack of first-mile feeder assets.
          * High-income corporate commuters have low NPF levels and show low price sensitivity. Their modal choice is largely governed by travel time delay.
          * When transit speed increases by 30% via Brisbane Metro (Policy 3), transit mode share climbs to **46.6%**, reducing car use down to **41.8%**.
        * **Connectome Neurological Mechanism**:
          * In the fruit fly brain, delay punishment scales non-linearly: $PPL1_{delay} \propto (T_{transit})^{1.3}$.
          * Cutting 15–20 minutes of travel delay removes the steepest gradient of the PPL1 aversion curve, increasing MBON01 approach firing by **+17.5 Hz**.
        * **Engineering Policy**:
          * Accelerate the northern extension of the Northern Busway to Chermside and southern extensions to Springwood/Logan.
          * Deploy Brisbane Metro high-capacity bi-articulated flash-charging vehicles with full physical segregation, guaranteeing commercial speeds above 45 km/h.
          * Implement **Transit Signal Priority (TSP)** across 30 congested intersections along Gympie Road and Logan Road to eliminate red-light queues.

        ---

        #### 2. Flexibility (Turn-up-and-Go Frequency): Eliminating Timetable Anxiety
        * **Simulation Findings**:
          * Commuters frequently abandon public transit because 20–30 minute service headways create severe schedule friction.
          * Missing a single bus results in late arrival, wiping out the 30-point workplace punctuality reward.
        * **Connectome Neurological Mechanism**:
          * Long waiting intervals fire anticipatory PPL1 stress neurons. Under morning sleep debt, circadian PDF clock neurons reinforce private vehicle reliance.
          * High-frequency service eliminates timetable calculation from the Central Complex decision network.
        * **Engineering Policy**:
          * Restructure core trunk lines (Northern Busway, South East Busway, Eastern Busway, and Brisbane Metro lines) to a **Turn-up-and-go** standard: **sub-5 minute peak headways** and **sub-10 minute off-peak headways**.
          * Synchronize feeder bus arrivals with trunk lines to compress transfer waiting times below 4 minutes.
          * Install real-time passenger countdown displays at all outer suburban stops to eliminate waiting uncertainty.

        ---

        #### 3. Accessibility (First/Last Mile Micro-Mobility): 50-Cent Multi-Modal Integration
        * **Simulation Findings**:
          * During summer temperatures above 32°C, active transport decreases significantly (cycling drops from 27.5% to 7.8%), and outer suburban residents face an 800m unshaded walk to the nearest bus stop.
          * Over 85% of displaced cyclists transfer to transit, increasing peak-hour transit vehicle occupancy.
        * **Connectome Neurological Mechanism**:
          * High subtropical heat stimulates peripheral TRP ion channels, driving PPL1 fatigue above 40 points and depressing MBON01 firing below the activation threshold.
        * **Engineering Policy**:
          * **50¢ Micro-Mobility Integration**: Extend the Translink 50-cent fare umbrella to council-contracted shared e-scooters and e-bikes (Neuron / Beam). Commuters checking in at a busway or rail station within 15 minutes receive a 50-cent integrated feeder fare.
          * **Suburban On-Demand Micro-Transit**: Deploy electric feeder shuttle vans connecting low-density cul-de-sacs in outer corridors (Logan, Carindale, Mt Gravatt) directly to rapid busway stations.
          * **Subtropical Shaded Active Corridors**: Plant continuous native Jacaranda and Poinciana canopy trees along major cycle routes to reduce surface radiant heat by 4–6°C.
          * Mandate air-conditioned End-of-Trip (EOT) showers, lockers, and e-bike charging stations for all major commercial developments under the *Brisbane City Plan 2014*.
        """)
    else:
        st.markdown(r"""
        本建議書基於果蠅大腦多目標價值仲裁模型（Kenyon Cells - MBON - DAN）與 10,000 名布里斯本通勤者的蒙地卡羅大數據模擬結果，向 **昆士蘭交通與主幹道部 (TMR)**、**Translink** 及 **布里斯本市政府 (BCC)** 提出具體工程規劃建言。

        考量到布里斯本 CBD 商業停車費已高居全澳前列（單日高達 $24 至 $38 澳幣），進一步課徵停車附加費已達邊際效益遞減且引發強烈民怨。本規劃書全面轉向**三大工程主軸：「Mobility 速度提升」、「Flexibility 班距彈性」與「Accessibility 第一哩微移動整合」**：

        ---

        #### 1. Mobility（速度提升）：消滅「PPL1 延遲之痛」—— 加速布里斯本 Metro 專用路權
        * **模擬數據發現**：
          * 票價由舊制 $4.50 降至 $0.50 時，大眾運輸佔比從 **35.1% 提升至 39.6%**，但仍有 **47.3% 的通勤者堅持自駕開車**（主因外圍郊區高達 95% 擁車率，且缺乏第一哩微移動工具）。
          * 高薪自駕群體體內 NPF 濃度低，對票價降幅鈍化；其行為完全由旅行時間延遲所主導。
          * 當結合專用路權使公車**提速 30%** (Policy 3) 時，大眾運輸佔比提升至 **46.6%**，自駕開車率顯著壓制至 **41.8%**！
        * **果蠅連接體神經機制**：
          * 在果蠅評價迴路中，時間延遲懲罰呈非線性指數增長：$PPL1_{delay} \propto (T_{transit})^{1.3}$。
          * 消滅 15 至 20 分鐘的壅塞延誤，直接截斷了 PPL1 痛感曲線最陡峭的區段，使 MBON01 放電增加 **+17.5 Hz**。
        * **具體工程策略**：
          * 加速推動 Northern Busway 往北延伸至 Chermside，以及南向延伸至 Springwood / Logan 走廊。
          * 全面普及 Brisbane Metro 雙節電動大容量載具，配置完全實體隔離的專用路權，確保商用運轉時速維持在 45 km/h 以上。
          * 於 Gympie Road 與 Logan Road 等 30 處核心瓶頸路口全面建置**主幹道公車號誌優先系統 (Transit Signal Priority, TSP)**，掃除停等紅燈的時間懲罰。

        ---

        #### 2. Flexibility（班距彈性）：消除發車時間焦慮 —— 實施「隨到隨走」班表
        * **模擬數據發現**：
          * 許多通勤者拒絕搭乘公車並非因為票價，而是因為郊區路線 20 至 30 分鐘一班的長班距帶來高度時間摩擦。
          * 只要錯過一班車，抵達時間即嚴重延誤，導致 30 點準時得點瞬間歸零。
        * **果蠅連接體神經機制**：
          * 長時間的不確定性候車會引發 PPL1 預期性焦慮神經元放電。在晨間睡眠負債下，PDF 晝夜時鐘神經元會強化對開車出行的依賴。
          * 高頻率的「隨到隨走 (Turn-up-and-go)」班表能徹底將發車時間約束自中央複合體決策樹中移除。
        * **具體工程策略**：
          * 將主要幹線（南區 Busway、北區 Busway、東區 Busway 及 Metro 走廊）全面轉型為 **隨到隨走 (Turn-up-and-go)**：**尖峰班距 &lt; 5 分鐘**，**離峰班距 &lt; 10 分鐘**。
          * 調整社區接駁公車班次，精確對接幹線抵達時間，將轉乘等候壓縮至 4 分鐘內。
          * 於全線郊區站點配置高精度即時動態到站看板，徹底消除乘客等候的不確定焦慮。

        ---

        #### 3. Accessibility（第一哩可達性）：克服亞熱帶酷暑 —— 50-Cent 微移動與接駁整合
        * **模擬數據發現**：
          * 夏季氣溫超過 32°C 時，主動式交通顯著受阻（自行車分流率自 27.5% 下降至 7.8%），外圍郊區居民常因住家距離車站有 800 公尺無遮陰上坡路而放棄公車。
          * 高溫環境下約 85% 的原自行車騎士轉向大眾運輸，增加夏日尖峰車廂運量。
        * **果蠅連接體神經機制**：
          * 高溫強烈激活果蠅周邊感覺的 TRP 離子通道，使 PPL1 疲勞放電突破 40 點，壓低 MBON01 放電致使通勤者迴避步行與騎車。
        * **具體工程策略**：
          * **50¢ 微移動跨界整合**：將 Translink 50-Cent 票價傘擴展至布里斯本市府簽約的共享電動滑板車與電動自行車 (Beam / Neuron)。凡在進出 Busway 或火車站前後 15 分鐘內使用，第一哩／最後一哩費用同樣僅收 50 Cent。
          * **外圍郊區需求反應式微型公車 (On-Demand Micro-Transit)**：在 Logan、Carindale、Mt Gravatt 等低密度無袋社區，開行全電動微型接駁車，提供社區端點至 Busway 站點的無縫接送。
          * **亞熱帶林蔭專用車道**：沿核心自行車道廣植本土藍花楹 (Jacaranda) 與鳳凰木 (Poinciana)，提供連續林蔭，將路面熱輻射降低 4 至 6°C。
          * 於《布里斯本城市規劃綱要 (City Plan 2014)》中強制要求商業大樓按比例設置冷氣淋浴間、乾衣置物櫃與電動載具安全充電座。
        """)

    # -------------------------------------------------------------
