from collector import request_flights, save_flights
from analytics import get_live_analytics, get_hist_analytics

origin = input("Origin airport: ").upper()
destination = input("Destination airport: ").upper()
departure_date = input("Departure date (YYYY-MM-DD): ")

# Collect new API data
flights = request_flights(origin, destination, departure_date)

# Get Analytics of live data
live_stats = get_live_analytics(flights)

# Save historical data
save_flights(origin, destination, departure_date, flights)

# Get Analytics for historical data
hist_stats = get_hist_analytics(origin, destination)

print("Flights saved to dataset.")


print("\nAnalytics (Live API Results)")
print("Lowest Price:", live_stats["lowest_price"])
print("Highest Price:", live_stats["highest_price"])
print("Average Price:", live_stats["average_price"])
print("Total Records:", live_stats["total_records"])

print("---------")

print("\nAnalytics (Historical Results)")
print("Lowest Price:", hist_stats["lowest_price"])
print("Highest Price:", hist_stats["highest_price"])
print("Average Price:", hist_stats["average_price"])
print("Total Records:", hist_stats["total_records"])
print("Filtered Records (Origin, Destination):", hist_stats["filtered_records"])