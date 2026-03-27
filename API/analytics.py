import pandas as pd

FILE_NAME = "serp_dataset.csv"

def get_analytics():

    df = pd.read_csv(FILE_NAME)

    analytics = {
        "lowest_price": df["price"].min(),
        "highest_price": df["price"].max(),
        "average_price": df["price"].mean(),
        "total_records": len(df)
    }

    return analytics