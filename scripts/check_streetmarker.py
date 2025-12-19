import pandas as pd
import os

SENSORS_PATH = 'data/On-street_Car_Parking_Sensor_Data_-_2019.csv'
BAYS_PATH = 'data/on-street-parking-bays.csv'

def check_streetmarker():
    print("--- HYPOTHESIS TEST: StreetMarker vs KerbsideID ---")
    
    # 1. Load Static Bays (Target IDs)
    print(f"Loading {BAYS_PATH}...")
    bays = pd.read_csv(BAYS_PATH)
    bays_ids = set(bays['KerbsideID'].dropna().astype(str).str.replace(r'\.0$', '', regex=True))
    print(f"Target (2024 KerbsideIDs): {len(bays_ids)}")

    # 2. Load 2019 'StreetMarker' (Candidate IDs)
    print(f"\nLoading {SENSORS_PATH} (StreetMarker column)...")
    street_markers = set()
    bay_ids = set() # Also load BayId again for comparison
    
    # Iterating to save RAM
    chunksize = 500000
    for chunk in pd.read_csv(SENSORS_PATH, usecols=['StreetMarker', 'BayId'], chunksize=chunksize):
        # normalize
        sm = chunk['StreetMarker'].dropna().astype(str).str.replace(r'\.0$', '', regex=True)
        bi = chunk['BayId'].dropna().astype(str).str.replace(r'\.0$', '', regex=True)
        
        street_markers.update(sm)
        bay_ids.update(bi)
        print(f"Collected {len(street_markers)} markers, {len(bay_ids)} IDs...", end='\r')
    
    print(f"\n\n--- RESULTS ---")
    
    # 3. Compare Matches
    match_sm = bays_ids.intersection(street_markers)
    match_bi = bays_ids.intersection(bay_ids)
    
    print(f"Unique StreetMarkers in 2019: {len(street_markers)}")
    print(f"Unique BayIds in 2019:        {len(bay_ids)}")
    
    print(f"\nMatch Count (StreetMarker == KerbsideID): {len(match_sm)}")
    print(f"Match Count (BayId == KerbsideID):        {len(match_bi)}")
    
    if len(match_sm) > len(match_bi):
        print("\nCONCLUSION: StreetMarker is the BETTER key!")
    else:
        print("\nCONCLUSION: BayId is BETTER (or StreetMarker is worse).")

if __name__ == "__main__":
    check_streetmarker()
