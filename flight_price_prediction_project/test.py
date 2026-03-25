from datetime import date
from flights.machine_learning.predictor import predict_price

result = predict_price(
    origin="YOW",
    destination="YYZ",
    name_airline="Air Canada",
    departure_date=date(2026, 6, 10),
    distance_km=400,
    days_until_departure=30,
    trip_duration_minutes=90,
    number_of_stops=0,
    departure_time_period="Morning",
    arrival_time_period="Afternoon",
)

print("Predicted price:", result)