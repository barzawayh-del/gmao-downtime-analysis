import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("gmao_clean.csv", parse_dates=["date"])

# Observation period: first to last day, inclusive
days = (df["date"].max() - df["date"].min()).days + 1
period_h = days * 24          # assumption: machines run 24h/day
print("Observation period:", days, "days =", period_h, "hours\n")

g = df.groupby("machine")["downtime_min"]
stats = pd.DataFrame({
    "failures": g.size(),                  # all failures, even unknown duration
    "known_durations": g.count(),          # failures with a known duration
    "downtime_h": g.sum() / 60,
    "MTTR_min": g.mean(),                  # mean() ignores NaN automatically
})
stats["MTBF_h"] = (period_h - stats["downtime_h"]) / stats["failures"]

# Sanity check: MTBF must be positive
assert (stats["MTBF_h"] > 0).all(), "Check your period or data!"

print(stats.round(2))

# Visual: two bar charts side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
stats["MTBF_h"].sort_values().plot.bar(ax=ax1, color="seagreen")
ax1.set_title("MTBF (hours) - higher is better")
stats["MTTR_min"].sort_values(ascending=False).plot.bar(ax=ax2, color="crimson")
ax2.set_title("MTTR (min) - lower is better")
plt.tight_layout()
plt.show()
stats["MTTR_reliable"] = stats["known_durations"] >= 2   # at least 2 measurements
print(stats[["failures", "known_durations", "MTTR_min", "MTTR_reliable"]])