import pandas as pd
from sqlalchemy import create_engine

# Config - Using Transaction Pooler (IPv4)
DB_USER = "postgres.prwbzhkabpclahzaaffi"  # Format: postgres.{project-ref}
DB_PASS = "rDDXVckv2lpzlwBh"
DB_HOST = "aws-1-ap-south-1.pooler.supabase.com"  # Transaction Pooler
DB_PORT = "6543"  # Pooler port
DB_NAME = "postgres"

OUTPUT_PATH = "data/supabase_snapshots.csv"

def extract_data():
    connection_url = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"

    
    print(f"Connecting to Supabase Pooler: {DB_HOST}:{DB_PORT}...")
    try:
        engine = create_engine(connection_url)
        query = "SELECT * FROM public.snapshots ORDER BY id ASC"
        
        print("Executing Query...")
        chunk_size = 50000
        chunks = []
        
        # Using chunks for progress tracking
        for chunk in pd.read_sql(query, engine, chunksize=chunk_size):
            chunks.append(chunk)
            total = len(pd.concat(chunks))
            print(f"Downloaded {total:,} rows...", end='\r')
            
        df = pd.concat(chunks)
        print(f"\n[SUCCESS] Total Rows: {len(df):,}")
        
        # Save
        df.to_csv(OUTPUT_PATH, index=False)
        print(f"[SUCCESS] Saved to {OUTPUT_PATH}")
        
    except Exception as e:
        print(f"\n[ERROR] Connection Failed: {e}")

        print("Please check your network connection or VPN.")

if __name__ == "__main__":
    extract_data()