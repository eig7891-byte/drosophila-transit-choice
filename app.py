"""
Drosophila Connectome Transit Simulator (Entry Point)
"""
import runpy
import sys
import os

if __name__ == "__main__":
    target = os.path.join(os.path.dirname(__file__), "app_drosophila_transit.py")
    runpy.run_path(target, run_name="__main__")
