import pandas as pd
import os

SENSORS_PATH = 'data/On-street_Car_Parking_Sensor_Data_-_2019.csv'
BAYS_PATH = 'data/on-street-parking-bays.csv'

def diagnose_loss():
    print("--- DIAGNOSTIC START ---")
    
    # 1. Check Static Bays IDs
    print(f"Loading {BAYS_PATH}...")
    bays = pd.read_csv(BAYS_PATH)
    bays = bays.dropna(subset=['KerbsideID'])
    # Clean Format
    bays['KerbsideID'] = bays['KerbsideID'].astype(str).str.replace(r'\.0$', '', regex=True)
    unique_bays_ids = set(bays['KerbsideID'].unique())
    print(f"Static Bays: {len(bays)} rows, {len(unique_bays_ids)} unique IDs")

    # 2. Check 2019 Sensor IDs (Read in chunks to avoid memory crash)
    print(f"\nLoading {SENSORS_PATH} (Iterating to count)...")
    sensor_ids = set()
    total_rows = 0
    
    # We only need the ID column
    chunksize = 500000
    for chunk in pd.read_csv(SENSORS_PATH, usecols=['BayId'], chunksize=chunksize):
        # Rename for consistency
        chunk_ids = chunk['BayId'].dropna().astype(str).str.replace(r'\.0$', '', regex=True)
        sensor_ids.update(chunk_ids)
        total_rows += len(chunk)
        print(f"Processed {total_rows} rows...", end='\r')
    
    print(f"\nTotal 2019 Rows: {total_rows}")
    print(f"Unique 2019 IDs: {len(sensor_ids)}")

    # 3. Analyze Overlap
    common_ids = unique_bays_ids.intersection(sensor_ids)
    missing_ids = sensor_ids - unique_bays_ids
    
    print(f"\n--- OVERLAP ANALYSIS ---")
    print(f"IDs in BOTH sets: {len(common_ids)}")
    print(f"IDs in 2019 but MISSING from Static Bays: {len(missing_ids)}")
    print(f"Percentage of 2019 IDs lost: {len(missing_ids) / len(sensor_ids) * 100:.2f}%")
    
    if len(missing_ids) > 0:
        print(f"Example Missing IDs: {list(missing_ids)[:5]}")

if __name__ == "__main__":
    diagnose_loss()
