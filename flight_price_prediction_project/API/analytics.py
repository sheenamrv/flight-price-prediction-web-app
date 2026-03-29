import pandas as pd
from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent
# FILE_NAME = BASE_DIR / "datasets" / "updated_eda.csv"
# FILE_NAME = Path("datasets/updated_eda.csv")
FILE_NAME = Path(__file__).resolve().parent / "datasets" / "updated_eda.csv"

def get_live_analytics(flights):

    prices = []

    for flight in flights:
        price = flight.get("price")

        if price is not None: 
            prices.append(price)

    if len(prices) == 0:
        return {
            "lowest_price" : None,
            "highest_price" : None,
            "average_price" : None, 
            "total_records" : 0
        }

    analytics = {
        "lowest_price": min(prices),
        "highest_price": max(prices),
        "average_price": sum(prices) / len(prices),
        "total_records": len(prices)
    }

    return analytics

def get_hist_analytics(origin, destination):

    if not FILE_NAME.exists():
        raise FileNotFoundError(f"CSV not found at: {FILE_NAME}")

    df = pd.read_csv(FILE_NAME)

    route_df = df[
        (df["origin"] == origin) &
        (df["destination"] == destination)
    ]

    if route_df.empty:
        return {
            "lowest_price" : None,
            "highest_price" : None,
            "average_price" : None, 
            "total_records" : 0
        }
    
    analytics = {
        "lowest_price": route_df["base_price"].min(),
        "highest_price": route_df["base_price"].max(),
        "average_price": route_df["base_price"].mean(),
        "total_records": len(df),
        "filtered_records": len(route_df)
    }

    return analytics