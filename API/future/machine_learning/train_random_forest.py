import pandas as pd
import joblib
# from future_engineering import engineer_training_features
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.read_csv("../../datasets/future_model.csv")
# df = engineer_training_features(df)

x = df.drop("base_price", axis=1)
y = df["base_price"]

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    test_size=0.3,
    random_state=42
)

rf = RandomForestRegressor(random_state=42, n_jobs=-1)

cv_params = {
    'n_estimators':[100,200],
    'max_depth':[10,15,20],
    'min_samples_split':[10,20],
    'min_samples_leaf':[5,10],
    'max_features':['sqrt',0.5]
}

rf_cv = GridSearchCV(
    rf,
    cv_params,
    cv=5,
    scoring='r2',
    refit=True,
    n_jobs=-1
)

rf_cv.fit(x_train, y_train)

best_rf = rf_cv.best_estimator_

print("Best params:", rf_cv.best_params_)

train_pred = best_rf.predict(x_train)
test_pred = best_rf.predict(x_test)

print("Training MAE:", mean_absolute_error(y_train, train_pred))
print("Training R2:", r2_score(y_train, train_pred))
print("Test MAE:", mean_absolute_error(y_test, test_pred))
print("Test R2:", r2_score(y_test, test_pred))

joblib.dump(best_rf, "models/random_forest_model.pkl")
joblib.dump(x.columns.tolist(), "models/random_forest_columns.pkl")

print("Random Forest model saved")