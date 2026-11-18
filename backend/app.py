from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import date, datetime
import pandas as pd
import joblib

app = FastAPI()

# Allow your friend's frontend website to connect without CORS errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Print exact details in the terminal whenever the frontend sends mismatched fields (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    raw_body = await request.body()
    print("\n================ 422 VALIDATION ERROR ================")
    print("RAW DATA SENT BY FRIEND'S WEBSITE:", raw_body.decode("utf-8", errors="ignore"))
    print("WHAT FASTAPI EXPECTED vs RECEIVED:", exc.errors())
    print("======================================================\n")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

# Load your exported model and column names once when the server starts
model = joblib.load("aerofare_model.joblib")
model_columns = joblib.load("model_columns.joblib")

ALL_AIRLINES = ["Air_India", "AirAsia", "GO_FIRST", "IndiGo", "SpiceJet", "Vistara"]

# Define the input structure expected from the website
class FlightSearch(BaseModel):
    airline: str
    source_city: str
    destination_city: str
    departure_time: str = "Morning"
    arrival_time: str = "Evening"
    flight_class: str = "Economy"   # "Economy" or "Business"
    stops_num: int = 0              # 0, 1, or 2
    duration_mins: int = 140
    travel_date: str                # Format: "YYYY-MM-DD"

def predict_price_for_row(row_dict: dict) -> float:
    df = pd.DataFrame([row_dict])
    df_encoded = pd.get_dummies(df)
    df_encoded = df_encoded.reindex(columns=model_columns, fill_value=0)
    return round(float(model.predict(df_encoded)[0]), 2)

@app.get("/")
def home():
    return {"status": "AeroFare ML API is running!"}

@app.post("/predict")
def predict_fare(search: FlightSearch):
    print("\n>>> VALID REQUEST RECEIVED:", search.model_dump())

    # 1. Automatically calculate days_left from today's date
    travel_dt = datetime.strptime(search.travel_date, "%Y-%m-%d").date()
    days_left = max(1, (travel_dt - date.today()).days)

    base_input = {
        "airline": search.airline,
        "source_city": search.source_city,
        "destination_city": search.destination_city,
        "departure_time": search.departure_time,
        "arrival_time": search.arrival_time,
        "class": search.flight_class,
        "stops_num": search.stops_num,
        "duration_mins": search.duration_mins,
        "days_left": days_left,
    }

    # 2. Predict price for the user's chosen flight
    predicted_price = predict_price_for_row(base_input)

    # 3. Predict prices for all 6 airlines (for the comparison bar chart)
    airline_comparison = []
    for airline_name in ALL_AIRLINES:
        temp = base_input.copy()
        temp["airline"] = airline_name
        airline_comparison.append({
            "airline": airline_name.replace("_", " "),
            "price": predict_price_for_row(temp)
        })
    airline_comparison.sort(key=lambda x: x["price"])

    # 4. Predict booking window trend (1 to 45 days ahead)
    booking_trend = []
    for d in [1, 3, 7, 14, 21, 30, 45]:
        temp = base_input.copy()
        temp["days_left"] = d
        booking_trend.append({
            "days_left": d,
            "price": predict_price_for_row(temp)
        })

    return {
        "predicted_price": predicted_price,
        "days_left_calculated": days_left,
        "airline_comparison": airline_comparison,
        "booking_trend": booking_trend
    }