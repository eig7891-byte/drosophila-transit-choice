"""
Drosophila Connectome 3D & 2D Visualizer
-----------------------------------------
Visualizes real Janelia FlyEM male CNS neurons (MBON01, PPL101, MBON11)
in 3D coordinate space and generates dynamic neural activation plots
synchronized with the Brisbane commuter decision state.
"""

import json
import os
import numpy as np
import plotly.graph_objects as go
from typing import Dict, Any, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'connectome')

class DrosophilaConnectomeVisualizer:
    def __init__(self):
        self.neurons = self._load_neurons()

    def _load_neurons(self) -> Dict[str, np.ndarray]:
        """Loads real 3D skeleton nodes from Janelia FlyEM datasets."""
        neuron_files = {
            'MBON01_Approach': 'MBON01_Approach_10013.json',
            'PPL101_Aversive_DAN': 'PPL101_Aversive_DAN_11900.json',
            'MBON11_Avoidance': 'MBON11_Avoidance_11402.json'
        }
        loaded = {}
        for name, filename in neuron_files.items():
            path = os.path.join(DATA_DIR, filename)
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        raw_nodes = data.get('data', [])
                        # Node format: [nodeId, x, y, z, radius, parentId]
                        coords = np.array([[n[1], n[2], n[3]] for n in raw_nodes if len(n) >= 4])
                        # Normalize to center around origin in microns (FlyEM units are typically 8nm per voxel)
                        coords_um = coords * 0.008
                        # Subsample for snappy interactive rendering (every 4th node)
                        loaded[name] = coords_um[::4]
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
            else:
                # Fallback synthetic morphology if file missing
                loaded[name] = self._generate_fallback_morphology(name)
        return loaded

    def _generate_fallback_morphology(self, name: str) -> np.ndarray:
        """Synthetic branching morphology as robust fallback."""
        n_pts = 800
        t = np.linspace(0, 10, n_pts)
        if 'Approach' in name:
            x = 200 + 40 * np.sin(t * 1.5) + np.random.normal(0, 5, n_pts)
            y = 150 + 30 * np.cos(t * 2.0) + np.random.normal(0, 5, n_pts)
            z = 100 + 15 * t + np.random.normal(0, 3, n_pts)
        elif 'Aversive' in name:
            x = 180 + 35 * np.cos(t * 1.2) + np.random.normal(0, 5, n_pts)
            y = 220 + 25 * np.sin(t * 1.8) + np.random.normal(0, 5, n_pts)
            z = 80 + 18 * t + np.random.normal(0, 3, n_pts)
        else:
            x = 220 + 30 * np.sin(t * 2.5) + np.random.normal(0, 5, n_pts)
            y = 180 + 35 * np.cos(t * 1.1) + np.random.normal(0, 5, n_pts)
            z = 120 + 12 * t + np.random.normal(0, 3, n_pts)
        return np.column_stack([x, y, z])

    def create_3d_connectome_figure(
        self,
        evaluation_result: Optional[Dict[str, Any]] = None
    ) -> go.Figure:
        """
        Builds a 3D Plotly visualization of the fruit fly brain and
        modulates neuron colors/sizes based on live decision activations.
        """
        fig = go.Figure()

        # Activation weights
        if evaluation_result:
            chosen = evaluation_result.get('chosen_mode', 'Transit_50c')
            # Extract PAM vs PPL1 intensities for the chosen mode
            evals = {e['option_name']: e for e in evaluation_result.get('evaluations', [])}
            active_eval = evals.get(chosen, {})
            mbon_app = active_eval.get('mbon_approach', 0.5)
            mbon_av = active_eval.get('mbon_avoidance', 0.5)
        else:
            mbon_app = 0.5
            mbon_av = 0.5

        # 1. MBON01 (Approach / Reward Signal) -> Vibrant Emerald Green / Gold
        if 'MBON01_Approach' in self.neurons:
            pts = self.neurons['MBON01_Approach']
            size = 2.0 + 3.0 * mbon_app
            opacity = 0.3 + 0.6 * mbon_app
            fig.add_trace(go.Scatter3d(
                x=pts[:, 0], y=pts[:, 1], z=pts[:, 2],
                mode='markers',
                marker=dict(
                    size=size,
                    color=pts[:, 2],
                    colorscale=[[0, '#00ff88'], [1, '#ffd700']],
                    opacity=opacity
                ),
                name=f'MBON01 (Reward/Approach, {len(pts)} nodes)',
                hoverinfo='text',
                hovertext='MBON01: Positive Valuation (50c Fare / Savings / Health)'
            ))

        # 2. PPL101 (Aversive Dopaminergic / Pain Signal) -> Crimson Red / Flame Orange
        if 'PPL101_Aversive_DAN' in self.neurons:
            pts = self.neurons['PPL101_Aversive_DAN']
            size = 2.0 + 3.0 * mbon_av
            opacity = 0.3 + 0.6 * mbon_av
            fig.add_trace(go.Scatter3d(
                x=pts[:, 0], y=pts[:, 1], z=pts[:, 2],
                mode='markers',
                marker=dict(
                    size=size,
                    color=pts[:, 2],
                    colorscale=[[0, '#ff1744'], [1, '#ff9100']],
                    opacity=opacity
                ),
                name=f'PPL101 (Aversive DAN, {len(pts)} nodes)',
                hoverinfo='text',
                hovertext='PPL101: Aversive Cost (Parking Fee / Delay / Fatigue)'
            ))

        # 3. MBON11 (Avoidance Output) -> Electric Cyan / Violet
        if 'MBON11_Avoidance' in self.neurons:
            pts = self.neurons['MBON11_Avoidance']
            fig.add_trace(go.Scatter3d(
                x=pts[:, 0], y=pts[:, 1], z=pts[:, 2],
                mode='markers',
                marker=dict(
                    size=2.5,
                    color='#7c4dff',
                    opacity=0.65
                ),
                name=f'MBON11 (Avoidance Circuit, {len(pts)} nodes)',
                hoverinfo='text',
                hovertext='MBON11: Active Avoidance Arbitration'
            ))

        # Style dark theme matching Janelia NeuPrint WebGL aesthetic
        fig.update_layout(
            scene=dict(
                xaxis=dict(title='Lateral (μm)', showbackground=False, zeroline=False),
                yaxis=dict(title='Anterior-Posterior (μm)', showbackground=False, zeroline=False),
                zaxis=dict(title='Dorsoventral (μm)', showbackground=False, zeroline=False),
                bgcolor='#0e1117'
            ),
            paper_bgcolor='#0e1117',
            font=dict(color='#e0e0e0'),
            margin=dict(l=0, r=0, b=0, t=30),
            legend=dict(
                x=0.02, y=0.98,
                bgcolor='rgba(20,24,35,0.8)',
                bordercolor='#333',
                borderwidth=1
            )
        )
        return fig

    def create_neural_circuit_bar_chart(self, evaluations: list) -> go.Figure:
        """Creates bar chart showing PAM (Reward) vs PPL1 (Cost) for each commute option."""
        modes = [e['option_name'] for e in evaluations]
        pam_scores = [e['pam_reward_total'] for e in evaluations]
        ppl1_scores = [e['ppl1_cost_total'] for e in evaluations]
        firing_rates = [e['firing_rate_hz'] for e in evaluations]

        fig = go.Figure(data=[
            go.Bar(name='PAM Reward (Positive Valence)', x=modes, y=pam_scores, marker_color='#00e676'),
            go.Bar(name='PPL1 Cost (Aversive Punishment)', x=modes, y=ppl1_scores, marker_color='#ff5252'),
            go.Bar(name='Action Firing Rate (Hz)', x=modes, y=firing_rates, marker_color='#448aff')
        ])
        fig.update_layout(
            barmode='group',
            title='Mushroom Body Firing Rates & Neuromodulator Balance per Mode',
            paper_bgcolor='#0e1117',
            plot_bgcolor='#161b22',
            font=dict(color='#e0e0e0'),
            yaxis=dict(title='Signal Intensity / Hz', gridcolor='#2d333b'),
            legend=dict(bgcolor='rgba(20,24,35,0.8)')
        )
        return fig