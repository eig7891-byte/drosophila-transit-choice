"""
Streamlit UI tab modules for Drosophila Transit Choice Dashboard.
"""
from .tab1_connectome import render_tab1_connectome
from .tab2_archetypes import render_tab2_archetypes
from .tab3_phenomena import render_tab3_phenomena
from .tab4_society_setup import render_tab4_society_setup
from .tab5_calibration import render_tab5_calibration
from .tab6_whitepaper import render_tab6_whitepaper
from .tab7_future import render_tab7_future
from .tab8_spatial_equity import render_tab8_spatial_equity

__all__ = [
    "render_tab1_connectome",
    "render_tab2_archetypes",
    "render_tab3_phenomena",
    "render_tab4_society_setup",
    "render_tab5_calibration",
    "render_tab6_whitepaper",
    "render_tab7_future",
    "render_tab8_spatial_equity"
]
