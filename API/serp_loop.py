import requests
import csv
import os
from datetime import datetime, timedelta
from hidden_api import API_KEY

API_KEY 
url = "https://serpapi.com/search"

airports = ["YUL", "YOW", "YVR", "YYC"]

file_name = "serp_dataset.csv"

query_date = datetime.today().strftime("%Y-%m-%d")

# start date
start_departure = datetime(2026, 3, 28)

# number of dates you want
num_dates = 9

departure_dates = [
    (start_departure + timedelta(days=5*i)).strftime("%Y-%m-%d")
    for i in range(num_dates)
]

file_exists = os.path.exists(file_name)

with open(file_name, "a", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    for origin in airports:
        for destination in airports:

            if origin == destination:
                continue

            for dep_date in departure_dates:

                params = {
                    "engine": "google_flights",
                    "departure_id": origin,
                    "arrival_id": destination,
                    "outbound_date": dep_date,
                    "type": "2",
                    "currency": "CAD",
                    "hl": "en",
                    "api_key": API_KEY
                }

                response = requests.get(url, params=params)
                data = response.json()

                # dep_datetime = datetime.strptime(dep_date, "%Y-%m-%d")
                # days_diff = (dep_datetime - query_date).days

                flights = data.get("best_flights", []) + data.get("other_flights", [])

                print(f"\nRoute {origin} → {destination} | Date {dep_date}")
                print("Flights found:", len(flights))

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

print("\nLoop complete. Flights appended to CSV.")