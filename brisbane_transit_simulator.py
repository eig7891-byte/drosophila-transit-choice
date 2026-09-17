"""
Brisbane Transit Policy & Commuter Population Simulator
-------------------------------------------------------
Powered by the Drosophila-Inspired Commute Decision Engine.
Simulates 10,000 heterogeneous commuters across Brisbane corridors.
"""

import numpy as np
import pandas as pd
import json
from dataclasses import dataclass
from typing import Dict, List, Any
from drosophila_brain_engine import (
    DrosophilaCommuteBrain,
    CommuteOption,
    InternalNeuromodulatorState,
    BrainWeights
)

@dataclass
class CommuteCorridor:
    name: str
    distance_km: float
    car_travel_time_min: float
    transit_travel_time_min: float
    bike_travel_time_min: float
    car_parking_fuel_cost: float
    distance_to_transit_m: float = 400.0

BRISBANE_CORRIDORS = [
    CommuteCorridor("Springwood to Rochedale South (5.2km Local)", 5.24, 8.5, 20.0, 18.0, 12.0, 2200.0),
    CommuteCorridor("Springwood to UQ St Lucia (28.8km University)", 28.78, 38.0, 42.0, 85.0, 26.5, 2200.0),
    CommuteCorridor("Chermside to CBD (Northern)", 10.5, 30.0, 50.0, 45.0, 26.0, 800.0),
    CommuteCorridor("Indooroopilly to CBD (Western)", 7.2, 22.0, 35.0, 32.0, 24.0, 600.0),
    CommuteCorridor("Mt Gravatt to CBD (South-East)", 13.8, 35.0, 55.0, 58.0, 28.0, 1500.0),
    CommuteCorridor("Logan Central to CBD (Outer South)", 26.5, 45.0, 85.0, 110.0, 34.0, 1800.0),
    CommuteCorridor("Carindale to CBD (Eastern)", 11.0, 28.0, 48.0, 48.0, 25.0, 400.0)
]

