import pandas as pd

SUPABASE_DATA = 'data/supabase_snapshots.csv'
STATIC_BAYS = 'data/on-street-parking-bays.csv'

def validate_supabase_data():
    print("=== SUPABASE DATA VALIDATION ===\n")
    
    # Load data
    print("Loading Supabase snapshots...")
    df = pd.read_csv(SUPABASE_DATA, parse_dates=['status_timestamp'])
    print(f"Total Rows: {len(df):,}")
    print(f"Columns: {list(df.columns)}\n")
    
    # 1. Time Range
    print("--- TIME RANGE ---")
    min_date = df['status_timestamp'].min()
    max_date = df['status_timestamp'].max()
    duration = max_date - min_date
    
    print(f"Start: {min_date}")
    print(f"End:   {max_date}")
    print(f"Duration: {duration.days} days ({duration.days / 7:.1f} weeks)\n")
    
    # 2. Ghost Bay Check
    print("--- GHOST BAY CHECK ---")
    bays = pd.read_csv(STATIC_BAYS)
    bays_ids = set(bays['KerbsideID'].dropna().astype(str).str.replace(r'\.0$', '', regex=True))
    
    # Clean Supabase IDs
    supabase_ids = set(df['kerbsideid'].dropna().astype(str).str.replace(r'\.0$', '', regex=True))
    
    overlap = bays_ids.intersection(supabase_ids)
    ghost_ids = supabase_ids - bays_ids
    
    print(f"Unique IDs in Supabase: {len(supabase_ids)}")
    print(f"Unique IDs in Static Map: {len(bays_ids)}")
    print(f"Matching IDs: {len(overlap)}")
    print(f"Ghost IDs: {len(ghost_ids)} ({len(ghost_ids) / len(supabase_ids) * 100:.2f}%)\n")
    
    if len(ghost_ids) > 0:
        print(f"Example Ghost IDs: {list(ghost_ids)[:5]}\n")
    
    # 3. Status Distribution
    print("--- STATUS DISTRIBUTION ---")
    status_counts = df['status'].value_counts()
    print(status_counts)
    print()
    
    # 4. Recommendation
    print("--- RECOMMENDATION ---")
    if len(ghost_ids) / len(supabase_ids) < 0.05:  # Less than 5% ghosts
        print("✓ EXCELLENT: Less than 5% ghost bays!")
        print("✓ This dataset is MUCH better than the 2019 data.")
        print("✓ Recommended: Use this for training.")
    else:
        print("⚠ Warning: Significant ghost bays detected.")
        print("Consider investigating the mismatch.")

if __name__ == "__main__":
    validate_supabase_data()
