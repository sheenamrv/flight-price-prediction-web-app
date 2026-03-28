import pandas as pd
import joblib
import sys
import os
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from future_engineering import engineer_training_features

df = pd.read_csv("../../datasets/future_model.csv")
# df = engineer_training_features(df)

x = df.drop("base_price", axis=1)
y = df["base_price"]

joblib.dump(x.columns.tolist(), "models/model_features.pkl")

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    test_size=0.3,
    random_state=42
)

xgb = XGBRegressor(random_state=0)

cv_params = {
    'max_depth': [4,6],
    'min_child_weight': [3,5],
    'learning_rate': [0.1,0.2,0.3],
    'n_estimators': [50,100,150],
    'subsample':[0.7],
    'colsample_bytree':[0.7]
}

xgb_cv = GridSearchCV(xgb, cv_params)

xgb_cv.fit(x_train, y_train)

best_model = xgb_cv.best_estimator_

print("Best params:", xgb_cv.best_params_)

train_pred = best_model.predict(x_train)
test_pred = best_model.predict(x_test)

print("Training MAE:", mean_absolute_error(y_train, train_pred))
print("Training R2:", r2_score(y_train, train_pred))
print("Test MAE:", mean_absolute_error(y_test, test_pred))
print("Test R2:", r2_score(y_test, test_pred))

joblib.dump(best_model, "models/xgboost_model.pkl")

# Save training columns
# joblib.dump(x.columns.tolist(), "models/xgboost_columns.pkl")

print("XGBoost model saved")