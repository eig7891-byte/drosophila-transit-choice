"""
Brisbane Transit Corridor Definitions & Physical Route Parameters
------------------------------------------------------------------
"""
from dataclasses import dataclass
from typing import List

@dataclass
class CommuteCorridor:
    name: str
    distance_km: float
    car_travel_time_min: float
    transit_travel_time_min: float
    bike_travel_time_min: float
    car_parking_fuel_cost: float
    distance_to_transit_m: float = 400.0

BRISBANE_CORRIDORS: List[CommuteCorridor] = [
    CommuteCorridor("Springwood to Rochedale South (5.2km Local)", 5.24, 8.5, 20.0, 18.0, 12.0, 2200.0),
    CommuteCorridor("Springwood to UQ St Lucia (28.8km University)", 28.78, 38.0, 42.0, 85.0, 26.5, 2200.0),
    CommuteCorridor("Chermside to CBD (Northern)", 10.5, 30.0, 50.0, 45.0, 26.0, 800.0),
    CommuteCorridor("Indooroopilly to CBD (Western)", 7.2, 22.0, 35.0, 32.0, 24.0, 600.0),
    CommuteCorridor("Mt Gravatt to CBD (South-East)", 13.8, 35.0, 55.0, 58.0, 28.0, 1500.0),
    CommuteCorridor("Logan Central to CBD (Outer South)", 26.5, 45.0, 85.0, 110.0, 34.0, 1800.0),
    CommuteCorridor("Carindale to CBD (Eastern)", 11.0, 28.0, 48.0, 48.0, 25.0, 400.0)
]
