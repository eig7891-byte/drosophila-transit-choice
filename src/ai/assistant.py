"""
Drosophila Transit AI Guide (Gemini 3.8 Flash)
Rock-Solid Clickable Popover Implementation:
- 100% Native Streamlit Popover Widget:
  * Avatar in bottom-right corner is the actual native interactive button.
  * Clicking the avatar or speech bubble opens the dialogue immediately.
  * ZERO dark backdrop overlay (background stays completely bright and normal).
  * Screen is 100% freely scrollable and interactive while the dialog is open.
  * NO fixed bottom input bar stuck across the screen.
  * Synchronized language: Chinese interface -> Chinese AI, English interface -> English AI.
  * Mode selection inside dialog: Professional Engineering vs Ultra-Simple Plain Language (ELI5).
  * Ultra-concise answers (2-3 sentences max, simple, punchy, direct to the point).
  * NO model names displayed.
"""

import os
import time
import base64
import streamlit as st
from google import genai
from PIL import Image

# Paths to avatar images
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ORIG_AVATAR_PATH = os.path.join(_ROOT, "assets", "fly_engineer_avatar.jpg")
THUMB_AVATAR_PATH = os.path.join(_ROOT, "assets", "fly_engineer_avatar_thumb.jpg")

@st.cache_data
def get_avatar_b64() -> str:
    """Load and cache the base64 string of the fly engineer avatar (prefers optimized thumbnail)."""
    if not os.path.exists(THUMB_AVATAR_PATH) and os.path.exists(ORIG_AVATAR_PATH):
        try:
            im = Image.open(ORIG_AVATAR_PATH)
            im.thumbnail((128, 128))
            im.save(THUMB_AVATAR_PATH, quality=90)
        except Exception:
            pass

    target_path = THUMB_AVATAR_PATH if os.path.exists(THUMB_AVATAR_PATH) else ORIG_AVATAR_PATH
    if os.path.exists(target_path):
        with open(target_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

def get_gemini_client():
    """Initialize Google GenAI client from secrets or environment."""
    api_key = None
    if hasattr(st, "secrets") and "gemini" in st.secrets and "api_key" in st.secrets["gemini"]:
        api_key = st.secrets["gemini"]["api_key"]
    elif "GEMINI_API_KEY" in os.environ:
        api_key = os.environ["GEMINI_API_KEY"]
    else:
        import toml
        secrets_file = os.path.join(r"c:\Users\eig78\Desktop\UNISQ\Side Project\.streamlit\secrets.toml")
        if os.path.exists(secrets_file):
            data = toml.load(secrets_file)
            api_key = data.get("gemini", {}).get("api_key")

    if not api_key:
        return None
    return genai.Client(api_key=api_key)

SYSTEM_KNOWLEDGE_PROMPT = """You are the 'Drosophila Transit AI Guide' (果蠅交通工程師解說員), an objective engineering assistant representing a Master's student researcher in computational transport engineering.
You explain the Brisbane Transit & FlyWire connectome simulation dashboard.

STRICT CONCISENESS & CLARITY RULES:
- ALL ANSWERS MUST BE ULTRA-CONCISE, ACCURATE, AND DIRECT TO THE POINT.
- Maximum 2 to 3 short sentences, or 3 brief bullet points.
- Strictly under 60 words (English) or 75 characters (Chinese).
- Absolutely NO filler, NO preamble, and NO repeating the question.
- DO NOT MENTION ANY AI MODEL NAMES (never say Gemini, Flash, etc.).
- ZERO EMOJIS. Never use emojis anywhere in the response.

SYSTEM FACTS & RESEARCH GROUNDING:
- Biological Connectome: HHMI Janelia male-cns:v1.0 3D skeleton points coupled with the FlyWire whole-brain connectome (Dorkenwald et al. / Schlegel et al., Nature 2024: 138,327 neurons, >130M synapses).
- Neural Decision Architecture:
  * Kenyon Cells (KC): Sparse multimodal encoding of transit cost, delay, walking fatigue, and heat.
  * PAM Dopamine (PAM01): Positive reward signal encoding monetary savings, travel speed, and comfort.
  * PPL1 Dopamine (PPL101): Aversive punishment signal encoding parking fees, in-transit delays, and physical walking fatigue.
  * MBON01 (Cholinergic): Approach output neuron driving selection of transit or active transport when reward exceeds pain.
  * MBON11 (GABAergic): Avoidance output neuron providing lateral inhibition to veto unfavorable choices.
  * Neuromodulators: NPF (budget urgency), Octopamine (vigor/fitness), Serotonin (delay patience), PDF (circadian sleep debt).
- 7 Greater Brisbane Corridors: Springwood local (5.2 km), Springwood UQ (28.8 km), Chermside (10.5 km), Indooroopilly (7.2 km), Mt Gravatt (13.8 km), Logan Central (26.5 km), Carindale (11.0 km).
- Empirical Calibration Provenance: Ingested 24,772,971 real Translink Go Card transactions (July vs August 2024, Queensland Open Data) and Q2 2025-26 Report. SciPy MLE/MAP optimization reduced loss by 72.5% (114.86 to 31.60) and RMSE to 1.99% (SEQ total transit error 0.54%).
- 10,000-Commuter Simulation Results:
  * Policy 1 (Current 50c): Car 51.4%, Transit 36.0%, Bike 12.6%. Subsidies alone leave outer car reliance at 54–58% because 1.8–2.2 km walks under subtropical heat trigger severe PPL1 fatigue.
  * Policy 2 (Old Fare $4.50): Car 53.8%, Transit 32.6%, Bike 13.6%.
  * Policy 3 (50c + Brisbane Metro +30% speed boost): Car drops to 45.6%, Transit rises to 43.5% (Speed beats subsidies).
  * Policy 4 (Green Mobility All-In): Car 44.9%, Transit 42.7%, Bike 12.4%.
  * First-Mile Deficit: 90.5% in outer suburbs lack e-scooters. Providing feeder micro-mobility raises outer transit capture from 6.2% to 17.5%.
  * Climate Barrier: Temperatures >34°C activate TRP channels, cutting active travel by 38.5% with 85% diverting to transit.
"""

def generate_ai_response(user_question: str, is_en: bool, is_eli5: bool, context_dict: dict = None) -> str:
    """Generate concise grounded answer using Gemini Flash."""
    client = get_gemini_client()
    if not client:
        return "Gemini API Key not configured. Please check `.streamlit/secrets.toml`."

    context_str = ""
    if context_dict:
        context_str = f"""
[CONTEXT: Corridor={context_dict.get('corridor', 'Chermside')}, Fare=${context_dict.get('fare', 0.5):.2f}, Parking=${context_dict.get('parking', 35):.2f}, Heat={context_dict.get('heat', 0.25)}]
"""

    if is_en:
        if is_eli5:
            mode_inst = """
[MODE: Ultra-Simple English (ELI5)]
- Explain in plain everyday language. Zero academic jargon. Zero emojis.
- Simple analogies: MBON01 = approach accelerator, PPL1 = friction brake, Dopamine = reward incentive, Summer sun = heat barrier.
- Exactly 2 short punchy sentences. Under 45 words.
"""
        else:
            mode_inst = """
[MODE: Professional Academic English]
- Tone: Master's level engineering student. Simple concrete verbs. Zero emojis.
- Strictly NO first-person pronouns ('I', 'we', 'our'). No AI buzzwords.
- 2 to 3 concise, punchy sentences stating data and mechanism directly (under 55 words).
"""
    else:
        if is_eli5:
            mode_inst = """
[MODE: 超簡單白話解說 (ELI5)]
- 徹底不用艱深術語，嚴禁任何表情符號 (No emojis)。
- 用直觀比喻：MBON01 是「前進油門」，PPL1 是「摩擦剎車」，多巴胺是「獎勵誘因」，夏日高溫是「體能路障」。
- 嚴格限制在 2 句短句內講完，秒懂明瞭（60 字以內）。
"""
        else:
            mode_inst = """
[MODE: 繁體中文 - 專業工程分析]
- 嚴謹客觀的交通與神經工程分析，嚴禁任何表情符號 (No emojis)。
- 嚴格不使用第一人稱（絕不使用「我」、「我們」）。
- 以 2 到 3 句短句直接給出數據結論與神經機轉，精準明瞭（75 字內）。
"""

    full_prompt = f"{SYSTEM_KNOWLEDGE_PROMPT}\n{context_str}\n{mode_inst}\n[QUESTION]: {user_question}"

    models_to_try = ["gemini-3.8-flash", "gemini-3.6-flash"]
    for model_name in models_to_try:
        try:
            res = client.models.generate_content(
                model=model_name,
                contents=full_prompt
            )
            if res and res.text:
                return res.text.strip()
        except Exception:
            time.sleep(1)
            continue

    return "System is currently busy. Please try again in a moment." if is_en else "系統目前繁忙，請稍候片刻再試一次。"

def inject_fly_engineer_floating_widget(is_en: bool, context_dict: dict = None):
    """
    100% Native Streamlit Popover Widget.
    - Avatar button is natively clickable in bottom-right corner.
    - Zero dark backdrop, zero screen dimming.
    - Full screen remains 100% freely scrollable.
    - No bottom bar across the screen.
    - Automatic language sync + ELI5 ultra-simple option.
    - Ultra-concise answers, no model names.
    """
    b64_img = get_avatar_b64()

    if "fly_ai_history" not in st.session_state:
        st.session_state.fly_ai_history = []

    speech_text = "Have a question? Ask me!" if is_en else "想問什麼嗎？問我吧！"
    header_title = "Drosophila Transit AI Guide" if is_en else "果蠅工程師 AI 解說員"
    header_sub = "Janelia FlyWire x Brisbane Transit Copilot" if is_en else "Janelia FlyWire x 布里斯本交通決策夥伴"
    close_hint = "[Click outside or avatar to close]" if is_en else "[點擊外部或頭像關閉]"

    # 1. CSS with ROBUST selectors (matching Streamlit 1.55+ DOM structure)
    st.markdown(f"""
    <style>
    /* Fixed container for the popover at bottom-right */
    div[data-testid="stPopover"],
    .stPopover {{
        position: fixed !important;
        bottom: 25px !important;
        right: 25px !important;
        z-index: 999999 !important;
        width: 68px !important;
        height: 68px !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }}

    /* Style the popover button into the circular fruit fly engineer avatar */
    button[data-testid="stPopoverButton"],
    div[data-testid="stPopover"] button,
    .stPopover button {{
        width: 68px !important;
        height: 68px !important;
        min-width: 68px !important;
        min-height: 68px !important;
        border-radius: 50% !important;
        background-image: url('data:image/jpeg;base64,{b64_img}') !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        border: 3px solid #ffcc00 !important;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.5) !important;
        cursor: pointer !important;
        transition: transform 0.22s ease, box-shadow 0.22s ease !important;
        padding: 0 !important;
        position: relative !important;
        overflow: visible !important;
    }}

    button[data-testid="stPopoverButton"]:hover,
    div[data-testid="stPopover"] button:hover,
    .stPopover button:hover {{
        transform: scale(1.10) rotate(3deg) !important;
        box-shadow: 0 10px 30px rgba(255, 204, 0, 0.75) !important;
    }}

    /* Hide default text/icons inside popover button */
    button[data-testid="stPopoverButton"] *,
    div[data-testid="stPopover"] button *,
    .stPopover button * {{
        display: none !important;
    }}

    /* Speech bubble popout attached to avatar */
    button[data-testid="stPopoverButton"]::before,
    div[data-testid="stPopover"] button::before,
    .stPopover button::before {{
        content: "{speech_text}" !important;
        position: absolute !important;
        right: 80px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        background: #ffffff !important;
        color: #0f172a !important;
        padding: 8px 14px !important;
        border-radius: 16px 16px 4px 16px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.25) !important;
        border: 2px solid #ffcc00 !important;
        white-space: nowrap !important;
        display: block !important;
        pointer-events: none !important;
    }}

    /* Popover Body Content Box (ZERO backdrop, background stays 100% visible and scrollable) */
    div[data-testid="stPopoverBody"] {{
        width: 440px !important;
        max-width: 92vw !important;
        max-height: 620px !important;
        background: #0f172a !important;
        color: #e2e8f0 !important;
        border: 2px solid #ffcc00 !important;
        border-radius: 16px !important;
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.8) !important;
        padding: 18px !important;
        overflow-y: auto !important;
    }}

    div[data-testid="stPopoverBody"] p,
    div[data-testid="stPopoverBody"] span,
    div[data-testid="stPopoverBody"] label {{
        color: #e2e8f0 !important;
    }}

    div[data-testid="stPopoverBody"]::-webkit-scrollbar {{
        width: 6px;
    }}
    div[data-testid="stPopoverBody"]::-webkit-scrollbar-thumb {{
        background: #475569;
        border-radius: 3px;
    }}
    </style>
    """, unsafe_allow_html=True)

    # 2. Native Popover Element with empty label (prevents any plain text "bar" appearance)
    with st.popover(" ", help="Drosophila Transit AI Guide"):
        # Header (NO model names)
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 2px solid #ffcc00; padding-bottom: 8px; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <img src="data:image/jpeg;base64,{b64_img}" style="width: 42px; height: 42px; border-radius: 50%; border: 2px solid #ffcc00; object-fit: cover;" />
                <div>
                    <div style="font-size: 0.95rem; font-weight: 800; color: #ffcc00; line-height: 1.2;">
                        {header_title}
                    </div>
                    <div style="font-size: 0.72rem; color: #94a3b8;">
                        {header_sub}
                    </div>
                </div>
            </div>
            <div style="font-size: 0.7rem; color: #64748b;">
                {close_hint}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Mode Selection: Synced with page language + ELI5 option
        if is_en:
            style_choice = st.radio(
                "Mode:",
                [" Professional Engineering", " Ultra-Simple Plain Language (ELI5)"],
                index=0,
                horizontal=True,
                key="fly_ai_pop_style_en"
            )
            is_eli5 = (style_choice == " Ultra-Simple Plain Language (ELI5)")
        else:
            style_choice = st.radio(
                "解說模式：",
                [" 專業工程分析", " 超簡單白話解說 (ELI5)"],
                index=0,
                horizontal=True,
                key="fly_ai_pop_style_zh"
            )
            is_eli5 = (style_choice == " 超簡單白話解說 (ELI5)")

        # 4 Quick Question Buttons in 2 columns
        st.markdown("##### " + ("Quick Questions:" if is_en else "常用問題快速提問："))
        q_col1, q_col2 = st.columns(2)
        quick_q = None
        with q_col1:
            if st.button("系統在算什麼？" if not is_en else "What is this simulation?", key="pop_qq_1", use_container_width=True):
                quick_q = "請用簡短一句話說明這套模擬系統在算什麼？" if not is_en else "Explain this simulation in simple words"
            if st.button("什麼是 MBON01？" if not is_en else "What is MBON01?", key="pop_qq_2", use_container_width=True):
                quick_q = "什麼是 MBON01 趨向輸出神經元？" if not is_en else "What is the MBON01 approach output neuron?"
        with q_col2:
            if st.button("50c 票價影響" if not is_en else "50c Fare Impact", key="pop_qq_3", use_container_width=True):
                quick_q = "50 Cent 單程票價如何改變通勤選擇？" if not is_en else "How does the 50c fare affect commute choices?"
            if st.button("2032 奧運願景" if not is_en else "2032 Olympics", key="pop_qq_4", use_container_width=True):
                quick_q = "2032 奧運完工後布里斯本交通會發生什麼？" if not is_en else "What will happen in Brisbane 2032 Olympics?"

        # Chat History Container (inside popover)
        st.markdown("---")
        hist_box = st.container(height=180)
        with hist_box:
            if not st.session_state.fly_ai_history:
                st.caption(
                    "Hello! Ask any question about the data or models." if is_en 
                    else "您好！點選上方快捷按鈕或在下方輸入，隨時提問！"
                )
            for msg in st.session_state.fly_ai_history:
                if msg["role"] == "user":
                    with st.chat_message("user"):
                        st.write(msg["content"])
                else:
                    target_img = THUMB_AVATAR_PATH if os.path.exists(THUMB_AVATAR_PATH) else ORIG_AVATAR_PATH
                    with st.chat_message("assistant", avatar=target_img if os.path.exists(target_img) else None):
                        st.markdown(msg["content"])

        # Input Form inside popover (NO bottom bar across main screen!)
        with st.form("fly_ai_popover_form", clear_on_submit=True):
            user_text = st.text_input(
                "Ask a question:" if is_en else "輸入問題：",
                key="fly_ai_input_text",
                placeholder="Ask about this page..." if is_en else "想問什麼嗎？問我吧！",
                label_visibility="collapsed"
            )
            c_sub1, c_sub2 = st.columns([3, 1])
            with c_sub1:
                submitted = st.form_submit_button("Ask" if is_en else "送出提問", use_container_width=True)
            with c_sub2:
                cleared = st.form_submit_button("Clear" if is_en else "清除", use_container_width=True, help="Clear / 清除")

        if cleared:
            st.session_state.fly_ai_history = []
            st.rerun()

        to_run = quick_q or (user_text if submitted and user_text.strip() else None)
        if to_run:
            st.session_state.fly_ai_history.append({"role": "user", "content": to_run})
            with st.spinner("Thinking..." if is_en else "果蠅工程師思考中..."):
                ans = generate_ai_response(to_run, is_en, is_eli5, context_dict)
                st.session_state.fly_ai_history.append({"role": "assistant", "content": ans})
            st.rerun()
