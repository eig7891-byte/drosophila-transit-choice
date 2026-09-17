"""
Drosophila-Inspired Commute Decision Engine
------------------------------------------
Implements Kenyon Cells, PAM/PPL1 microcircuits, MBON integration,
and Central Complex (CX) action selection.
"""
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Any

from .neuromodulators import InternalNeuromodulatorState
from .calibration import BrainWeights, CALIBRATED_BRAIN_WEIGHTS

@dataclass
class CommuteOption:
    name: str                   # 'Car', 'Transit_50c', 'Bicycle'
    travel_time_min: float      # e.g., 30.0, 90.0, 65.0
    monetary_cost_aud: float    # e.g., 28.0 (parking+fuel), 1.0 (50c fare), 0.0
    physical_effort: float      # 0.0 (passive) to 1.0 (heavy exertion)
    departure_time_hr: float    # e.g., 8.5 (8:30am), 7.5 (7:30am)
    comfort_index: float        # 0.0 (sweaty/crowded) to 1.0 (private AC car)

class DrosophilaCommuteBrain:
    def __init__(self, target_arrival_hr: float = 9.0, weights: BrainWeights = None):
        self.target_arrival_hr = target_arrival_hr
        self.weights = weights if weights is not None else CALIBRATED_BRAIN_WEIGHTS

    def evaluate_mode(
        self,
        option: CommuteOption,
        state: InternalNeuromodulatorState,
        weather_heat_index: float = 0.2,
        transit_productivity: float = 0.6
    ) -> Dict[str, Any]:
        baseline_car_cost = 28.0
        money_saved = max(0.0, baseline_car_cost - option.monetary_cost_aud)

        # PAM Cluster (Reward)
        pam_money = (money_saved * 1.2) * (0.5 + 3.5 * state.npf_hunger)
        time_saved = max(0.0, 90.0 - option.travel_time_min)
        pam_speed = (time_saved * 0.45) * (1.0 + 2.2 * (1.0 - state.npf_hunger))
        pam_health = (option.physical_effort * 25.0) * (1.0 + 3.0 * state.octopamine_vigor)
        pam_comfort = (option.comfort_index * 22.0) * (1.0 + 1.5 * (1.0 - state.npf_hunger))
        sleep_comfort = max(0.0, option.departure_time_hr - 7.0) * 12.0
        pam_sleep = sleep_comfort * (1.0 + 2.5 * state.pdf_sleep_debt)
        pam_utility = (transit_productivity * 18.0) if option.name.startswith('Transit') else 0.0

        total_pam = (
            self.weights.w_pam_money * pam_money +
            self.weights.w_pam_speed * pam_speed +
            self.weights.w_pam_health * pam_health +
            self.weights.w_pam_comfort * pam_comfort +
            self.weights.w_pam_sleep * pam_sleep +
            self.weights.w_pam_utility * pam_utility
        )

        # PPL1 Cluster (Aversive Punishment)
        ppl1_cost = option.monetary_cost_aud * (0.20 + 2.2 * state.npf_hunger) * 0.70
        effective_delay = option.travel_time_min / (1.0 + 1.8 * state.serotonin_patience)
        ppl1_delay = effective_delay * 0.40
        duration_factor = (option.travel_time_min / 30.0) ** self.weights.fatigue_exponent
        effort_burden = option.physical_effort * duration_factor * (1.0 + 2.5 * weather_heat_index)
        ppl1_fatigue = (effort_burden / (1.0 + 2.5 * state.octopamine_vigor)) * 26.0
        wake_up_deficit = max(0.0, 8.5 - option.departure_time_hr)
        ppl1_early_wake = (wake_up_deficit ** 1.3) * (1.0 + 3.2 * state.pdf_sleep_debt) * 10.0

        total_ppl1 = (
            self.weights.w_ppl1_cost * ppl1_cost +
            self.weights.w_ppl1_delay * ppl1_delay +
            self.weights.w_ppl1_fatigue * ppl1_fatigue +
            self.weights.w_ppl1_early_wake * ppl1_early_wake
        )

        # MBON Integration
        mbon_approach = float(np.tanh(total_pam / 25.0))
        mbon_avoidance = float(np.tanh(total_ppl1 / 25.0))
        net_valence = mbon_approach - mbon_avoidance
        firing_rate_hz = float(np.clip(25.0 + 40.0 * net_valence, 5.0, 90.0))

        return {
            'option_name': option.name,
            'pam_reward_total': total_pam,
            'ppl1_cost_total': total_ppl1,
            'pam_components': {
                'money_saved': pam_money,
                'speed_time_saved': pam_speed,
                'health_fitness': pam_health,
                'comfort': pam_comfort,
                'sleep_rest': pam_sleep,
                'transit_productivity': pam_utility
            },
            'ppl1_components': {
                'out_of_pocket_cost': ppl1_cost,
                'time_delay': ppl1_delay,
                'physical_fatigue': ppl1_fatigue,
                'early_wake_deficit': ppl1_early_wake
            },
            'mbon_approach': mbon_approach,
            'mbon_avoidance': mbon_avoidance,
            'net_valence': net_valence,
            'firing_rate_hz': firing_rate_hz
        }

    def decide_commute(
        self,
        options: List[CommuteOption],
        state: InternalNeuromodulatorState,
        weather_heat_index: float = 0.2,
        transit_productivity: float = 0.6,
        temperature_softmax: float = 0.35,
        stochastic_sample: bool = False,
        rng: np.random.Generator = None
    ) -> Dict[str, Any]:
        evaluations = [
            self.evaluate_mode(opt, state, weather_heat_index, transit_productivity)
            for opt in options
        ]
        valences = np.array([e['net_valence'] for e in evaluations])
        exp_vals = np.exp((valences - np.max(valences)) / temperature_softmax)
        probabilities = exp_vals / np.sum(exp_vals)

        if stochastic_sample and rng is not None:
            chosen_idx = int(rng.choice(len(options), p=probabilities))
        else:
            chosen_idx = int(np.argmax(probabilities))

        chosen_option = options[chosen_idx]
        return {
            'chosen_mode': chosen_option.name,
            'chosen_option': chosen_option,
            'probabilities': {opt.name: float(p) for opt, p in zip(options, probabilities)},
            'evaluations': evaluations,
            'state_snapshot': state
        }
