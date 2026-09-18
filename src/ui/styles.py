"""
Custom UI styles and CSS injection for Drosophila Transit Choice Dashboard.
"""
import streamlit as st

CUSTOM_CSS = """
<style>
    .stApp {
        background-color: #0e131f !important;
        color: #f1f5f9 !important;
    }
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00e676;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #cbd5e1;
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
    /* Multi-column / clean flex layout for tab bar, eliminating scroll arrows */
    button[data-testid="stTabScrollLeft"],
    button[data-testid="stTabScrollRight"] {
        display: none !important;
    }
    div[data-testid="stTabs"] > div:first-child {
        overflow: visible !important;
    }
    div[data-baseweb="tab-list"] {
        display: flex !important;
        flex-wrap: wrap !important;
        width: 100% !important;
        overflow: visible !important;
        gap: 6px !important;
        border-bottom: 2px solid #1e293b !important;
        padding-bottom: 8px !important;
        margin-bottom: 14px !important;
    }
    div[data-baseweb="tab-highlight"],
    div[data-baseweb="tab-border"] {
        display: none !important;
    }
    button[data-baseweb="tab"] {
        white-space: nowrap !important;
        padding: 9px 14px !important;
        border-radius: 8px !important;
        background-color: #1a2234 !important;
        border: 1px solid #334155 !important;
        margin-bottom: 4px !important;
        font-weight: 600 !important;
        font-size: 0.90rem !important;
        flex: 1 1 auto !important;
        min-width: 115px !important;
        text-align: center !important;
        justify-content: center !important;
        color: #f8fafc !important;
        transition: all 0.15s ease-in-out !important;
    }
    button[data-baseweb="tab"] * {
        color: #f8fafc !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"]:hover {
        border-color: #38bdf8 !important;
        background-color: #243049 !important;
        color: #38bdf8 !important;
    }
    button[data-baseweb="tab"]:hover * {
        color: #38bdf8 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #0b291e !important;
        border-color: #00e676 !important;
        color: #00e676 !important;
        box-shadow: 0 0 10px rgba(0, 230, 118, 0.3) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] * {
        color: #00e676 !important;
        font-weight: 700 !important;
    }
    .phenomenon-card {
        background-color: #131926;
        border: 1px solid #1e293b;
        border-left: 5px solid #38bdf8;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 20px;
    }
    .phenomenon-card p, .metric-box p, .character-card p {
        color: #e2e8f0 !important;
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
    .benchmark-table td {
        color: #f1f5f9 !important;
    }

    /* Global High Contrast Enhancements */
    label, [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] span {
        color: #f8fafc !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricValue"] * {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    .stCaption, [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * {
        color: #cbd5e1 !important;
        font-size: 0.90rem !important;
    }
    .streamlit-expanderHeader, [data-testid="stExpander"] details summary * {
        color: #f8fafc !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #f8fafc !important;
    }
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] span {
        color: #f8fafc !important;
    }
    .stCheckbox p, .stRadio p {
        color: #f1f5f9 !important;
    }

    /* Sidebar Collapsed Control with "Option 設定" Label */
    [data-testid="stSidebarCollapsedControl"] {
        background: #131d2e !important;
        border: 1px solid #1e3a5f !important;
        border-radius: 6px !important;
        padding: 2px 8px !important;
        display: inline-flex !important;
        align-items: center !important;
        width: auto !important;
        overflow: visible !important;
    }
    [data-testid="stSidebarCollapsedControl"] button {
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        color: #f1f5f9 !important;
        width: auto !important;
        overflow: visible !important;
    }
    [data-testid="stSidebarCollapsedControl"] button::after {
        content: " Option 設定";
        font-size: 0.88rem;
        font-weight: 600;
        color: #00e676;
        white-space: nowrap;
        margin-left: 4px;
    }
    /* Streamlit Alert Boxes (st.info, st.warning, st.success) High Contrast Dark Theme */
    div[data-testid="stAlert"], .stAlert {
        background: #0f172a !important;
        border: 1px solid #1e3a8a !important;
        border-left: 5px solid #38bdf8 !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
        padding: 14px 18px !important;
    }
    div[data-testid="stAlert"] *, .stAlert * {
        color: #f8fafc !important;
    }
    div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p,
    .stAlert [data-testid="stMarkdownContainer"] p {
        color: #f1f5f9 !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }
    div[data-testid="stAlert"] svg, .stAlert svg {
        fill: #38bdf8 !important;
        color: #38bdf8 !important;
    }

    /* Streamlit Static Tables (st.table) - Multi-Decadal Parameter Matrix & Others */
    div[data-testid="stTable"],
    div[data-testid="stTable"] table,
    .stTable,
    .stTable table,
    table {
        color: #f8fafc !important;
        background-color: #0f172a !important;
        border-collapse: collapse !important;
        width: 100% !important;
    }
    div[data-testid="stTable"] th, .stTable th, table th {
        color: #38bdf8 !important;
        background-color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border: 1px solid #334155 !important;
        padding: 12px 14px !important;
        text-align: left !important;
    }
    div[data-testid="stTable"] td, .stTable td, table td {
        color: #f8fafc !important;
        background-color: #0f172a !important;
        font-size: 0.92rem !important;
        border: 1px solid #1e293b !important;
        padding: 12px 14px !important;
    }
    div[data-testid="stTable"] tr:nth-child(even) td, .stTable tr:nth-child(even) td, table tr:nth-child(even) td {
        background-color: #131e33 !important;
    }
    div[data-testid="stTable"] tr:hover td, .stTable tr:hover td, table tr:hover td {
        background-color: #1e293b !important;
    }
    div[data-testid="stTable"] *, .stTable *, table * {
        color: #f8fafc !important;
    }

    /* Streamlit DataFrame Container High Contrast */
    [data-testid="stDataFrame"] {
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    /* Plotly Chart Legends and Text High Contrast Overrides */
    .js-plotly-plot .plotly .legendtext {
        fill: #f8fafc !important;
        color: #f8fafc !important;
        font-size: 11px !important;
    }
    .js-plotly-plot .plotly .xtitle, .js-plotly-plot .plotly .ytitle {
        fill: #f8fafc !important;
        color: #f8fafc !important;
        font-weight: 600 !important;
    }
    .js-plotly-plot .plotly .xtick text, .js-plotly-plot .plotly .ytick text {
        fill: #cbd5e1 !important;
        color: #cbd5e1 !important;
    }
    .js-plotly-plot .plotly .gtitle {
        fill: #ffffff !important;
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    .js-plotly-plot .plotly .cbtitle {
        fill: #f8fafc !important;
        color: #f8fafc !important;
    }
    .js-plotly-plot .plotly .cbtick text {
        fill: #cbd5e1 !important;
        color: #cbd5e1 !important;
    }
</style>
"""

def inject_custom_styles():
    """Inject custom CSS rules into Streamlit head."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
