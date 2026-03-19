import requests
from datetime import datetime
from src.db import get_collections

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_forecast(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation,weather_code",
        "timezone": "auto"
    }

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def save_forecast(city, lat, lon, forecast_json):
    collections = get_collections()
    hourly = forecast_json.get("hourly", {})

    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    precipitation = hourly.get("precipitation", [])
    weather_codes = hourly.get("weather_code", [])

    docs = []
    for i in range(len(times)):
        docs.append({
            "city": city,
            "lat": lat,
            "lon": lon,
            "forecast_time": times[i],
            "temperature_c": temps[i],
            "precipitation": precipitation[i],
            "weather_code": weather_codes[i],
            "inserted_at": datetime.utcnow()
        })

    if docs:
        collections["forecasts"].insert_many(docs)