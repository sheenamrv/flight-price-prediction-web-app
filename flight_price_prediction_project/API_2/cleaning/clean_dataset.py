import pandas as pd

INPUT_FILE = "../../model_building/flights_eda_df.csv"
OUTPUT_FILE = "../datasets/updated_eda.csv"

DROP_AIRLINES = [
    "Air North Yukon's Airline",
    "Central Mountain Air LTD",
    "Pacific Coastal Airlines Limited",
    "Air Transat"
]

RENAME_AIRLINES = {
    "Porter Airlines Canada Limited": "Porter Airlines",
    "WestJet ": "WestJet" 
}

def clean_dataset():
    df = pd.read_csv(INPUT_FILE)

    # df.columns = df.columns.str.stip()

    if "Name_airline" in df.columns:
        df["Name_airline"] = df["Name_airline"].str.strip()

    # Rename the airlines
    df["Name_airline"] = df["Name_airline"].replace(RENAME_AIRLINES)

    # Drop unwanted airlines
    df = df[~df["Name_airline"].isin(DROP_AIRLINES)]

    if "bookable_seats" in df.columns:
        df = df.drop(column=["bookable_seats"])

    if "duration_group" in df.columns:
        df = df.drop(columns=["duration_group"])

    if "distance_km" in df.columns:
        df["distance_km"] = df["distance_km"].round().astype(int)

    if "aircraft" in df.columns:
        df = df.drop(columns=["aircraft"])

    df.to_csv(OUTPUT_FILE, index=False)

    print("Clean EDA dataset saved!")

if __name__ == "__main__":
    clean_dataset()