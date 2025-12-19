import pandas as pd

FILE_PATH = 'data/on-street-parking-bay-sensors.csv'

def analyze_live_file():
    print(f"Loading {FILE_PATH}...")
    df = pd.read_csv(FILE_PATH)
    
    print(f"Total Rows: {len(df)}")
    
    # Check for time columns
    time_cols = [c for c in df.columns if 'time' in c.lower() or 'date' in c.lower()]
    print(f"Time Columns found: {time_cols}")
    
    if not time_cols:
        print("No time columns found! It might be a static snapshot.")
        return

    # Analyze primary time column (usually Status_Timestamp or LastUpdated)
    # We prefer Status_Timestamp as it reflects the event time
    target_col = 'Status_Timestamp' if 'Status_Timestamp' in df.columns else time_cols[0]
    
    print(f"Analyzing Time Range using: {target_col}")
    df[target_col] = pd.to_datetime(df[target_col], errors='coerce')
    
    min_date = df[target_col].min()
    max_date = df[target_col].max()
    
    print(f"Start Time: {min_date}")
    print(f"End Time:   {max_date}")
    
    if pd.notnull(min_date) and pd.notnull(max_date):
        duration = max_date - min_date
        print(f"Time Span:  {duration}")
    
    # Check if it's a snapshot (1 row per sensor) or a log (many rows per sensor)
    # Using 'KerbsideID' or 'BayId'
    id_col = 'KerbsideID' if 'KerbsideID' in df.columns else 'BayId'
    if id_col in df.columns:
        unique_ids = df[id_col].nunique()
        print(f"Unique Sensors: {unique_ids}")
        ratio = len(df) / unique_ids
        print(f"Avg Records per Sensor: {ratio:.2f}")
        
        if ratio < 1.1:
            print("\nCONCLUSION: This is likely a SNAPSHOT (Current State only).")
            print("It cannot be used for training history.")
        else:
            print(f"\nCONCLUSION: This contains history ({ratio:.1f} events per sensor).")

if __name__ == "__main__":
    analyze_live_file()
