import requests
import csv
import os
from datetime import datetime
from hidden_api import API_KEY

API_KEY
URL = "https://serpapi.com/search"
FILE_NAME = "../datasets/future_updated_eda.csv"

# Location metadata
AIRPORT_DATA = {
    "YOW": {"city": "Ottawa"},
    "YYZ": {"city": "Toronto"},
    "YVR": {"city": "Vancouver"},
    "YYC": {"city": "Calgary"}
}

def get_time_period(h):
    if 0 <= h < 5:
        return 'Night'
    if 5 <= h < 8:
        return 'Early Morning'
    if 8 <= h < 12:
        return 'Morning'
    if 12 <= h < 17:
        return 'Afternoon'
    if 17 <= h < 21:
        return 'Evening'
    return 'Late Evening'

def request_flights(origin, destination, departure_date):

    params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date": departure_date,
        "type": "2",
        "currency": "CAD",
        "hl": "en",
        "api_key": API_KEY
    }

    response = requests.get(URL, params=params)
    data = response.json()

    flights = data.get("best_flights", []) + data.get("other_flights", [])
    return flights


def save_flights(origin, destination, departure_date, flights):

    query_date = datetime.today().strftime("%Y-%m-%d")

    file_exists = os.path.exists(FILE_NAME)

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "origin",
                "City",
                "destination",
                "City_destination",
                "Name_airline",
                "query_date",
                "departure_date",
                "departure_clock_time",
                "day_of_week_departure",
                "month_departure",
                "arrival_date",
                "arrival_clock_time",
                "days_until_departure",
                "trip_duration_minutes",
                "number_of_stops",
                "base_price",
                "departure_hour",
                "arrival_hour",
                "departure_time_period",
                "arrival_time_period"
            ])

        for flight in flights:

            segments = flight["flights"]

            first = segments[0]
            last = segments[-1]

            airline = first.get("airline", "")

            dep_time = first["departure_airport"]["time"]
            arr_time = last["arrival_airport"]["time"]

            dep_dt = datetime.fromisoformat(dep_time)
            arr_dt = datetime.fromisoformat(arr_time)

            departure_hour = dep_dt.hour
            arrival_hour = arr_dt.hour

            query_date = datetime.today().date()

            duration = flight.get("total_duration", 0)

            writer.writerow([
                origin,
                AIRPORT_DATA[origin]["city"],
                destination,
                AIRPORT_DATA[destination]["city"],
                airline,
                query_date,
                dep_dt.date(),
                dep_dt.time(),
                dep_dt.strftime("%A"),
                dep_dt.month,
                arr_dt.date(),
                arr_dt.time(),
                (dep_dt.date() - query_date).days,
                duration,
                len(segments) - 1,
                flight.get("price", ""),
                departure_hour,
                arrival_hour,
                get_time_period(departure_hour),
                get_time_period(arrival_hour)
            ])