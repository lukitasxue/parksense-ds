import pandas as pd
import os

SENSORS_PATH = 'data/On-street_Car_Parking_Sensor_Data_-_2019.csv'
BAYS_PATH = 'data/on-street-parking-bays.csv'

def check_alternatives():
    print("--- HYPOTHESIS TEST: DeviceId & RoadSegmentID ---")
    
    # 1. Inspect Static Data Columns
    print(f"Loading {BAYS_PATH}...")
    bays = pd.read_csv(BAYS_PATH)
    print(f"Static Columns: {list(bays.columns)}")
    
    # Check if DeviceId exists in Static (it usually doesn't, but let's check)
    has_device_id_static = 'DeviceId' in bays.columns
    
    # RoadSegmentID is definitely in Static
    static_segments = set(bays['RoadSegmentID'].dropna().astype(str))
    print(f"Unique Static RoadSegmentIDs: {len(static_segments)}")

    # 2. Check 2019 Data
    print(f"\nLoading {SENSORS_PATH} (Sample)...")
    # We load a sample to check column presence first
    sample = pd.read_csv(SENSORS_PATH, nrows=5)
    print(f"2019 Columns: {list(sample.columns)}")
    
    # 2019 has 'DeviceId' -> Let's check overlap with Static 'RoadSegmentID' (unlikely match, but requested)
    # 2019 has 'StreetId' -> Maybe matches RoadSegmentID?
    
    print("\nChecking Overlaps (Full Scan)...")
    
    sensor_devices = set()
    sensor_segments = set() # We'll try to match StreetId or similar
    
    # Iterate
    chunksize = 500000
    for chunk in pd.read_csv(SENSORS_PATH, usecols=['DeviceId', 'StreetId'], chunksize=chunksize):
        sensor_devices.update(chunk['DeviceId'].dropna().astype(str))
        sensor_segments.update(chunk['StreetId'].dropna().astype(str))
        print(f"Collected {len(sensor_devices)} devices, {len(sensor_segments)} streets...", end='\r')

    print("\n\n--- RESULTS ---")
    
    # Overlap 1: 2019 DeviceId vs Static RoadSegmentID (Cross-match?)
    match_dev_seg = static_segments.intersection(sensor_devices)
    print(f"Overlap (2019 DeviceId == Static RoadSegmentID): {len(match_dev_seg)}")
    
    # Overlap 2: 2019 StreetId vs Static RoadSegmentID
    match_str_seg = static_segments.intersection(sensor_segments)
    print(f"Overlap (2019 StreetId == Static RoadSegmentID): {len(match_str_seg)}")
    
    # Overlap 3: 2019 DeviceId vs Static KerbsideID (Just in case)
    bays_kerb = set(bays['KerbsideID'].dropna().astype(str).str.replace(r'\.0$', '', regex=True))
    match_dev_kerb = bays_kerb.intersection(sensor_devices)
    print(f"Overlap (2019 DeviceId == Static KerbsideID):    {len(match_dev_kerb)}")

if __name__ == "__main__":
    check_alternatives()
