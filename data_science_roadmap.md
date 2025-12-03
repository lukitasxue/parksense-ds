# ParkSense Data Science Roadmap

## 1. Data Preparation (Cleaning & Merging)
**Goal**: Create a single "Master Table" for training.

*   **Inputs**:
    *   `on-street-car-parking-sensor-data-2019.csv` (Historical events)
    *   `on-street-parking-bays.csv` (Static locations)
*   **Steps**:
    1.  **Filter**: Remove rows with missing `KerbsideID` or invalid timestamps.
    2.  **Join**: Merge Historical data with Static data on `KerbsideID` to add `Latitude`, `Longitude`.
    3.  **Sort**: Ensure data is sorted by `KerbsideID` and `Time`.
    4.  **Target Creation**: For every row (event), look ahead 15, 30, and 45 minutes.
        *   Create columns: `is_free_15m`, `is_free_30m`, `is_free_45m` (0 or 1).

## 2. Exploratory Data Analysis (EDA)
**Goal**: Understand parking patterns to validate data and inspire features.

*   **Analyses to Run**:
    *   **Occupancy by Hour**: Plot average occupancy rate (0-1) vs Hour of Day (0-23). *Expectation: Peaks during business hours.*
    *   **Occupancy by Day**: Weekday vs Weekend patterns.
    *   **Turnover Rate**: Distribution of "Stay Duration". *How long do cars usually stay?*
    *   **Geospatial Heatmap**: Which streets are busiest? (Use Lat/Lon).

## 3. Feature Engineering
**Goal**: Convert raw data into model-ready numbers.

*   **Input Columns**: `Timestamp`, `Location`, `KerbsideID`.
*   **Engineered Features (X)**:
    *   `hour_sin`, `hour_cos`: Cyclical encoding of hour (so 23:00 is close to 00:00).
    *   `day_of_week`: 0-6 (Mon-Sun).
    *   `is_weekend`: Boolean.
    *   `latitude`, `longitude`: Spatial features.
    *   *(Advanced)* `historical_occupancy_rate`: The average occupancy for this specific bay at this hour (calculated from training set).
*   **Target Variables (y)**:
    *   `is_free_15m` (Binary)

## 4. Model Training
**Goal**: Train a model to predict `P(Free | Features)`.

*   **Model Selection**:
    *   **Baseline**: `LogisticRegression` (Simple, interpretable probabilities).
    *   **Recommended**: `RandomForestClassifier` (Handles non-linear time/space patterns well, robust to outliers).
*   **Evaluation**:
    *   Split data: Train (Jan-Oct 2019), Test (Nov-Dec 2019) - *Time-based split is crucial!*
    *   Metric: **ROC-AUC** or **Log Loss** (since we care about probability accuracy, not just hard yes/no).

## 5. Output
*   Save the trained model as a `.joblib` file (e.g., `parking_model_v1.joblib`).
*   Create a Python script `predict.py` that loads the model and accepts a `(lat, lon, time)` query.
