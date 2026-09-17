"""
Custom UI styles and CSS injection for Drosophila Transit Choice Dashboard.
"""
import streamlit as st

CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00e676;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 1.2rem;
    }
    .intro-banner {
        background: linear-gradient(135deg, #131d2e 0%, #0d131f 100%);
        border: 1px solid #1e3a5f;
        border-left: 5px solid #00e676;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: #1e222d;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #00e676;
        margin-bottom: 1rem;
    }
    .winner-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #38bdf8;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        margin-bottom: 1.2rem;
    }
    .character-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        margin-bottom: 10px;
        transition: transform 0.2s;
    }
    .character-card:hover {
        border-color: #00e676;
        transform: translateY(-2px);
    }
    .character-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-top: 8px;
        margin-bottom: 4px;
    }
    /* Multi-row wrapping for tab bar to eliminate tiny arrows */
    div[data-baseweb="tab-list"] {
        flex-wrap: wrap !important;
        gap: 6px !important;
        border-bottom: 2px solid #1e293b !important;
        padding-bottom: 8px !important;
        margin-bottom: 12px !important;
    }
    button[data-baseweb="tab"] {
        white-space: normal !important;
        padding: 8px 16px !important;
        border-radius: 8px !important;
        background-color: #131926 !important;
        border: 1px solid #1e293b !important;
        margin-bottom: 4px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    button[data-baseweb="tab"]:hover {
        border-color: #38bdf8 !important;
        color: #38bdf8 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #1e293b !important;
        border-color: #00e676 !important;
        color: #00e676 !important;
    }
    .phenomenon-card {
        background-color: #131926;
        border: 1px solid #1e293b;
        border-left: 5px solid #38bdf8;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 20px;
    }
    .benchmark-table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        font-size: 0.95rem;
    }
    .benchmark-table th, .benchmark-table td {
        border: 1px solid #334155;
        padding: 10px 12px;
        text-align: left;
    }
    .benchmark-table th {
        background-color: #1e293b;
        color: #38bdf8;
        font-weight: 700;
    }
</style>
"""

def inject_custom_styles():
    """Inject custom CSS rules into Streamlit head."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
