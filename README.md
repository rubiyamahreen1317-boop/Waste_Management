# Canteen Food Waste Management System

A Flask dashboard for reviewing canteen waste records, comparing regression models, generating day/week/month forecasts, and planning compost or biogas routing.

## Setup and run

The app uses Python 3.11 and reads the active dataset from `data/food_waste.csv`.

```bash
uv pip install --python python --target .pythonlibs/lib/python3.11/site-packages -r requirements.txt
python app.py
```

Open the Replit preview after starting **Start application**. Flask binds to `0.0.0.0` and uses port `5000` (or the `PORT` environment variable when supplied).

## Data

The active CSV is the supplied `college_canteen_food_waste_demo.csv`, copied to `data/food_waste.csv`. It contains 2,190 rows from 365 dates and is marked `synthetic_demo`; it is demonstration data, not measured canteen operations. The original CSV from the ZIP is preserved as `data/food_waste_original.csv`, and the supplied demo copy is also kept at `data/college_canteen_food_waste_demo.csv`.

Missing canteen fields are filled with seeded values and listed as simulated in the dashboard. Existing data values are not presented as measured ground truth just because a column is present. Synthetic demo model scores do not prove real-world accuracy.

Use **Upload new dataset** to validate and train on a CSV before it replaces the active dataset. Failed uploads leave the active dataset in place. The **Retrain models** control refits the current data. The cleaned frame and model pipelines are saved in `saved_models/`; they are regenerated from the active dataset when needed.

Actual records entered in the dashboard and saved prediction snapshots are stored in `data/food_waste_records.sqlite3`. This local SQLite file persists across app restarts in the workspace. Deployment filesystems may not guarantee durable local writes; export records regularly if deployed.

## Features

- Three regressors: Random Forest, Gradient Boosting, and XGBoost.
- Chronological 80/20 evaluation grouped by date, with preprocessing fit only on training rows.
- MAE, RMSE, and R² per model; each model is refit on all available rows for forecasting.
- Separate day, 7-day, and 30-day model forecasts plus an inverse-RMSE-weighted combined estimate.
- Recommendation panel showing the heuristic behind compost/biogas routing and explicit yield assumptions.
- Recorded waste totals for the latest dataset day, trailing seven days, and latest calendar month, alongside the selected forecast and treatment recommendation.
- Dataset totals for meals served, food prepared, total waste, and waste percentage, plus category-level waste analysis.
- Dashboard charts for waste forecasts, category totals, model comparisons, compost/biogas split, moisture, pH, temperature, and meals served.
- Search, filters, date ranges, pagination, CSV export, and CRUD for manually entered actual records.
- Saved prediction history and downloadable CSV performance reports.
- CSV upload validation and model retraining.

## Model and treatment limitations

The training pipeline excludes `waste_level`, `suggested_treatment`, provenance, and other target-derived labels. Imputation and categorical encoding are fitted inside each model pipeline on the training split. Metrics from the bundled synthetic demo dataset are useful only to exercise the workflow; they do not establish accuracy on real operations.

Forecasts are estimates, not guarantees. Treatment recommendations use available dataset averages and transparent planning heuristics. Approximate yield assumptions are 0.10 m³ of biogas per kg routed to digestion and compost mass near 30% of feed mass. Confirm with measured inputs and local treatment conditions.

## API routes

- `GET /api/forecast?period=day|week|month`
- `GET /api/metrics`
- `GET /api/history`
- `GET /api/records` and `GET /api/records/export.csv`
- `POST /api/records`, `PUT /api/records/<id>`, `DELETE /api/records/<id>`
- `POST /api/predictions` and `GET /api/predictions/history`
- `GET /api/reports/performance.csv`
- `POST /api/retrain`
- `POST /upload` (CSV form field: `dataset`)
