# 🚗 ParkSense: Intelligent Parking for Melbourne CBD

ParkSense is an AI-powered parking assistant that moves beyond simply showing where parking is available *now*—it predicts where it will be available in the **next 15 minutes**.

![ParkSense Demo Screenshot Placeholder](https://media.discordapp.net/attachments/1441015950425067530/1466673390017577001/image.png?ex=697d9989&is=697c4809&hm=62a35251b1e28fdb52861388c6f8aae90ea2f33f81135fff5ac5b796c40d902e&=&format=webp&quality=lossless&width=2462&height=1209)

## 🌟 The Vision
The core intention of ParkSense is to solve the "Binary Parking Problem." Standard apps tell you a spot is free, but by the time you drive there, it's often taken. ParkSense uses Machine Learning to provide a **probability percentage**, allowing users to make data-driven decisions while navigating the CBD.

---

## 🛠️ How It Works: The Pipeline

The system operates as a three-stage intelligence pipeline:

### 1. Real-Time Data Acquisition
The frontend fetches live sensor data directly from the **Melbourne Open Data API**. Every 15 minutes, the app heartbeats to synchronize several thousand sensor states (Present/Vacant) across the city.

### 2. Neighborhood Intelligence (The Model)
This is where the magic happens. Instead of tracking 3,000+ individual sensors (which are highly volatile and "noisy"), our AI uses a **Neighborhood Grouping Strategy**:
*   **The Logic**: We group bays into blocks of **20 units** based on their street segment (`kerbsideid`).
*   **The Intention**: Predicting if one exact spot will be free is a gamble; predicting the occupancy trend of a block is a science. This provides a much more reliable metric for a driver looking for a space in a specific area.

### 3. AI Prediction Layer
When you click a bay on the map:
1.  **Frontend** identifies the bay's neighborhood and sends its current state to our **Python Backend**.
2.  **Backend** feeds this into a trained **XGBoost Regressor** model.
3.  **The AI** analyzes the current time, day of the week, and recent 30-minute trends to calculate the probability of that bay being free in the next **15-minute horizon**.

---

## 🧠 Training & Design
*   **Model**: XGBoost (Extreme Gradient Boosting).
*   **Training Data**: Months of historical parking snapshots captured and stored in **Supabase**.
*   **Features**: The model looks at `hour_of_day`, `day_of_week`, and `lag_features` (recent occupancy trends) to understand the "rhythm" of the city.

---

## 💻 Tech Stack
*   **Frontend**: Next.js (App Router), MapLibre GL for high-performance geospatial rendering.
*   **Backend**: FastAPI (Python), XGBoost for real-time model inference.
*   **Data/Infrastructure**: Supabase (PostgreSQL), Melbourne Open Data API.

---

## 🚦 Quick Start

To get the project running locally, please refer to our detailed guides:

*   📖 **[Quick Start Guide](./QUICK_START.md)** - Get the frontend up and running in 2 minutes.
*   🗺️ **[API Integration Details](./MELBOURNE_API_INTEGRATION.md)** - Explaining the direct connection to Melbourne's sensors.


# parksense-be

ParkSense backend written in FastAPI (Python).

## Getting started

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # or .venv\\Scripts\\activate on Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create your `.env` based on `.env.example` and fill in:

   - `DATABASE_URL` pointing to a Postgres instance (for example, Supabase project's Postgres URL using the `postgresql+asyncpg://` scheme).
   - Optional Supabase keys if you need them elsewhere (`SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`).

4. Run the API:

   ```bash
   uvicorn app.main:app --reload
   ```

The API root is available at `/`.

### Database and migrations

- Async database access is configured via SQLAlchemy in `app/db/` using `DATABASE_URL`.
- Alembic configuration lives under `migrations/` and is driven by `alembic.ini` at the project root.

#### Running migrations

1. Create a new migration after you change models:

  ```bash
  alembic revision -m "describe change"  # creates a file under migrations/versions/
  ```

2. Apply all pending migrations:

  ```bash
  alembic upgrade head
  ```

### Health check

- Path: `/api/v1/health`
- Method: `GET`
- Response body:
  - `status`: `"ok"`
  - `environment`: current environment name (for example, `"local"`)
  - `service`: service / project name (for example, `"ParkSense API"`)



