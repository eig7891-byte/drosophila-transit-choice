"""
Streamlit UI tab modules for Drosophila Transit Choice Dashboard.
Streamlined 3-Chapter Showcase:
1. Corridor Benchmark Showdown (4 Corridors)
2. Empirical Data Provenance & SciPy MLE Calibration Engine
3. Interactive Policy Sandbox & Macro Simulation
"""
from .tab1_showdown import render_tab1_showdown
from .tab2_calibration import render_tab2_calibration
from .tab3_sandbox import render_tab3_sandbox

# Previous & legacy imports for backward compatibility
from .tab1_connectome import render_tab1_connectome
from .tab2_grounding import render_tab2_grounding
from .tab3_calibration_tmr import render_tab3_calibration_tmr
from .tab4_core_corridors import render_tab4_core_corridors
from .tab5_validation_routes import render_tab5_validation_routes
from .tab6_conclusions import render_tab6_conclusions
from .tab7_database import render_tab7_database
from .tab2_archetypes import render_tab2_archetypes
from .tab3_phenomena import render_tab3_phenomena
from .tab4_society_setup import render_tab4_society_setup
from .tab5_calibration import render_tab5_calibration
from .tab6_whitepaper import render_tab6_whitepaper
from .tab7_future import render_tab7_future
from .tab8_spatial_equity import render_tab8_spatial_equity

__all__ = [
    # New Streamlined 3-Chapter Architecture
    "render_tab1_showdown",
    "render_tab2_calibration",
    "render_tab3_sandbox",
    # 7-Chapter Modules
    "render_tab1_connectome",
    "render_tab2_grounding",
    "render_tab3_calibration_tmr",
    "render_tab4_core_corridors",
    "render_tab5_validation_routes",
    "render_tab6_conclusions",
    "render_tab7_database",
    # Legacy Modules
    "render_tab2_archetypes",
    "render_tab3_phenomena",
    "render_tab4_society_setup",
    "render_tab5_calibration",
    "render_tab6_whitepaper",
    "render_tab7_future",
    "render_tab8_spatial_equity"
]
