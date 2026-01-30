import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import os

def train_production_model():
    """
    Trains the production XGBoost model to predict parking availability.
    The model uses 'neighborhood' grouping (20 bays) to provide more stable 
    predictions than tracking individual noisy sensor data.
    """
    print("🚀 Loading snapshot data...")
    # Load historical sensor data exported from Supabase
    df = pd.read_csv('data/supabase_snapshots.csv')
    df['status_timestamp'] = pd.to_datetime(df['status_timestamp'])
    
    # --- 1. Neighborhood Grouping Logic ---
    # We group bays into blocks of 20 based on their kerbside ID.
    # Individual sensor data is often too 'noisy' (flipping between Present/Vacant).
    # Predicting the occupancy % of a block is more accurate for the user.
    print("📍 Grouping bays into neighborhoods...")
    df['group_id'] = (df['kerbsideid'] // 20) * 20
    df['is_occupied'] = df['status'].apply(lambda x: 1 if x == 'Present' else 0)
    
    # 2. Time-Series Resampling 
    # Convert individual sensor events into consistent 15-minute 'heartbeats'.
    # This calculates the average occupancy ratio (0.0 to 1.0) for each group at each interval.
    print("📊 Preprocessing time-series into 15-min intervals...")
    group_ts = df.groupby(['group_id', pd.Grouper(key='status_timestamp', freq='15min')])['is_occupied'].mean().reset_index()
    group_ts.columns = ['group_id', 'timestamp', 'occupancy_ratio']
    group_ts = group_ts.sort_values(['group_id', 'timestamp'])
    
    # --- 3. Feature Engineering ---
    # We create inputs (X) that help the model understand 'patterns'.
    print("🛠️ Engineering features (lags and time-based)...")
    group_ts['hour'] = group_ts['timestamp'].dt.hour
    group_ts['day_of_week'] = group_ts['timestamp'].dt.dayofweek
    
    # Lag Features: Looking at what happened 15m and 30m ago to find trends
    group_ts['lag_15m'] = group_ts.groupby('group_id')['occupancy_ratio'].shift(1)
    group_ts['lag_30m'] = group_ts.groupby('group_id')['occupancy_ratio'].shift(2)
    
    # Target Variable: This is what we want the model to learn to predict
    # We shift the current occupancy back by 1 (which represents 15 minutes into the future)
    group_ts['target_15m'] = group_ts.groupby('group_id')['occupancy_ratio'].shift(-1)
    
    # Remove rows with empty values created by the 'shifts' (the very first and last records)
    model_data = group_ts.dropna()
    
    # Define the exact order of features for the model
    features = ['group_id', 'occupancy_ratio', 'hour', 'day_of_week', 'lag_15m', 'lag_30m']
    X = model_data[features]
    y = model_data['target_15m']
    
    # --- 4. Model Training ---
    # Using XGBoost Regressor: A powerful tree-based model.
    # We optimize for 'Regression' because we are predicting a percentage (0.0 to 1.0).
    print(f"🧠 Training XGBoost model on {len(X)} samples...")
    model = XGBRegressor(
        n_estimators=300,    # Number of trees
        learning_rate=0.05,  # Speed of learning
        max_depth=7,         # Complexity of each tree
        subsample=0.8,       # % of data used to grow each tree (prevents overfitting)
        colsample_bytree=0.8
    )
    model.fit(X, y)
    
    # --- 5. Exporting for Production ---
    # Save the model in Universal Binary JSON format for fast loading in the FastAPI backend.
    os.makedirs('models', exist_ok=True)
    model_file = 'models/parking_model_15m.ubj'
    model.save_model(model_file)
    
    # Save the feature sequence to ensure the backend provides data in the SAME order
    with open('models/features.txt', 'w') as f:
        f.write(",".join(features))
        
    print(f"✅ Success! Model saved to {model_file}")
    print(f"📍 Features expected by BE: {features}")

if __name__ == "__main__":
    train_production_model()

