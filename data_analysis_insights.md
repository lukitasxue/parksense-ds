# ParkSense Data Analysis Insights

## 1. Parking Behavior Trends (Time)
*   **Peak Congestion**: The busiest hours for car arrivals are late afternoon (16:00 - 18:00), with the absolute peak at **17:00 (5 PM)**. This suggests a rush of activity related to end-of-work transitions or evening dining/entertainment.
*   **Morning Rush**: There is a secondary, smaller peak in the morning around **7:00 - 9:00 AM**, likely corresponding to commuters arriving for work.
*   **Quiet Hours**: Activity drops significantly after 20:00 (8 PM) and remains very low until 6:00 AM.
*   **Insight**: Models should treat "Time of Day" as a critical non-linear feature. A simple linear "later is busier" rule won't work because of the evening spike and overnight drop.

## 2. Spatial Distribution (Hotspots)
*   **Clustered Activity**: Parking sensors are not evenly distributed. They are heavily clustered in specific high-density zones (the CBD).
*   **Implication**: Location (`Latitude`, `Longitude`) is a powerful predictor. A car parking in a "hotspot" likely faces different availability probabilities than one on the fringe.

## 3. Duration of Stay
*   **Short Stays Dominate**: The vast majority of parking sessions are very short (< 15 minutes). This is visible in the huge spike on the left of the duration histogram.
*   **Turnover**: High turnover means availability changes rapidly. A spot occupied now has a high chance of becoming free in 15 minutes.
*   **Outliers**: There is a long tail of cars staying 1-3 hours, but they are the minority.
*   **Insight for Modeling**: Since most stays are short, the past state of the bay (e.g., "Was it occupied 10 mins ago?") might be less predictive than the general time/location trends, unless we know *exactly* when the car arrived.

## 4. Class Balance
*   **Balanced Dataset**: The target variable `is_free_15m` is reasonably balanced (~45% Occupied vs ~55% Free).
*   **Good News**: We do **not** need complex techniques like SMOTE or heavy class weighting. Standard accuracy/ROC-AUC metrics will be reliable.
