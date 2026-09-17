"""
Legacy alias forwarding to src.simulation for backward compatibility.
"""
from src.simulation import CommuteCorridor, BRISBANE_CORRIDORS, BrisbaneTransitSimulator

__all__ = ["CommuteCorridor", "BRISBANE_CORRIDORS", "BrisbaneTransitSimulator"]