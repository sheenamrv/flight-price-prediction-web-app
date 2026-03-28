import pandas as pd

INPUT_FILE = "../datasets/future_updated_eda.csv"
OUTPUT_FILE = "../datasets/future_model.csv"

df = pd.read_csv(INPUT_FILE)

# Feature engineering
df['is_weekend_departure'] = df['day_of_week_departure'].isin(
['Saturday', 'Sunday']
).astype(int)

df['season'] = df['month_departure'].apply(
    lambda m: 'Winter' if m in [12,1,2]
    else 'Spring' if m in [3,4,5] 
    else 'Summer' if m in [6,7,8] 
    else 'Fall'
)

    # Select columns
df2 = df.loc[:,[
    'base_price',
    'origin',
    'destination', 
    'Name_airline', 
    'day_of_week_departure', 
    'days_until_departure',
    'trip_duration_minutes', 
    'number_of_stops',
    'departure_hour', 
    'arrival_hour', 
    'departure_time_period',
    'arrival_time_period', 
    'is_weekend_departure',
    'season']]

    # Get Dummies
df3 = pd.get_dummies(df2, columns = [
    'origin', 
    'destination', 
    'Name_airline', 
    'day_of_week_departure',
    'departure_time_period', 
    'arrival_time_period', 
    'season'], drop_first=True).astype(int)

df3.to_csv(OUTPUT_FILE, index=False)
    #return df3

# def engineer_prediction_features(df):

#     # ensure departure_date is datetime
#     df['departure_date'] = pd.to_datetime(df['departure_date'])

#     # create missing columns used in training
#     df['day_of_week_departure'] = df['departure_date'].dt.day_name()

#     df['month_departure'] = df['departure_date'].dt.month
    
#     # recreate features that training data had
#     df['is_weekend_departure'] = df['day_of_week_departure'].isin(
#         ['Saturday', 'Sunday']
#     ).astype(int)

#     df['season'] = df['month_departure'].apply(
#         lambda m: 'Winter' if m in [12,1,2]
#         else 'Spring' if m in [3,4,5]
#         else 'Summer' if m in [6,7,8]
#         else 'Fall'
#     )

#     df2 = df.loc[:,[
#         'origin',
#         'destination',
#         'distance_km',
#         'Name_airline',
#         'day_of_week_departure',
#         'days_until_departure',
#         'trip_duration_minutes',
#         'number_of_stops',
#         'departure_hour',
#         'arrival_hour',
#         'departure_time_period',
#         'arrival_time_period',
#         'is_weekend_departure',
#         'season'
#     ]]

#     df3 = pd.get_dummies(
#         df2,
#         columns=[
#             'origin',
#             'destination',
#             'Name_airline',
#             'day_of_week_departure',
#             'departure_time_period',
#             'arrival_time_period',
#             'season'
#         ],
#         drop_first=True
#     )

#     return df3