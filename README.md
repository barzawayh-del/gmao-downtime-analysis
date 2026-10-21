# GMAO Downtime Analysis

Cleans a messy maintenance log (Excel) and computes Pareto charts,
MTBF and MTTR per machine with pandas and matplotlib.

## Run

```bash
pip install pandas numpy matplotlib openpyxl
python main1.py
```

## Metrics

- MTBF: mean time between failures (hours)
- MTTR: mean time to repair (minutes)