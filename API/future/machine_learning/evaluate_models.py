import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

df = pd.read_csv("../../datasets/future_model.csv")

X = df.drop("base_price", axis=1)
y = df["base_price"]

x_train, x_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42
)

xgb = joblib.load("models/xgboost_model.pkl")
rf = joblib.load("models/random_forest_model.pkl")

results = pd.DataFrame(columns=['Model','Train MAE','Train R2','Test MAE','Test R2'])

def evaluate(model_name, model):

    train_pred = model.predict(x_train)
    test_pred = model.predict(x_test)

    row = {
        'Model':model_name,
        'Train MAE':mean_absolute_error(y_train, train_pred),
        'Train R2':r2_score(y_train, train_pred),
        'Test MAE':mean_absolute_error(y_test, test_pred),
        'Test R2':r2_score(y_test, test_pred)
    }

    return pd.DataFrame(row, index=[0])

results = pd.concat([
    results,
    evaluate("XGBoost", xgb),
    evaluate("Random Forest", rf)
])

print(results)