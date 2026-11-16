import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_validate

# Same synthetic data as ml_day1.py (planted pattern, NOT real plant data)
rng = np.random.default_rng(42)
n = 2000
df = pd.DataFrame({
    "machine": rng.choice(["Press-A", "Press-B", "Conveyor", "Pump"], n),
    "cause": rng.choice(["electrical", "mechanical", "sensor", "operator"], n),
})
base = 30 + np.where(df["cause"] == "mechanical", 40, 0) + np.where(df["machine"] == "Press-A", 20, 0)
df["downtime_min"] = (base * rng.exponential(1.0, n)).round(1)

X = pd.get_dummies(df[["machine", "cause"]])
y = df["downtime_min"]

cv = KFold(n_splits=10, shuffle=True, random_state=42)
metrics = {"MAE": "neg_mean_absolute_error", "RMSE": "neg_root_mean_squared_error"}

candidates = {
    "baseline median": DummyRegressor(strategy="median"),
    "baseline mean": DummyRegressor(strategy="mean"),
    "forest (squared error)": RandomForestRegressor(
        n_estimators=100, min_samples_leaf=20, random_state=42, n_jobs=-1),
    "forest (absolute error)": RandomForestRegressor(
        n_estimators=100, min_samples_leaf=20, criterion="absolute_error",
        random_state=42, n_jobs=-1),
}

rows = []
for name, estimator in candidates.items():
    res = cross_validate(estimator, X, y, cv=cv, scoring=metrics)
    rows.append({
        "model": name,
        "MAE": round(-res["test_MAE"].mean(), 1),
        "RMSE": round(-res["test_RMSE"].mean(), 1),
    })
print(pd.DataFrame(rows).to_string(index=False))