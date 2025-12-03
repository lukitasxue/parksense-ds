import pandas as pd
import sys

def log(msg, file):
    print(msg)
    file.write(msg + "\n")

try:
    with open('analysis_report.txt', 'w') as f:
        # Load datasets
        log("Loading datasets...", f)
        bays = pd.read_csv('data/on-street-parking-bays.csv')
        sensors = pd.read_csv('data/on-street-parking-bay-sensors.csv')

        log(f"Bays columns: {list(bays.columns)}", f)
        log(f"Sensors columns: {list(sensors.columns)}", f)

        # Check KerbsideID
        log("\n--- KerbsideID Analysis ---", f)
        log(f"Total bays rows: {len(bays)}", f)
        bays_with_id = bays[bays['KerbsideID'].notna()]
        log(f"Bays with KerbsideID: {len(bays_with_id)}", f)
        log(f"Unique KerbsideIDs in bays: {bays['KerbsideID'].nunique()}", f)

        log(f"\nTotal sensor readings: {len(sensors)}", f)
        sensors_with_id = sensors[sensors['KerbsideID'].notna()]
        log(f"Sensors with KerbsideID: {len(sensors_with_id)}", f)
        log(f"Unique KerbsideIDs in sensors: {sensors['KerbsideID'].nunique()}", f)

        # Overlap
        # Convert to string to ensure type matching, dropping .0 if float
        bays_ids = set(bays_with_id['KerbsideID'].astype(str).str.replace(r'\.0$', '', regex=True))
        sensor_ids = set(sensors_with_id['KerbsideID'].astype(str).str.replace(r'\.0$', '', regex=True))

        common_ids = bays_ids & sensor_ids
        log(f"\nCommon KerbsideIDs: {len(common_ids)}", f)

        # Check if all sensor IDs are in bays
        missing_in_bays = sensor_ids - bays_ids
        log(f"Sensor IDs NOT in bays file: {len(missing_in_bays)}", f)
        if len(missing_in_bays) > 0:
            log(f"Example missing IDs (first 5): {list(missing_in_bays)[:5]}", f)

        # Check duplicates in bays
        log("\n--- Duplicates in Bays ---", f)
        dupes = bays_with_id[bays_with_id.duplicated('KerbsideID', keep=False)]
        if not dupes.empty:
            log(f"Duplicate KerbsideIDs found in bays: {len(dupes)}", f)
            log(str(dupes[['KerbsideID', 'RoadSegmentDescription']].sort_values('KerbsideID').head()), f)
        else:
            log("No duplicate KerbsideIDs in bays (ignoring NaNs).", f)

except Exception as e:
    print(f"An error occurred: {e}")
