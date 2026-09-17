"""
Drosophila Neuromodulatory System & Physiological Internal State Gates
----------------------------------------------------------------------
Models the chemical internal state variables:
- NPF (Neuropeptide F): Budget scarcity / financial urgency.
- Octopamine (OA): Locomotor vigor / physical stamina.
- Serotonin (5-HT): Delay discounting resilience / waiting tolerance.
- PDF (Pigment-Dispersing Factor): Morning circadian sleep pressure.
"""
from dataclasses import dataclass

@dataclass
class InternalNeuromodulatorState:
    npf_hunger: float           # [0, 1] Financial budget pressure (hungry for savings)
    octopamine_vigor: float     # [0, 1] Physical fitness drive / athletic stamina
    serotonin_patience: float   # [0, 1] Tolerance for transit delay / waiting
    pdf_sleep_debt: float       # [0, 1] Circadian morning sleepiness / sleep inertia
