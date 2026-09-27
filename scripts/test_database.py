"""
Verification test script for src.data.database module.
"""
import sys
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.data.database import get_db, TransitDatabase

def main():
    print("Testing TransitDatabase interface...")
    db = get_db()
    
    # 1. Status
    status = db.get_status()
    print("\n--- Database Status ---")
    print(f"Path: {status['db_path']}")
    print(f"Size: {status['file_size_bytes']} bytes")
    print("Table row counts:")
    for tbl, count in status['table_counts'].items():
        print(f"  - {tbl}: {count} rows")

    # 2. Corridors
    print("\n--- Corridors Query ---")
    df_corridors = db.get_corridors()
    print(df_corridors[["name", "distance_km", "transit_travel_time_min", "car_parking_fuel_cost"]])

    # 3. Patronage by Era
    print("\n--- Patronage by Policy Era Summary ---")
    df_era = db.get_patronage_by_era_summary()
    print(df_era.head(6))

    # 4. Calibration Targets
    print("\n--- Calibration Targets ---")
    df_targets = db.get_calibration_targets()
    print(df_targets)

    # 5. Connectome Neurons (MBON search)
    print("\n--- Neuron Search (Approach / Incentive) ---")
    df_neurons = db.get_neurons(transit_role="Approach")
    print(df_neurons[["root_id", "primary_type", "transit_role", "name"]].head(5))

    # 6. Cross-table Universal Search
    print("\n--- Cross-table Search for 'Springwood' ---")
    results = db.search_all("Springwood")
    for tbl, df in results.items():
        print(f"Found {len(df)} matching rows in '{tbl}'")

    print("\nAll database tests passed successfully!")

if __name__ == "__main__":
    main()
