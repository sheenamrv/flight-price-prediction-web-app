import sys
from pathlib import Path
from django.shortcuts import render
from datetime import datetime, date

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

from API.collector import request_flights, get_time_period
from API.analytics import get_live_analytics, get_hist_analytics
from .machine_learning.predictor import predict_price

# TO DO : Store MAE with model and add in predictor.py
MODEL_MAE = 36.6

# Build the ML model input
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

    return {
        "origin": origin,
        "destination": destination,
        "name_airline": first.get("airline", ""),
        "departure_date": dep_dt.date(),
        "days_until_departure": max((dep_dt.date() - date.today()).days, 0),
        "trip_duration_minutes": int(flight.get("total_duration", 0) or 0),
        "number_of_stops": max(len(segments) - 1, 0),
        "departure_hour": dep_dt.hour,
        "arrival_hour": arr_dt.hour,
        "departure_time_period": get_time_period(dep_dt.hour),
        "arrival_time_period": get_time_period(arr_dt.hour),
    }

# Build the UI display data
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
    first_predicted_price = None
    error = None
    live_stats = None
    hist_stats = None
    origin = None
    destination = None
    suggestion_message = None


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
                departure_date_obj = datetime.strptime(departure_date, "%Y-%m-%d").date()

                if departure_date_obj < date.today():
                    error = "Departure date cannot be before today."
                else:
                    flights = request_flights(origin, destination, departure_date)

                    live_stats = get_live_analytics(flights)
                    hist_stats = get_hist_analytics(origin, destination)

                    # if flights:
                    #     first_flight = flights[0]
                    #     model_input = build_pipeline_input(origin, destination, first_flight)

                    #     if model_input:
                    #         predicted_price = predict_price(**model_input)

                    for flight in flights:
                        model_input = build_pipeline_input(origin, destination, flight)
                        predicted_price = None

                        if model_input:
                            predicted_price = predict_price(**model_input)

                            if flight == flights[0]:
                                first_predicted_price = predicted_price

                        card = collect_result_data(
                            origin=origin,
                            destination=destination,
                            flight=flight,
                            predicted_price=predicted_price,
                        )

                        if card:
                            results.append(card)

                    suggestion_message = None

                    if live_stats and first_predicted_price is not None:
                        current_price = live_stats.get("lowest_price")
                        historical_avg = hist_stats.get("average_price") if hist_stats else None
                        

                        if current_price is not None:
                            diff = current_price - first_predicted_price

                            if abs(diff) <= MODEL_MAE:
                                suggestion_message = f"The current price of the cheapest flight (${current_price:.2f}) is close to the predicted value (${first_predicted_price:.2f} ± ${MODEL_MAE:.2f}), which is within the model’s typical range, so there is no strong indication that the price is unusually high or low and booking now would be reasonable, though waiting may not lead to a significantly better price."

                            elif diff < 0:
                                suggestion_message = f"The current price of the cheapest flight (${current_price:.2f}) is ${abs(diff):.2f} below the predicted value (${first_predicted_price:.2f}), which is beyond the model’s typical range and suggests the price is relatively low, making this a good opportunity to book."

                            else:
                                suggestion_message = f"The current price of the cheapest flight (${current_price:.2f}) is ${diff:.2f} above the predicted value (${first_predicted_price:.2f}), which is higher than expected and may indicate relatively high pricing, so it could be worth monitoring before booking."

                            if historical_avg is not None:
                                if current_price < historical_avg:
                                    suggestion_message += f" It is also below the historical average (${historical_avg:.2f}), reinforcing that this is a favorable price."
                                elif current_price > historical_avg:
                                    suggestion_message += f" It is also above the historical average (${historical_avg:.2f}), suggesting it may not be the most competitive price."


                    # for flight in flights:
                    #     card = collect_result_data(
                    #         origin=origin,
                    #         destination=destination,
                    #         flight=flight,
                    #     )
                    #     if card:
                    #         results.append(card)

            except ValueError:
                error = "Please enter a valid departure date."
            except Exception as e:
                error = str(e)

    return render(
        request,
        "flights/flights_search_page.html",
        {
            "origin": origin,
            "destination": destination,
            "results": results,
            "predicted_price": first_predicted_price,
            "live_stats": live_stats,
            "hist_stats": hist_stats,
            "mae": MODEL_MAE,
            "suggestion_message": suggestion_message,
            "error": error,
        },
    )