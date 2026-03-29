import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, r2_score
# from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv("../model_building/flights_eda_df.csv")

# Feature Engineering
df["is_weekend_departure"] = df["day_of_week_departure"].isin(["Saturday", "Sunday"]).astype(int)

df["route"] = df["origin"] + '-' + df["destination"]

df["season"] = df["month_departure"].apply(
    lambda m: (
        "Winter" if m in [12, 1, 2]
        else "Spring" if m in [3, 4, 5]
        else "Summer" if m in [6, 7, 8]
        else "Fall"
    )
)

# df["days_until_departure_group"] = pd.cut(
#     df["days_until_departure"],
#     bins=[-1, 50, 100, 150, 200, 250, 300, 350, float("inf")],
#     labels=[
#         "0-50 days","51-100 days","101-150 days","151-200 days",
#         "200-250 days","251-300 days","301-350 days","350+ days"
#     ],
# )

# df["airline_route"] = (
#     df["Name_airline"] + "_" + df["origin"] + "-" + df["destination"]
# )

# df["distance_bin"] = pd.cut(
#     df["distance_km"],
#     bins=[-1, 500, 1000, 1500, 2000, 2500, 3000, 3500, float("inf")],
#     labels=[
#         "0-500 km","501-1000 km","1001-1500 km","1501-2000 km",
#         "2001-2500 km","2501-3000 km","3001-3500 km","3500+ km"
#     ],
# )

# Features
features = [
    "origin", "destination", "Name_airline",
    "day_of_week_departure", "days_until_departure",
    "trip_duration_minutes", "number_of_stops",
    "departure_hour", "arrival_hour",
    "departure_time_period", "arrival_time_period",
    "is_weekend_departure", "season", "route"
    # "days_until_departure_group","airline_route","distance_bin"
]

target = "base_price"
X = df[features]
y = df[target]

# Columns (from get_dummies columns)
categorical = [
    "origin", "destination", "Name_airline",
    "day_of_week_departure", "departure_time_period",
    "arrival_time_period", "season", "route"
    # "days_until_departure_group", "distance_bin", "airline_route"
]

numeric = [
    "days_until_departure",
    "trip_duration_minutes", "number_of_stops",
    "departure_hour", "arrival_hour",
    "is_weekend_departure"
]

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore", drop="first"), categorical),
    ("num", "passthrough", numeric)
])

# Model
# model = XGBRegressor(
#     objective="reg:squarederror",
#     n_estimators=150,
#     max_depth=6,
#     learning_rate=0.1,
#     subsample=0.7,
#     colsample_bytree=0.7,
#     random_state=42
# )
rf = RandomForestRegressor(
    random_state=42,
    n_jobs=-1
)

# Pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", rf)
])

# Params
cv_params = {
    "model__n_estimators": [100, 200],
    "model__max_depth": [10, 15, 20],
    "model__min_samples_split": [10, 20],
    "model__min_samples_leaf": [5, 10],
    "model__max_features": ["sqrt", 0.5],
}

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

grid_search = GridSearchCV(
    estimator=pipeline,
    param_grid=cv_params,
    cv=5,
    scoring="neg_mean_absolute_error",
    refit=True,
    n_jobs=-1,
    verbose=1
)

# Train
grid_search.fit(X_train, y_train)

best_pipeline = grid_search.best_estimator_

# Evaluate
train_pred = best_pipeline.predict(X_train)
test_pred = best_pipeline.predict(X_test)

print("Best Params:", grid_search.best_params_)
print("Best CV Score:", grid_search.best_score_)
print("Train MAE:", mean_absolute_error(y_train, train_pred))
print("Train R2:", r2_score(y_train, train_pred))
print("Test MAE:", mean_absolute_error(y_test, test_pred))
print("Test R2:", r2_score(y_test, test_pred))

# Save model
joblib.dump(
    best_pipeline,
    "../flight_price_prediction_project/flights/machine_learning/flight_price_pipeline.pkl"
)

print("Pipeline saved!!!!!!!!!!")