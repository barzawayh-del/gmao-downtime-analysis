import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

# 1. Synthetic data with a planted pattern (NOT real plant data)
rng = np.random.default_rng(42)
n = 2000
df = pd.DataFrame({
    "machine": rng.choice(["Press-A", "Press-B", "Conveyor", "Pump"], n),
    "cause": rng.choice(["electrical", "mechanical", "sensor", "operator"], n),
})
base = 30 + np.where(df["cause"] == "mechanical", 40, 0) + np.where(df["machine"] == "Press-A", 20, 0)
df["downtime_min"] = (base * rng.exponential(1.0, n)).round(1)

# 2. Features (text -> 0/1 columns) and target
X = pd.get_dummies(df[["machine", "cause"]])
y = df["downtime_min"]

# 3. Hold out 25% of rows that the model never sees during training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# 4. Baseline: always predict the training mean
baseline_pred = np.full(len(y_test), y_train.mean())
baseline_mae = mean_absolute_error(y_test, baseline_pred)

# 5. Model
model = RandomForestRegressor(n_estimators=200, min_samples_leaf=20, random_state=42)
model.fit(X_train, y_train)
model_mae = mean_absolute_error(y_test, model.predict(X_test))

print("Rows: train", len(X_train), "| test", len(X_test))
print("Baseline MAE (min):", round(baseline_mae, 1))
print("Model MAE (min):   ", round(model_mae, 1))

importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nFeature importance:\n", importance.round(3))
median_pred = np.full(len(y_test), y_train.median())
median_mae = mean_absolute_error(y_test, median_pred)
print("Median baseline MAE (min):", round(median_mae, 1))
# Sanity test: destroy the pattern by shuffling the target
y_shuf = pd.Series(rng.permutation(y.to_numpy()), index=y.index)
Xs_train, Xs_test, ys_train, ys_test = train_test_split(X, y_shuf, test_size=0.25, random_state=42)
shuf_model = RandomForestRegressor(n_estimators=200, min_samples_leaf=20, random_state=42)
shuf_model.fit(Xs_train, ys_train)

print("\nShuffled baseline MAE:", round(mean_absolute_error(ys_test, np.full(len(ys_test), ys_train.mean())), 1))
print("Shuffled model MAE:   ", round(mean_absolute_error(ys_test, shuf_model.predict(Xs_test)), 1))
from sklearn.dummy import DummyRegressor
from sklearn.model_selection import cross_val_score

cv_model = cross_val_score(model, X, y, cv=5, scoring="neg_mean_absolute_error")
cv_base = cross_val_score(DummyRegressor(strategy="median"), X, y, cv=5, scoring="neg_mean_absolute_error")

print("\nCV model MAE per fold:  ", (-cv_model).round(1))
print("CV baseline MAE per fold:", (-cv_base).round(1))
print("Mean model:", round(-cv_model.mean(), 1), "| Mean baseline:", round(-cv_base.mean(), 1))