# Drosophila Connectome Transit Choice Model

An Agent-Based Neuromorphic Transit Choice Simulation for South East Queensland (Translink 50-Cent Fare Policy), combining Janelia FlyEM connectome circuit architecture with empirical travel data.

---

## 1. Overview

Standard transportation choice models (such as multinomial logit formulations) assume human commuters act as rational economic agents with linear utility functions. These models often fail to capture non-linear behavioral shifts, such as why an 89% public transit fare reduction (Queensland 50-Cent initiative) leads to only a modest reduction in car dependency across outer suburban areas.

This project implements a **bio-inspired multi-agent transit choice architecture** adapted from the *Drosophila melanogaster* connectome:
* **Kenyon Cells & Sparse Coding**: Multimodal sensory representation of route characteristics (cost, in-vehicle delay, headways, and active walking fatigue under subtropical heat).
* **MBON-DAN Dual-Valence Circuit**: Dopaminergic reward (PAM money/speed neurons) and punishment (PPL1 cost/delay/fatigue neurons) arbitration.
* **Neuromodulatory Gating**: Octopamine (locomotor vigor), Serotonin (delay tolerance), Neuropeptide F (budget urgency), and PDF clock neurons (morning circadian sleep debt).
* **Empirical Inverse Calibration (MLE/MAP)**: Fitted via SciPy `L-BFGS-B` against 24.77 million Translink Go Card transactions and Q2 2025-26 quarterly report targets (reducing objective loss by 72.5%, RMSE down to 1.99%).

---

## 2. Quick Start

### 2.1 Installation
```bash
git clone https://github.com/eig7891-byte/drosophila-transit-choice.git
cd drosophila-transit-choice
pip install -r requirements.txt
```

### 2.2 Run the Interactive Streamlit Dashboard
```bash
streamlit run app.py
```
*(Or run via the backward-compatible wrapper: `streamlit run app_drosophila_transit.py`)*

### 2.3 Run Automated Unit Tests
```bash
pytest tests -v
```

### 2.4 Run Standalone MLE Parameter Calibration
```bash
python scripts/run_mle_calibration.py
```

---

## 3. Project Architecture

The codebase is organized as a modular Python package:

```text
drosophila-transit-choice/
├── app.py                             # Streamlit application entry point
├── app_drosophila_transit.py          # Backward-compatible entry point forwarding to app.py
├── src/
│   ├── core/                          # Neural arbitration engine & calibration state
│   │   ├── engine.py                  # DrosophilaCommuteBrain & CommuteOption
│   │   ├── neuromodulators.py         # InternalNeuromodulatorState (NPF, OA, Ser, PDF)
│   │   └── calibration.py             # BrainWeights, priors, and MLE parameter loader
│   ├── simulation/                    # Corridor & population agent-based modeling
│   │   ├── corridors.py               # Brisbane physical corridors & ABS demographic parameters
│   │   └── population.py              # BrisbaneTransitSimulator (10,000 synthetic commuters)
│   ├── visualization/                 # 3D interactive connectome renderers
│   │   └── connectome_3d.py           # DrosophilaConnectomeVisualizer
│   ├── ai/                            # Intelligent assistant popover widget
│   │   └── assistant.py               # Fly Engineer AI (Gemini Flash & native popover)
│   └── ui/                            # Decomposed presentation layer
│       ├── styles.py                  # Custom CSS styling rules
│       ├── sidebar.py                 # Sidebar parameter inputs and reactive state
│       └── tabs/                      # 8 modular tab modules (Tab 1 to Tab 8)
│           ├── tab1_connectome.py     # 3D connectome morphology & biological grounding
│           ├── tab2_archetypes.py     # HTML5 canvas arena & commuter archetypes
│           ├── tab3_phenomena.py      # Non-linear neural discrepancies & insights
│           ├── tab4_society_setup.py  # 10,000-commuter demographic & spatial setup
│           ├── tab5_calibration.py    # Policy scenarios & empirical calibration results
│           ├── tab6_whitepaper.py     # Transit policy & engineering white paper
│           ├── tab7_future.py         # Multi-decadal statutory master plan matrix
│           └── tab8_spatial_equity.py # Suburb-level modal split & spatial equity sandbox
├── scripts/
│   └── run_mle_calibration.py         # Standalone SciPy MLE inverse calibration pipeline
├── tests/                             # Comprehensive pytest test suite (20 tests)
│   ├── conftest.py                    # Pytest fixtures
│   ├── test_drosophila_engine.py      # Core neural engine tests
│   ├── test_corridor_simulation.py    # Spatial corridor & demographic tests
│   ├── test_calibration_pipeline.py   # Empirical calibration & target validation tests
│   ├── test_data_consistency.py       # Data integrity, corridor attributes & zero-emoji tests
│   └── test_ui_modules.py             # UI components, tabs, and visualizer tests
├── data/
│   ├── connectome/                    # Janelia FlyEM 3D morphology nodes (MBON01, MBON11, PPL101)
│   ├── empirical/                     # Translink Q2 report & empirical calibration targets
│   ├── metadata/                      # FlyWire connectome cell types & synaptic catalogs
│   └── parameters/                    # Calibrated brain weights and precomputed simulation data
├── assets/                            # Doomfly HTML5 interactive canvas and avatar media
├── reports/                           # Academic & technical synthesis reports
├── .gitattributes                     # Git line ending normalization & binary tracking
├── .gitignore                         # Ignore Python bytecode, virtualenv & test caches
├── CITATION.cff                       # Machine-readable academic citation metadata (Zenodo/GitHub)
├── LICENSE                            # MIT open-source license
├── requirements.txt                   # Project dependencies
└── README.md                          # Research overview and documentation
```

---

## 4. Empirical Data Sources & Provenance

* **Queensland Government Open Data Portal**: Translink Go Card journey transactions (July 2024 baseline vs. August 2024 50-cent onset).
* **Translink Division (TMR)**: Quarterly Public Transport Performance & Customer Experience Report (Q2 2025-26).
* **Australian Bureau of Statistics (ABS)**: 2021 Census QuickStats (SAL32626 & South East Queensland journey-to-work vehicle ownership statistics).
* **Janelia Research Campus / FlyWire**: Whole-brain connectome wiring diagram (*Drosophila melanogaster*, Nature 2024).
