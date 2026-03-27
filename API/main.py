from collector import request_flights, save_flights
from analytics import get_analytics

origin = input("Origin airport: ").upper()
destination = input("Destination airport: ").upper()
departure_date = input("Departure date (YYYY-MM-DD): ")

# Collect new API data
flights = request_flights(origin, destination, departure_date)

# Save historical data
save_flights(origin, destination, departure_date, flights)

print("Flights saved to dataset.")

# Get analytics
stats = get_analytics()

print("\nAnalytics")
print("Lowest Price:", stats["lowest_price"])
print("Highest Price:", stats["highest_price"])
print("Average Price:", stats["average_price"])
print("Total Records:", stats["total_records"])