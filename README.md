# GMAO Downtime Analysis

Computes MTBF and MTTR per machine from a maintenance (GMAO) downtime log,
builds an Excel report with a chart, and emails it automatically on weekdays.

## Files
- `main1.py`: MTBF / MTTR analysis and charts
- `report_day9.py`: builds `gmao_report.xlsx` (summary, clean log, MTBF chart)
- `send_report.py`: emails the report
- `run_pipeline.py`: runs both steps, logs to `pipeline.log`, emails an alert on failure
- `run_report.bat`: entry point used by Windows Task Scheduler
- `api_day8.py`: weather API example with error handling

## Setup

```bash
pip install pandas numpy matplotlib openpyxl requests
```

Data is not included (ignored by Git). Provide `gmao_clean.csv` with the
columns `date`, `machine`, `downtime_min`, `cause`.

Email credentials are read from environment variables, never from the code:
`GMAIL_USER` and `GMAIL_APP_PASSWORD` (a Gmail app password).

## Run

```bash
python run_pipeline.py
```

## Schedule (Windows, weekdays at 19:30)

```bash
schtasks /create /tn "GMAOReport" /tr "C:\path\to\run_report.bat" /sc weekly /d MON,TUE,WED,THU,FRI /st 19:30
```

## Metrics
- MTBF: mean time between failures (hours). Assumes 24h/day operation.
- MTTR: mean time to repair (minutes). Flagged unreliable with fewer than 2 known durations.

## Limitations
- Runs only when the computer is on and the user is logged in.
- Small sample data: use the numbers to learn the method, not to take decisions.