class BrisbaneTransitSimulator:
    def __init__(self, seed: int = 42, weights: BrainWeights = None):
        self.brain = DrosophilaCommuteBrain(target_arrival_hr=9.0, weights=weights)
        self.rng = np.random.default_rng(seed)

    def generate_population(self, n_commuters: int = 10000) -> pd.DataFrame:
        archetypes = self.rng.choice(
            ['Student', 'CBD_Professional', 'Suburban_Worker', 'Fitness_Enthusiast'],
            size=n_commuters,
            p=[0.25, 0.40, 0.20, 0.15]
        )

        records = []
        for arch in archetypes:
            corridor = self.rng.choice(BRISBANE_CORRIDORS)
            # Real-world demographic vehicle ownership (ABS Census 2021 & TMR HTS Queensland):
            if arch == 'Student':
                npf = self.rng.uniform(0.75, 0.98)
                oa = self.rng.uniform(0.20, 0.50)
                ser = self.rng.uniform(0.40, 0.75)
                pdf = self.rng.uniform(0.30, 0.70)
                has_car = bool(self.rng.random() < 0.68)
                has_bike = bool(self.rng.random() < 0.32)
                has_scooter = bool(self.rng.random() < 0.16)
            elif arch == 'CBD_Professional':
                npf = self.rng.uniform(0.05, 0.35)
                oa = self.rng.uniform(0.15, 0.45)
                ser = self.rng.uniform(0.10, 0.40)
                pdf = self.rng.uniform(0.60, 0.95)
                has_car = bool(self.rng.random() < 0.96)
                has_bike = bool(self.rng.random() < 0.20)
                has_scooter = bool(self.rng.random() < 0.08)
            elif arch == 'Suburban_Worker':
                npf = self.rng.uniform(0.40, 0.70)
                oa = self.rng.uniform(0.20, 0.50)
                ser = self.rng.uniform(0.30, 0.60)
                pdf = self.rng.uniform(0.40, 0.75)
                has_car = bool(self.rng.random() < 0.95) # ABS Springwood: 2.2 vehicles/dwelling
                has_bike = bool(self.rng.random() < 0.18)
                has_scooter = bool(self.rng.random() < 0.06)
            else: # Fitness_Enthusiast
                npf = self.rng.uniform(0.20, 0.60)
                oa = self.rng.uniform(0.80, 0.98)
                ser = self.rng.uniform(0.40, 0.70)
                pdf = self.rng.uniform(0.05, 0.35)
                has_car = bool(self.rng.random() < 0.88)
                has_bike = bool(self.rng.random() < 0.92)
                has_scooter = bool(self.rng.random() < 0.10)

            records.append({
                'archetype': arch,
                'corridor_name': corridor.name,
                'distance_km': corridor.distance_km,
                'distance_to_transit_m': corridor.distance_to_transit_m,
                'car_time': corridor.car_travel_time_min,
                'transit_time': corridor.transit_travel_time_min,
                'bike_time': corridor.bike_travel_time_min,
                'car_cost': corridor.car_parking_fuel_cost,
                'npf': npf,
                'octopamine': oa,
                'serotonin': ser,
                'pdf': pdf,
                'has_car': has_car,
                'has_bike': has_bike,
                'has_scooter': has_scooter
            })

        return pd.DataFrame(records)

    def run_policy_scenario(
        self,
        population: pd.DataFrame,
        transit_fare_aud: float = 0.50,
        transit_speed_factor: float = 1.0,
        bike_effort_discount: float = 0.0,
        weather_heat_index: float = 0.25,
        stochastic_sampling: bool = True
    ) -> Dict[str, Any]:
        choices = []
        prob_car_list = []
        prob_transit_list = []
        prob_bike_list = []

        for _, row in population.iterrows():
            state = InternalNeuromodulatorState(
                npf_hunger=row['npf'],
                octopamine_vigor=row['octopamine'],
                serotonin_patience=row['serotonin'],
                pdf_sleep_debt=row['pdf']
            )

            t_bike = row['bike_time']
            t_car = row['car_time']
            dep_car = 9.0 - (t_car / 60.0)
            dep_bike = 9.0 - (t_bike / 60.0)
            bike_effort = max(0.2, 0.85 * (1.0 - bike_effort_discount))
            
            # Base transit times
            base_t_transit = row['transit_time'] * transit_speed_factor
            dist_m = row['distance_to_transit_m']
            
            # Walk to transit
            walk_time_min = dist_m / 84.0  # 1.4 m/s walking speed
            walk_effort = min(1.0, 0.15 + (dist_m / 3500.0))  # Scales up rapidly with distance
            t_transit_walk = base_t_transit + walk_time_min * 2.0  # round trip walk
            dep_transit_walk = 9.0 - (t_transit_walk / 60.0)
            
            # Scooter to transit
            scooter_time_min = dist_m / 240.0  # 4.0 m/s scooter speed
            scooter_effort = 0.10
            scooter_cost_one_way = 1.0 + 0.45 * scooter_time_min
            t_transit_scooter = base_t_transit + scooter_time_min * 2.0
            dep_transit_scooter = 9.0 - (t_transit_scooter / 60.0)

            # Choice Set Availability Gating (Only accessible modes are considered)
            options = []
            if row.get('has_car', True):
                options.append(CommuteOption(
                    name='Car',
                    travel_time_min=t_car,
                    monetary_cost_aud=row['car_cost'],
                    physical_effort=0.05,
                    departure_time_hr=dep_car,
                    comfort_index=0.95
                ))

            # Transit_Walk is universally available to anyone with locomotion
            options.append(CommuteOption(
                name='Transit_Walk',
                travel_time_min=t_transit_walk,
                monetary_cost_aud=transit_fare_aud * 2.0,
                physical_effort=walk_effort,
                departure_time_hr=dep_transit_walk,
                comfort_index=0.70
            ))

            # Transit_Scooter requires owning or having access to an e-scooter
            if row.get('has_scooter', True):
                options.append(CommuteOption(
                    name='Transit_Scooter',
                    travel_time_min=t_transit_scooter,
                    monetary_cost_aud=(transit_fare_aud + scooter_cost_one_way) * 2.0,
                    physical_effort=scooter_effort,
                    departure_time_hr=dep_transit_scooter,
                    comfort_index=0.80
                ))

            # Bicycle requires owning a functional bicycle
            if row.get('has_bike', True):
                options.append(CommuteOption(
                    name='Bicycle',
                    travel_time_min=t_bike,
                    monetary_cost_aud=0.0,
                    physical_effort=bike_effort,
                    departure_time_hr=dep_bike,
                    comfort_index=0.45
                ))

            decision = self.brain.decide_commute(
                options, state,
                weather_heat_index=weather_heat_index,
                stochastic_sample=stochastic_sampling,
                rng=self.rng
            )
            choices.append(decision['chosen_mode'])
            probs = decision['probabilities']
            prob_car_list.append(probs.get('Car', 0.0))
            prob_transit_list.append(probs.get('Transit_Walk', 0.0) + probs.get('Transit_Scooter', 0.0))
            prob_bike_list.append(probs.get('Bicycle', 0.0))

        pop_res = population.copy()
        pop_res['chosen_mode'] = choices
        pop_res['prob_car'] = prob_car_list
        pop_res['prob_transit'] = prob_transit_list
        pop_res['prob_bike'] = prob_bike_list

        mode_counts = pop_res['chosen_mode'].value_counts()
        total = len(pop_res)
        car_share = float(mode_counts.get('Car', 0) / total * 100.0)
        transit_walk_share = float(mode_counts.get('Transit_Walk', 0) / total * 100.0)
        transit_scooter_share = float(mode_counts.get('Transit_Scooter', 0) / total * 100.0)
        transit_share = transit_walk_share + transit_scooter_share
        bike_share = float(mode_counts.get('Bicycle', 0) / total * 100.0)

        car_trips = pop_res[pop_res['chosen_mode'] == 'Car']
        daily_vkt = float((car_trips['distance_km'] * 2.0).sum())
        daily_co2_kg = float(daily_vkt * 0.171)

        total_potential_vkt = float((pop_res['distance_km'] * 2.0).sum())
        vkt_saved = total_potential_vkt - daily_vkt
        co2_saved_kg = vkt_saved * 0.171

        archetype_breakdown = pop_res.groupby(['archetype', 'chosen_mode']).size().unstack(fill_value=0)
        arch_pct = (archetype_breakdown.T / archetype_breakdown.sum(axis=1)).T * 100.0

        corridor_breakdown = pop_res.groupby(['corridor_name', 'chosen_mode']).size().unstack(fill_value=0)
        corridor_pct = (corridor_breakdown.T / corridor_breakdown.sum(axis=1)).T * 100.0

        return {
            'transit_fare_aud': transit_fare_aud,
            'transit_speed_factor': transit_speed_factor,
            'bike_effort_discount': bike_effort_discount,
            'weather_heat_index': weather_heat_index,
            'mode_shares': {
                'Car': car_share,
                'Transit': transit_share,
                'Bicycle': bike_share
            },
            'mode_counts': {k: int(v) for k, v in mode_counts.items()},
            'daily_car_vkt': daily_vkt,
            'daily_vkt_saved': vkt_saved,
            'daily_co2_kg': daily_co2_kg,
            'daily_co2_saved_kg': co2_saved_kg,
            'archetype_breakdown_pct': arch_pct.round(1).to_dict(),
            'corridor_breakdown_pct': corridor_pct.round(1).to_dict()
        }

    def run_comparative_policy_study(self, n_commuters: int = 10000) -> Dict[str, Any]:
        population = self.generate_population(n_commuters)

        scenarios = {
            "Policy_1_Current_50c": {
                'transit_fare_aud': 0.50,
                'transit_speed_factor': 1.0,
                'bike_effort_discount': 0.0,
                'weather_heat_index': 0.25
            },
            "Policy_2_Fare_Rollback_Old_Tariff": {
                'transit_fare_aud': 4.50, # Old Brisbane 2-zone fare
                'transit_speed_factor': 1.0,
                'bike_effort_discount': 0.0,
                'weather_heat_index': 0.25
            },
            "Policy_3_50c_Plus_Brisbane_Metro": {
                'transit_fare_aud': 0.50,
                'transit_speed_factor': 0.70, # 30% faster via Brisbane Metro & dedicated busways
                'bike_effort_discount': 0.0,
                'weather_heat_index': 0.25
            },
            "Policy_4_Green_Mobility_All_In": {
                'transit_fare_aud': 0.50,
                'transit_speed_factor': 0.70,
                'bike_effort_discount': 0.40, # Shaded bikeways + CBD End-of-Trip showers
                'weather_heat_index': 0.25
            }
        }

        results = {}
        for sc_name, params in scenarios.items():
            res = self.run_policy_scenario(population, **params)
            results[sc_name] = res

        fare_sweep = []
        for fare in np.arange(0.0, 8.5, 0.5):
            sw_res = self.run_policy_scenario(population, transit_fare_aud=float(fare), weather_heat_index=0.25)
            fare_sweep.append({
                'fare_aud': float(fare),
                'car_share': sw_res['mode_shares']['Car'],
                'transit_share': sw_res['mode_shares']['Transit'],
                'bike_share': sw_res['mode_shares']['Bicycle']
            })

        demographics = {
            'overall_ownership': {
                'car': round(float(population['has_car'].mean() * 100), 1),
                'bike': round(float(population['has_bike'].mean() * 100), 1),
                'scooter': round(float(population['has_scooter'].mean() * 100), 1)
            },
            'archetype_counts': {k: int(v) for k, v in population['archetype'].value_counts().items()},
            'archetype_ownership': (population.groupby('archetype')[['has_car', 'has_bike', 'has_scooter']].mean() * 100.0).round(1).to_dict()
        }

        return {
            'total_commuters_simulated': n_commuters,
            'demographics': demographics,
            'scenarios': results,
            'fare_sensitivity_sweep': fare_sweep
        }

if __name__ == '__main__':
    sim = BrisbaneTransitSimulator(seed=42)
    print("Running 10,000 Commuter Simulation across 4 Brisbane Policies...")
    study = sim.run_comparative_policy_study(10000)
    
    with open('brisbane_transit_statistical_report.json', 'w', encoding='utf-8') as f:
        json.dump(study, f, indent=2)
        
    print("Simulation complete! Results written to brisbane_transit_statistical_report.json")
    for sc, data in study['scenarios'].items():
        print(f"\n--- {sc} ---")
        print(f"  Mode Split: Car {data['mode_shares']['Car']:.1f}%, Transit {data['mode_shares']['Transit']:.1f}%, Bike {data['mode_shares']['Bicycle']:.1f}%")
        print(f"  CO2 Saved Daily: {data['daily_co2_saved_kg']:.1f} kg")