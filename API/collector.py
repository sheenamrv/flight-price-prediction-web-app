import requests
import csv
import os
from datetime import datetime
from hidden_api import API_KEY

API_KEY
URL = "https://serpapi.com/search"
FILE_NAME = "serp_dataset.csv"


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
                "destination",
                "query_date",
                "departure_datetime",
                "arrival_datetime",
                "airline",
                "flight_number",
                "stops",
                "duration",
                "price"
            ])

        for flight in flights:

            first_segment = flight["flights"][0]
            last_segment = flight["flights"][-1]

            airline = first_segment["airline"]
            flight_number = first_segment["flight_number"]

            departure_datetime = first_segment.get("departure_airport", {}).get("time", "")
            arrival_datetime = last_segment.get("arrival_airport", {}).get("time", "")

            duration = flight.get("total_duration", "")
            price = flight.get("price", "")
            stops = len(flight["flights"]) - 1

            writer.writerow([
                origin,
                destination,
                query_date,
                departure_datetime,
                arrival_datetime,
                airline,
                flight_number,
                stops,
                duration,
                price
            ])