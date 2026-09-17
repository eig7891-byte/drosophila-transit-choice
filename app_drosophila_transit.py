"""
🧠 果蠅大腦通勤決策模擬器 (Drosophila-Brain Commute Simulator: Brisbane Transit)
---------------------------------------------------------------------------------
Backward-compatibility entry point forwarding to the modularized app.py.
"""
import os
import runpy

if __name__ == "__main__" or "streamlit" in __name__:
    entry = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    runpy.run_path(entry, run_name="__main__")