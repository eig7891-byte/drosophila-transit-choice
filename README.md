# 🧠 Drosophila Connectome Transit Choice Model

An Agent-Based Neuromorphic Transit Choice Simulation for South East Queensland (Translink 50-Cent Fare), combining real Janelia FlyEM connectome circuit architecture with empirical travel data.

---

## 🌟 Overview

Traditional transportation choice models (e.g. Logit / Four-Step Models) assume perfect human utility rationality and struggle to explain non-linear tipping points—such as why an 89% public transit fare reduction (Queensland 50-Cent initiative) only reduces car reliance by 2.8% in outer suburbs.

This project introduces a **bio-inspired multi-agent transit choice architecture** adapted from the *Drosophila melanogaster* connectome:
* **Kenyon Cells & Sparse Coding**: Multimodal sensory representation of route characteristics (cost, in-vehicle delay, headways, and active walking fatigue under subtropical heat).
* **MBON-DAN Dual-Valence Circuit**: Dopaminergic reward (PAM money/speed neurons) and punishment (PPL1 cost/delay/fatigue neurons) arbitration.
* **Neuromodulatory Gating**: Octopamine (locomotor vigor), Serotonin (delay tolerance), Neuropeptide F (budget urgency), and PDF clock neurons (morning circadian sleep debt).
* **Empirical Inverse Calibration (MLE/MAP)**: Fitted via SciPy `L-BFGS-B` against 24.77 million Translink Go Card transactions (reducing objective loss by 72.5%, RMSE down to 1.99%).

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
pip install -r requirements.txt
```

### 2. Run the Interactive Streamlit Dashboard
```bash
streamlit run app.py
```
*(Or run directly: `streamlit run app_drosophila_transit.py`)*

### 3. Run Automated Unit Tests
```bash
python test_drosophila_engine.py
```

---

## 🔬 Project Structure

```text
├── app_drosophila_transit.py         # Main interactive Streamlit dashboard (8 Tabs, Bilingual)
├── app.py                            # Streamlit entry point wrapper
├── drosophila_brain_engine.py        # Core Kenyon Cell -> MBON / DAN neural choice engine
├── drosophila_visualizer.py          # 3D interactive connectome morphology renderer
├── brisbane_transit_simulator.py     # Corridor data and Monte Carlo agent population engine
├── test_drosophila_engine.py         # Comprehensive unit testing suite (6 test cases)
├── calibrated_brain_parameters.json  # Calibrated synaptic weights and optimization metadata
├── assets/                           # Interactive HTML canvas, avatars, and visual media
├── data/
│   ├── connectome/                   # Real Janelia FlyEM 3D morphology nodes (MBON01, MBON11, PPL101)
│   └── translink/                    # Empirical corridor targets from Queensland Open Data
├── pt-performance-accessibility_q2_2025_26.xlsx # Official Translink patronage quarterly report
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

---

## 📊 Empirical Data Sources

* **Queensland Government Open Data Portal**: Translink Go Card journey transactions (July 2024 baseline vs. August 2024 50-cent onset).
* **Translink Division (TMR)**: Quarterly Public Transport Performance & Customer Experience Report (Q2 2025-26).
* **Janelia Research Campus / FlyWire**: Whole-brain connectome wiring diagram (*Drosophila melanogaster*).
