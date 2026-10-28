import requests
import pandas as pd


def get_forecast(lat, lon, days=3):
    """Fetch hourly temperature forecast and return a DataFrame (or None on failure)."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "forecast_days": days,
        "timezone": "auto",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as error:
        print("Request failed:", error)
        return None

    data = response.json()
    return pd.DataFrame({
        "time": pd.to_datetime(data["hourly"]["time"]),
        "temp_c": data["hourly"]["temperature_2m"],
    })


df = get_forecast(33.57, -7.59, days=3)

if df is not None:
    df["day"] = df["time"].dt.date
    daily = df.groupby("day")["temp_c"].agg(["min", "max", "mean"]).round(1)
    print(daily)
    df.to_csv("forecast.csv", index=False)
    print("\nSaved forecast.csv:", len(df), "rows")