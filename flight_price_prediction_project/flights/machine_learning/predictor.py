from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "flight_price_pipeline.pkl" # The pipeline produced

pipeline = joblib.load(MODEL_PATH)

# Based on previous feature engineering 
def get_season(month: int) -> str:
    if month in [12, 1, 2]:
        return "Winter"
    if month in [3, 4, 5]:
        return "Spring"
    if month in [6, 7, 8]:
        return "Summer"
    return "Fall"

# def get_days_until_departure_group(days: int) -> str:
#     if days <= 50:
#         return "0-50 days"
#     if days <= 100:
#         return "51-100 days"
#     if days <= 150:
#         return "101-150 days"
#     if days <= 200:
#         return "151-200 days"
#     if days <= 250:
#         return "200-250 days"
#     if days <= 300:
#         return "251-300 days"
#     if days <= 350:
#         return "301-350 days"
#     return "350+ days"

# def get_distance_bin(distance: float) -> str:
#     if distance <= 500:
#         return "0-500 km"
#     if distance <= 1000:
#         return "501-1000 km"
#     if distance <= 1500:
#         return "1001-1500 km"
#     if distance <= 2000:
#         return "1501-2000 km"
#     if distance <= 2500:
#         return "2001-2500 km"
#     if distance <= 3000:
#         return "2501-3000 km"
#     if distance <= 3500:
#         return "3001-3500 km"
#     return "3500+ km"

# Generate a flight price prediction
def predict_price(origin: str, destination: str, name_airline: str, departure_date, days_until_departure: int, trip_duration_minutes: int, number_of_stops: int, departure_hour: int, arrival_hour: int, departure_time_period: str, arrival_time_period: str) -> float:
    
    # Prep data 
    origin = origin.upper().strip()
    destination = destination.upper().strip()
    route = f"{origin}-{destination}"
    name_airline = name_airline.strip()

    # Convert date if needed
    if isinstance(departure_date, str):
        departure_date = pd.to_datetime(departure_date) 

    day_of_week_departure = departure_date.strftime("%A")
    is_weekend_departure = int(day_of_week_departure in ["Saturday", "Sunday"])
    season = get_season(departure_date.month)
    # days_until_departure_group = get_days_until_departure_group(days_until_departure)
    # distance_bin = get_distance_bin(distance_km)
    # airline_route = f"{name_airline}_{origin}-{destination}"

    input_df = pd.DataFrame([{
        "origin": origin,
        "destination": destination,
        "route": route,
        "Name_airline": name_airline,
        "day_of_week_departure": day_of_week_departure,
        "days_until_departure": int(days_until_departure),
        "trip_duration_minutes": int(trip_duration_minutes),
        "number_of_stops": int(number_of_stops),
        "departure_hour": int(departure_hour),
        "arrival_hour": int(arrival_hour),
        "departure_time_period": departure_time_period,
        "arrival_time_period": arrival_time_period,
        "is_weekend_departure": is_weekend_departure,
        "season": season,
        # "days_until_departure_group": days_until_departure_group,
        # "airline_route": airline_route,
        # "distance_bin": distance_bin,
    }])

    # Predict the price
    prediction = pipeline.predict(input_df)[0]
    price_prediction = round(float(prediction),2)

    return price_prediction