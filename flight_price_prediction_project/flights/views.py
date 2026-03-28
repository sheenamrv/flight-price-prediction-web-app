import sys
from pathlib import Path
from django.shortcuts import render
from datetime import datetime, date
from API.collector import request_flights, get_time_period, KNOWN_DISTANCES
from .machine_learning.predictor import predict_price

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

def build_pipeline_input(origin, destination, flight):
    segments = flight.get("flights", [])
    if not segments:
        return None

    first = segments[0]
    last = segments[-1]

    dep_time = first.get("departure_airport", {}).get("time")
    arr_time = last.get("arrival_airport", {}).get("time")

    if not dep_time or not arr_time:
        return None

    dep_dt = datetime.fromisoformat(dep_time)
    arr_dt = datetime.fromisoformat(arr_time)

    distance_km = KNOWN_DISTANCES.get((origin, destination))
    if distance_km is None:
        return None

    return {
        "origin": origin,
        "destination": destination,
        "name_airline": first.get("airline", ""),
        "departure_date": dep_dt.date(),
        "distance_km": distance_km,
        "days_until_departure": max((dep_dt.date() - date.today()).days, 0),
        "trip_duration_minutes": int(flight.get("total_duration", 0) or 0),
        "number_of_stops": max(len(segments) - 1, 0),
        "departure_hour": dep_dt.hour,
        "arrival_hour": arr_dt.hour,
        "departure_time_period": get_time_period(dep_dt.hour),
        "arrival_time_period": get_time_period(arr_dt.hour),
    }

def collect_result_data(origin, destination, flight, predicted_price=None):
    segments = flight.get("flights", [])
    if not segments:
        return None

    first = segments[0]
    last = segments[-1]

    dep_time = first.get("departure_airport", {}).get("time")
    arr_time = last.get("arrival_airport", {}).get("time")

    if not dep_time or not arr_time:
        return None

    dep_dt = datetime.fromisoformat(dep_time)
    arr_dt = datetime.fromisoformat(arr_time)

    total_duration = int(flight.get("total_duration", 0) or 0)
    hours = total_duration // 60
    minutes = total_duration % 60

    if hours > 0:
        duration_label = f"{hours}h {minutes}m"
    else:
        duration_label = f"{minutes}m"

    stops = max(len(segments) - 1, 0)
    if stops == 0:
        stops_label = "Non-stop"
    elif stops == 1:
        stops_label = "1 Stop"
    else:
        stops_label = f"{stops} Stops"

    return {
        "airline": first.get("airline", ""),
        "origin": origin,
        "destination": destination,
        "departure_time": dep_dt.strftime("%H:%M"),
        "arrival_time": arr_dt.strftime("%H:%M"),
        "duration_label": duration_label,
        "stops_label": stops_label,
        "api_price": flight.get("price"),
        "predicted_price": predicted_price,
    }

# PAGES
# For landing/home page
def landing_page(request):
    return render(request, "flights/landing_page.html")

# For flights search page
def flights_search_page(request):
    results = []
    predicted_price = None
    error = None

    if request.method == "POST":
        origin = (request.POST.get("origin") or "").strip().upper()
        destination = (request.POST.get("destination") or "").strip().upper()
        departure_date = (request.POST.get("departure_date") or "").strip()

        if not origin or not destination or not departure_date:
            error = "Please fill out all fields."
        elif origin == destination:
            error = "Origin and destination must be different."
        else:
            try:
                flights = request_flights(origin, destination, departure_date)

                if flights:
                    first_flight = flights[0]
                    model_input = build_pipeline_input(origin, destination, first_flight)

                    if model_input:
                        predicted_price = predict_price(**model_input)

                for index, flight in enumerate(flights):
                    card = collect_result_data(
                        origin = origin,
                        destination = destination,
                        flight = flight,
                        predicted_price = predicted_price if index == 0 else None,
                    )
                    if card:
                        results.append(card)

            except Exception as e:
                error = str(e)

    return render(
        request,
        "flights/flights_search_page.html",
        {
            "results": results,
            "predicted_price": predicted_price,
            "error": error,
        },
    )
    