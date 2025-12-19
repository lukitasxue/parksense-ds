# Model Training Results (Baseline)

## 1. Top-Level Metrics
*   **Accuracy**: 61%
*   **ROC-AUC**: 0.67
*   **Conclusion**: The model is better than random guessing (which would be ~50%), but it still has significant room for improvement. It correctly predicts the status of a parking spot about 6 times out of 10.

## 2. Detailed Performance
*   **Precision (Free/1)**: 66%. When the model says "This spot is Free", it is correct 66% of the time. This is decent for a user-facing app (minimizing false hope).
*   **Recall (Free/1)**: 66%. The model captures 66% of all actual free spots.
*   **Precision (Occupied/0)**: 55%. The model struggles more with identifying occupied spots, often mistaking them for free ones.

## 3. Feature Importance
*   **#1 Predictor: Hour**: As expected, the time of day is by far the strongest signal.
*   **#2 Predictor: Location (Lat/Lon)**: Where the spot is matters significantly.
*   **Weak Predictor**: Weekend status. This is surprising! It suggests parking patterns in the CBD might be similar on weekends (shoppers) vs. weekdays (workers), or our `is_weekend` feature is too simple.

## 4. Recommendations for Next Iteration
1.  **More Data**: We only used a tiny 1% sample. Training on 10% or 100% of the 2019 data will likely boost accuracy by 5-10%.
2.  **Better Features**: 
    *   Add `nearby_businesses` or `zone_type` to give the model more context about location.
    *   Cyclical Time: Transform `hour` into `sin(hour)` and `cos(hour)` so 23:00 is close to 00:00.
3.  **Hyperparameter Tuning**: We used default settings. Tweak `max_depth` and `n_estimators`.
