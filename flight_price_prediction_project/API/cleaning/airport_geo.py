import pandas as pd

FILE = "../datasets/updated_eda.csv"

df = pd.read_csv(FILE)

routes = df.groupby(["origin", "destination"])["distance_km"].unique()

for (origin, destination), distance in routes.items():
    print(f"{origin} -> {destination}: {list(distance)}km")