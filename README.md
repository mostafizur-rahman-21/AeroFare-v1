# ✈️ AeroFare — Flight Ticket Price Prediction & Booking Trend Analyzer

An end-to-end machine learning web prototype that estimates Indian domestic flight ticket fares based on historical booking records and visualizes cross-airline pricing and advance-booking trends.

> **Academic Prototype Disclaimer:** AeroFare is an academic prototype trained on historical flight data (`Clean_Dataset.csv`). All outputs represent estimated fares based on past patterns and do not connect to live airline pricing engines, real-time seat inventory, or official ticket quotes.

---

## 👥 Team K — Scholars Institute of Technology and Management

* **Project Window:** 16–20 November 2026 *(Development: 16–18 Nov | Presentations: 19–20 Nov)*
* **Mostafizur Rahman** *(Team Leader)* — Data Preprocessing, Random Forest ML Model, FastAPI Backend & Tunnel Deployment
* **Mahammad Ashif** — Frontend Webpage & Chart.js Visualizations
* **Mountain Brahma** — Frontend Architecture & Styling
* **Ruhan e Farhad** — Sample Testing & Quality Assurance
* **Parag Jyoti Borah** — Dataset Documentation, PRD & Presentation

---

## 🎯 Core & Optional Features

### Core Features

* **Flight Fare Estimator:** Predicts estimated historical fares in Indian Rupees (`₹`) from itinerary inputs (`airline`, `source_city`, `destination_city`, `departure_time`, `arrival_time`, `flight_class`, `stops_num`, `duration_mins`, and `travel_date`).
* **Automated Lead-Time Calculation:** Converts the user's `travel_date` (`YYYY-MM-DD`) into `days_left` dynamically on the backend.
* **Trained Random Forest Model:** Powered by `scikit-learn` (`RandomForestRegressor`), achieving a holdout test Mean Absolute Error (MAE) of **~₹1,084.95** across 29 one-hot encoded features.

### Optional / Visual Enhancements

* **All-Airline Comparison Chart:** Interactive Chart.js bar chart comparing estimated fares across all 6 domestic carriers (`AirAsia`, `SpiceJet`, `IndiGo`, `GO_FIRST`, `Air_India`, `Vistara`).
* **Booking Window Trend Chart:** Interactive Chart.js line chart illustrating price changes from `1` to `45` days in advance.
* **UI & Connectivity Extras:** Glassmorphism UI with Light/Dark theme toggle, 1–9 passenger multiplier, 12-language UI switcher, configurable backend URL box, and Cloudflare Quick Tunnel (`cloudflared`) HTTPS support.

---

## 🛠️ Tech Stack

* **Machine Learning:** Python 3, `scikit-learn` (`RandomForestRegressor`), `pandas`, `numpy`, `joblib`
* **Backend API:** FastAPI, Uvicorn, Pydantic v2
* **Frontend:** HTML5, Vanilla CSS3, Vanilla JavaScript (ES6+), Chart.js
* **Dataset:** [Kaggle — Flight Price Prediction Dataset](https://www.kaggle.com/datasets/shubhambathwal/flight-price-prediction) (`CC0: Public Domain`, target column: `price`)

---

## 📂 Repository Structure

```text
AeroFare/
├── backend/
│   ├── app.py                  # FastAPI REST API server (GET /, POST /predict)
│   ├── aerofare_model.joblib   # Serialized Random Forest Regressor
│   ├── model_columns.joblib    # Ordered list of 29 training feature columns
│   └── requirements.txt        # Python backend dependencies
├── ml/
│   └── aerofare_model.ipynb    # EDA, preprocessing, model training & holdout test MAE
├── frontend/
│   ├── index.html              # Single-file HTML5/CSS3/JS web interface
│   └── logo.png                # AeroFare project logo
└── docs/
    └── AeroFare_Team_K_PRD.docx
```
