# Parking Availability Prediction Strategy

## Current Objective
Build a predictive model to forecast parking bay availability at 15/30/45 minute intervals.

## Analysis Phase 1: Kerbside ID Pattern Investigation

### What We're Testing
**Hypothesis**: If kerbside IDs are sequential and spatially correlated (e.g., IDs 7000-7010 are geographically close), we can group nearby bays and predict availability for groups rather than individual bays.

### Why Grouping Matters
1. **Reduces model complexity**: Instead of predicting 3,309 individual bays → predict ~300-400 groups
2. **More robust**: Aggregated data is less noisy
3. **Practical**: Users care about "is parking available in this area?" not "is bay #7432 available?"
4. **Better generalization**: Model learns area patterns, not individual bay quirks

### Step 1: Run the Analysis Notebook 📊

I've created `01_kerbside_id_analysis.ipynb` for you. Run it to analyze:

1. **Kerbside ID distribution**
   - Min/max IDs
   - Range and gaps between consecutive IDs
   
2. **Sequentiality check**
   - Are IDs sequential (1, 2, 3...) or random?
   - What's the average gap between consecutive IDs?
   
3. **Clustering potential**
   - Can we group by 10s? 100s? 1000s?
   - How many bays per cluster?

4. **Visual analysis**
   - Distribution plots
   - Gap analysis
   - Cluster visualization

### To Run:
```bash
cd parksense-ds
jupyter notebook 01_kerbside_id_analysis.ipynb
```

Or in VS Code:
1. Open the notebook
2. Select Python kernel
3. Click "Run All"

---

## What to Report Back

After running the notebook, tell me:

1. **Are IDs mostly sequential?** (e.g., "80% of gaps are <= 10")
2. **What's the recommended grouping?** (The notebook will tell you)
3. **Screenshots** of the plots if possible

---

## Next Steps (After Results)

### Scenario A: IDs ARE Sequential & Spatially Correlated ✅

**Then we proceed with grouping strategy:**

1. **Create bay groups** (e.g., group by 100s: 7000-7099, 7100-7199...)

2. **Feature engineering per group:**
   - Hour of day (0-23)
   - Day of week (Mon-Sun)
   - Month
   - Group ID
   - Group-level occupancy rate
   - Historical patterns

3. **Target variable:**
   - Group occupancy rate at t+15min, t+30min, t+45min
   - Or: Probability of finding available parking in the group

4. **Model architecture:**
   - **Option 1**: Regression (predict occupancy %)
   - **Option 2**: Classification (available/not available)
   - **Option 3**: Time series (LSTM/GRU if we have good temporal data)

5. **Training approach:**
   - Train/test split by time (not random - to avoid data leakage)
   - Validate on recent data
   - Models to try:
     - XGBoost/LightGBM (fast, accurate)
     - Random Forest (baseline)
     - LSTM if we use sequences

---

### Scenario B: IDs Are NOT Sequential/Correlated ❌

**Then we use spatial grouping instead:**

1. **Need lat/lon data**
   - Good news: Melbourne API has it!
   - We'll fetch full bay metadata with coordinates

2. **Spatial clustering:**
   - Use K-Means or DBSCAN to cluster bays by location
   - Create ~300-400 spatial zones
   - Each zone = a group

3. **Then same modeling approach as Scenario A**

---

## Data Preparation Steps

### 1. Merge Snapshot Data with Bay Metadata

```python
# You have:
snapshots.csv: id, kerbsideid, status, status_timestamp, created_at

# We need to fetch:
bay_metadata.csv: kerbsideid, lat, lon, road_segment_description

# Then merge both for complete dataset
```

### 2. Create Temporal Features

```python
df['hour'] = pd.to_datetime(df['status_timestamp']).dt.hour
df['day_of_week'] = pd.to_datetime(df['status_timestamp']).dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6])
```

### 3. Create Target (Future Availability)

```python
# For each snapshot, we want to know: "15/30/45 min later, is this bay/group occupied?"
df = df.sort_values(['kerbsideid', 'status_timestamp'])
df['status_15min_later'] = df.groupby('kerbsideid')['status'].shift(-1)
df['status_30min_later'] = df.groupby('kerbsideid')['status'].shift(-2)
# etc.
```

### 4. Handle Imbalanced Data

If 90% of bays are always occupied → use SMOTE or class weighting

---

## Model Evaluation

### Metrics to Track:
- **Accuracy**: Overall correctness
- **Precision/Recall**: Important if availability is rare
- **F1-Score**: Balance of precision/recall
- **AUC-ROC**: Model's discriminative power
- **MAE/RMSE**: If predicting occupancy %

### Real-world validation:
- "If I arrive at time T, what's the chance I'll find parking?"
- "Which areas should I check first?"

---

## Summary

**Right now**: Run the notebook and report findings

**Next (if grouping works)**:
1. Define groups
2. Aggregate data by group
3. Engineer features
4. Train model
5. Evaluate & iterate

**Next (if grouping doesn't work)**:
1. Fetch lat/lon data
2. Spatial clustering
3. Same as above

---

## Questions to Think About

1. **What's your prediction horizon?** 15/30/45 min?
2. **What's the use case?** 
   - Real-time recommendation ("check this area")
   - Or planning ("best time to visit")
3. **How often do you want predictions?** Every 5 min? 15 min?

I'm ready to help with the next phase once you share the notebook results! 🚀
