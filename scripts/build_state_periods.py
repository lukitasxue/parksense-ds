import pandas as pd

INPUT_CSV = "data/supabase_snapshots.csv"
OUTPUT_CSV = "data/kerbside_state_periods.csv"

def build_state_periods():
    df = pd.read_csv(INPUT_CSV)

    # Parse the actual event timestamp
    df["status_timestamp"] = pd.to_datetime(df["status_timestamp"], utc=True)

    # Sort by kerbside and time
    df = df.sort_values(["kerbsideid", "status_timestamp"])

    # Each row starts a new state
    df["start_time"] = df["status_timestamp"]

    # End time = next change for the same kerbside
    df["end_time"] = (
        df.groupby("kerbsideid")["status_timestamp"]
        .shift(-1)
    )

    # Drop last row per kerbside (no known end yet)
    df = df.dropna(subset=["end_time"])

    # Build refined dataset
    periods = df[
        ["kerbsideid", "status", "start_time", "end_time"]
    ].copy()

    # Duration in minutes
    periods["duration_minutes"] = (
        (periods["end_time"] - periods["start_time"])
        .dt.total_seconds() / 60
    )

    periods.to_csv(OUTPUT_CSV, index=False)
    print(f"[SUCCESS] Saved {len(periods):,} rows to {OUTPUT_CSV}")

if __name__ == "__main__":
    build_state_periods()
