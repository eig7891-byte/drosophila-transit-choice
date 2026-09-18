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
    /* Clean horizontal scrollable tab bar with high-contrast arrow navigation */
    div[data-testid="stTabs"] {
        width: 100% !important;
    }
    div[data-baseweb="tab-list"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        white-space: nowrap !important;
        width: 100% !important;
        gap: 8px !important;
        border-bottom: 2px solid #1e293b !important;
        padding-bottom: 6px !important;
        margin-bottom: 16px !important;
    }
    div[data-baseweb="tab-highlight"],
    div[data-baseweb="tab-border"] {
        display: none !important;
    }
    /* Tab Buttons - Default Unselected State */
    button[data-testid="stTab"],
    [data-testid="stTab"],
    button[data-baseweb="tab"],
    div[data-baseweb="tab"] {
        white-space: nowrap !important;
        padding: 8px 16px !important;
        border-radius: 8px 8px 0 0 !important;
        background-color: #131d2e !important;
        border: 1px solid #1e3a5f !important;
        border-bottom: 2px solid #1e3a5f !important;
        margin-bottom: 0px !important;
        font-weight: 600 !important;
        font-size: 0.90rem !important;
        flex: 0 0 auto !important;
        text-align: center !important;
        justify-content: center !important;
        color: #94a3b8 !important;
        cursor: pointer !important;
        transition: all 0.15s ease-in-out !important;
    }
    button[data-testid="stTab"] *,
    [data-testid="stTab"] *,
    button[data-baseweb="tab"] *,
    div[data-baseweb="tab"] * {
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }
    /* Tab Buttons - Hover State */
    button[data-testid="stTab"]:hover,
    [data-testid="stTab"]:hover,
    button[data-baseweb="tab"]:hover,
    div[data-baseweb="tab"]:hover {
        border-color: #38bdf8 !important;
        background-color: #1e293b !important;
        color: #38bdf8 !important;
    }
    button[data-testid="stTab"]:hover *,
    [data-testid="stTab"]:hover *,
    button[data-baseweb="tab"]:hover *,
    div[data-baseweb="tab"]:hover * {
        color: #38bdf8 !important;
    }
    /* Tab Buttons - Active / Selected State */
    button[data-testid="stTab"][aria-selected="true"],
    [data-testid="stTab"][aria-selected="true"],
    button[data-baseweb="tab"][aria-selected="true"],
    div[data-baseweb="tab"][aria-selected="true"] {
        background-color: #0b291e !important;
        border-color: #00e676 !important;
        border-bottom: 3px solid #00e676 !important;
        color: #00e676 !important;
        box-shadow: 0 -2px 10px rgba(0, 230, 118, 0.35) !important;
    }
    button[data-testid="stTab"][aria-selected="true"] *,
    [data-testid="stTab"][aria-selected="true"] *,
    button[data-baseweb="tab"][aria-selected="true"] *,
    div[data-baseweb="tab"][aria-selected="true"] * {
        color: #00e676 !important;
        font-weight: 700 !important;
    }
    /* Tab Navigation Arrows */
    button[data-testid="stTabsScrollLeft"],
    button[data-testid="stTabsScrollRight"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background-color: #111d33 !important;
        border: 1.5px solid #00e676 !important;
        border-radius: 6px !important;
        color: #00e676 !important;
        opacity: 1 !important;
        visibility: visible !important;
        z-index: 100 !important;
        cursor: pointer !important;
        box-shadow: 0 0 10px rgba(0, 230, 118, 0.35) !important;
        width: 32px !important;
        height: 36px !important;
        padding: 0 !important;
    }
    button[data-testid="stTabsScrollLeft"] svg,
    button[data-testid="stTabsScrollRight"] svg {
        color: #00e676 !important;
        fill: #00e676 !important;
        width: 22px !important;
        height: 22px !important;
    }
    button[data-testid="stTabsScrollLeft"]:hover,
    button[data-testid="stTabsScrollRight"]:hover {
        background-color: #162a45 !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 14px rgba(56, 189, 248, 0.5) !important;
    }
    button[data-testid="stTabsScrollLeft"]:hover svg,
    button[data-testid="stTabsScrollRight"]:hover svg {
        color: #38bdf8 !important;
        fill: #38bdf8 !important;
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
        background-color: #0f172a !important;
        border-radius: 8px;
        overflow: hidden;
    }
    .benchmark-table th, .benchmark-table td {
        border: 1px solid #1e293b !important;
        padding: 10px 14px;
        text-align: left;
    }
    .benchmark-table th {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        font-weight: 700;
        font-size: 0.94rem;
    }
    .benchmark-table td {
        background-color: #0f172a !important;
        color: #f1f5f9 !important;
        font-size: 0.92rem;
    }
    .benchmark-table tr:nth-child(even) td {
        background-color: #131e33 !important;
    }
    .benchmark-table tr:hover td {
        background-color: #1e293b !important;
    }
    code, span.code-badge {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        border: 1px solid #334155 !important;
        border-radius: 4px !important;
        padding: 2px 6px !important;
        font-family: monospace !important;
        font-size: 0.85rem !important;
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
    /* Sidebar Dark Theme & Container Backgrounds */
    header[data-testid="stHeader"] {
        background-color: #0e131f !important;
    }
    section[data-testid="stSidebar"],
    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"],
    [data-testid="stSidebarHeader"] {
        background-color: #0b111e !important;
        border-right: 1px solid #1e293b !important;
        color: #f1f5f9 !important;
    }
    [data-testid="stSidebar"] h1 {
        color: #00e676 !important;
        font-weight: 700 !important;
        font-size: 1.45rem !important;
        margin-bottom: 0.8rem !important;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #38bdf8 !important;
        font-weight: 700 !important;
        font-size: 1.10rem !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] span {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 0.90rem !important;
    }
    [data-testid="stSidebar"] p {
        color: #cbd5e1 !important;
        font-size: 0.90rem !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #1e293b !important;
        margin: 1rem 0 !important;
    }

    /* Sidebar Selectbox */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #162032 !important;
        border: 1.5px solid #334155 !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="select"] > div:hover {
        border-color: #38bdf8 !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: #f8fafc !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="select"] svg {
        fill: #38bdf8 !important;
        color: #38bdf8 !important;
    }
    ul[role="listbox"], div[data-baseweb="menu"] {
        background-color: #162032 !important;
        border: 1px solid #1e3a5f !important;
    }
    li[role="option"] {
        color: #e2e8f0 !important;
    }
    li[role="option"][aria-selected="true"] {
        background-color: #0b291e !important;
        color: #00e676 !important;
        font-weight: 700 !important;
    }

    /* Sidebar Sliders */
    [data-testid="stSidebar"] [data-testid="stSliderThumbValue"] {
        color: #00e676 !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] [data-testid="stSliderTickBar"] div {
        color: #94a3b8 !important;
    }

    /* Sidebar Radio and Checkbox */
    [data-testid="stSidebar"] [data-testid="stRadio"] label p,
    [data-testid="stSidebar"] [data-testid="stRadio"] label span,
    .stCheckbox p, .stRadio p {
        color: #e2e8f0 !important;
        font-size: 0.92rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover p {
        color: #00e676 !important;
    }

    /* Sidebar Collapse & Expand Controls */
    [data-testid="stSidebarCollapseButton"] button {
        color: #00e676 !important;
    }
    [data-testid="stSidebarCollapseButton"] button svg {
        color: #00e676 !important;
        fill: #00e676 !important;
    }
    [data-testid="stSidebarCollapseButton"] button:hover {
        color: #38bdf8 !important;
    }
    [data-testid="stSidebarCollapseButton"] button:hover svg {
        color: #38bdf8 !important;
        fill: #38bdf8 !important;
    }

    /* Sidebar Collapsed Control with "Option 設定" Label */
    button[data-testid="stExpandSidebarButton"],
    [data-testid="stExpandSidebarButton"],
    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="collapsedControl"] button {
        display: inline-flex !important;
        align-items: center !important;
        background-color: #111d33 !important;
        border: 1.5px solid #00e676 !important;
        border-radius: 8px !important;
        padding: 6px 14px !important;
        width: auto !important;
        height: auto !important;
        min-height: 38px !important;
        overflow: visible !important;
        gap: 6px !important;
        cursor: pointer !important;
        box-shadow: 0 0 12px rgba(0, 230, 118, 0.35) !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999999 !important;
    }
    button[data-testid="stExpandSidebarButton"] svg,
    [data-testid="stExpandSidebarButton"] svg,
    [data-testid="stSidebarCollapsedControl"] button svg,
    [data-testid="collapsedControl"] button svg {
        color: #00e676 !important;
        fill: #00e676 !important;
        width: 20px !important;
        height: 20px !important;
    }
    button[data-testid="stExpandSidebarButton"]::after,
    [data-testid="stExpandSidebarButton"]::after,
    [data-testid="stSidebarCollapsedControl"] button::after,
    [data-testid="collapsedControl"] button::after {
        content: "Option 設定" !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        color: #00e676 !important;
        white-space: nowrap !important;
        display: inline-block !important;
        margin-left: 6px !important;
    }
    button[data-testid="stExpandSidebarButton"]:hover,
    [data-testid="stExpandSidebarButton"]:hover,
    [data-testid="stSidebarCollapsedControl"] button:hover,
    [data-testid="collapsedControl"] button:hover {
        background-color: #162a45 !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.5) !important;
    }
    button[data-testid="stExpandSidebarButton"]:hover::after,
    [data-testid="stExpandSidebarButton"]:hover::after,
    [data-testid="stSidebarCollapsedControl"] button:hover::after,
    [data-testid="collapsedControl"] button:hover::after {
        color: #38bdf8 !important;
    }
    button[data-testid="stExpandSidebarButton"]:hover svg,
    [data-testid="stExpandSidebarButton"]:hover svg,
    [data-testid="stSidebarCollapsedControl"] button:hover svg,
    [data-testid="collapsedControl"] button:hover svg {
        color: #38bdf8 !important;
        fill: #38bdf8 !important;
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
