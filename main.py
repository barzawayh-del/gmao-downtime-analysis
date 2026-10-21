import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def make_fake_log(n=200, seed=42):
    """Create a fake maintenance log."""
    np.random.seed(seed)
    return pd.DataFrame({
        "machine": np.random.choice(["Press-A", "Press-B", "Conveyor", "Pump"], n),
        "downtime_min": np.random.exponential(scale=40, size=n).round(1),
        "cause": np.random.choice(["electrical", "mechanical", "sensor", "operator"], n),
    })


def pareto_chart(df, group_col):
    """Bar chart of total downtime per group + cumulative % line + 80% reference."""
    summary = df.groupby(group_col)["downtime_min"].sum().sort_values(ascending=False)
    cum_pct = summary.cumsum() / summary.sum() * 100

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(summary.index, summary.values, color="steelblue")
    ax.set_ylabel("Total downtime (min)")

    ax2 = ax.twinx()
    ax2.plot(summary.index, cum_pct.values, color="crimson", marker="o")
    ax2.set_ylim(0, 110)
    ax2.axhline(80, color="gray", linestyle="--")  # the 80% reference line
    ax2.set_ylabel("Cumulative %")

    ax.set_title(f"Pareto of downtime by {group_col}")
    plt.tight_layout()
    plt.show()


df = make_fake_log()
pareto_chart(df, "cause")    # close this window to see the next chart
pareto_chart(df, "machine")