import os
import time
import json
import pandas as pd
from dotenv import load_dotenv
from amadeus import Client, ResponseError
from datetime import datetime, timedelta
from tqdm import tqdm

load_dotenv()

amadeus = Client(
    client_id=os.getenv("AMADEUS_API_KEY"),
    client_secret=os.getenv("AMADEUS_API_SECRET")
)

# 4 Airports and Routes
airports = ["YOW", "YYZ", "YVR", "YYC"]
routes = [(o, d) for o in airports for d in airports if o != d]

holidays = [
    "2026-01-01",  # New Year's Day
    "2026-12-25",  # Christmas
    "2026-07-01",  # Canada Day
]

# Generate dates for the next 365 days
all_dates = [(datetime.today() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(365)]

# Exclude Sunday=6
weekdays_to_include = [0, 1, 2, 3, 4, 5]

# Filter dates
dates = [d for d in all_dates if datetime.strptime(d, "%Y-%m-%d").weekday() in weekdays_to_include]

# Ensure holidays included
for h in holidays:
    if h not in dates:
        dates.append(h)

# Remove duplicates and sort
dates = sorted(list(set(dates)))

# Output file
OUTPUT_FILE = "flights_dataset.csv"

def parse_duration(duration_str):
    """Convert ISO duration PT#H#M into minutes"""
    if not duration_str:
        return 0
    duration_str = duration_str.replace("PT", "")
    hours = 0
    minutes = 0
    if "H" in duration_str:
        parts = duration_str.split("H")
        hours = int(parts[0])
        duration_str = parts[1] if len(parts) > 1 else ""
    if "M" in duration_str:
        minutes = int(duration_str.replace("M", ""))
    return hours * 60 + minutes

def extract_features(offer, origin, dest, query_date):
    itinerary = offer.get("itineraries", [{}])[0]
    segments = itinerary.get("segments", [])
    if not segments:
        return None

    first_segment = segments[0]
    last_segment = segments[-1]

    departure_time = first_segment["departure"]["at"]
    arrival_time = last_segment["arrival"]["at"]

    duration_minutes = sum(parse_duration(seg.get("duration", "PT0M")) for seg in segments)

    bags = first_segment.get("includedCheckedBags", {})
    cabin_bags = first_segment.get("includedCabinBags", {})

    dep_dt = datetime.strptime(departure_time[:10], "%Y-%m-%d")
    query_dt = datetime.strptime(query_date, "%Y-%m-%d")

    return {
        "origin": origin,
        "destination": dest,
        "query_date": query_date,

        # Time features
        "departure_time": departure_time,
        "arrival_time": arrival_time,
        "day_of_week": dep_dt.weekday(),
        "month": dep_dt.month,
        "days_until_departure": (dep_dt - query_dt).days,

        # Flight info
        "airline": first_segment.get("carrierCode"),
        "aircraft": first_segment.get("aircraft", {}).get("code"),
        "trip_duration_minutes": duration_minutes,
        "number_of_stops": max(len(segments) - 1, 0),

        # Pricing
        "currency": offer.get("price", {}).get("currency"),
        "base_price": float(offer.get("price", {}).get("base", 0)),
        "total_price": float(offer.get("price", {}).get("total", 0)),

        # Demand signals
        "bookable_seats": offer.get("numberOfBookableSeats", 0),

        # Service features
        "checked_bags": bags.get("quantity", 0),
        "cabin_bags": cabin_bags.get("quantity", 0)
    }

# Data Collection
MAX_REQUESTS = 500
request_count = 0
results = []

for origin, dest in tqdm(routes):
    for date in dates:
        if request_count >= MAX_REQUESTS:
            print("Reached max request limit of", MAX_REQUESTS)
            break

        success = False
        attempts = 0

        while not success and attempts < 3:
            try:
                response = amadeus.shopping.flight_offers_search.get(
                    originLocationCode=origin,
                    destinationLocationCode=dest,
                    departureDate=date,
                    adults=1
                )

                request_count += 1

                for offer in response.data:
                    try:
                        feat = extract_features(offer, origin, dest, date)
                        if feat:
                            results.append(feat)
                    except:
                        continue

                success = True

            except ResponseError as error:
                print("API ERROR:", error)
                attempts += 1
                time.sleep(5)

        if len(results) % 100 == 0 and len(results) > 0:
            pd.DataFrame(results).to_csv(
                OUTPUT_FILE,
                mode="a",
                header=not os.path.exists(OUTPUT_FILE),
                index=False
            )
            results = []  # clear memory after saving

        time.sleep(2.5)

    if request_count >= MAX_REQUESTS:
        break

# Final save
if len(results) > 0:
    pd.DataFrame(results).to_csv(
        OUTPUT_FILE,
        mode="a",
        header=not os.path.exists(OUTPUT_FILE),
        index=False
    )

print("Collection complete!!!!! YAYYY")