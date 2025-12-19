import pandas as pd

BAYS_PATH = 'data/on-street-parking-bays.csv'
SENSORS_PATH = 'data/on-street-parking-bay-sensors.csv' # Note: This is the LIVE sensor file, not 2019

def check_live():
    print("--- CONTROL TEST: Live Sensors vs Static Bays ---")
    
    # 1. Load Static Bays
    print(f"Loading {BAYS_PATH}...")
    bays = pd.read_csv(BAYS_PATH)
    bays_ids = set(bays['KerbsideID'].dropna().astype(str).str.replace(r'\.0$', '', regex=True))
    print(f"Static Map IDs: {len(bays_ids)}")

    # 2. Load Live Sensors
    print(f"Loading {SENSORS_PATH}...")
    sensors = pd.read_csv(SENSORS_PATH)
    # Note: Column might be 'KerbsideID' or 'BayId' in this file too
    col_name = 'KerbsideID' if 'KerbsideID' in sensors.columns else 'BayId'
    print(f"Using Sensor Column: {col_name}")
    
    sensor_ids = set(sensors[col_name].dropna().astype(str).str.replace(r'\.0$', '', regex=True))
    print(f"Live Sensor IDs: {len(sensor_ids)}")
    
    # 3. Overlap
    common = bays_ids.intersection(sensor_ids)
    print(f"\n--- RESULTS ---")
    print(f"Overlap Count: {len(common)}")
    print(f"Match Rate (Sensor -> Map): {len(common) / len(sensor_ids) * 100:.2f}%")

if __name__ == "__main__":
    check_live()
