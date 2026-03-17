import requests
from src.config_loader import load_env

BASE_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

def fetch_forecast(city, country=None, units="imperial"):
    env = load_env()
    q = city if not country else f"{city},{country}"
    params = {
        "q": q,
        "appid": env["openweather_api_key"],
        "units": units
    }
    response = requests.get(BASE_FORECAST_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

from datetime import datetime
from src.db import get_collections

def save_forecast(city, country, forecast_json):
    collections = get_collections()
    docs = []

    for item in forecast_json.get("list", []):
        docs.append({
            "city": city,
            "country": country,
            "forecast_time": item.get("dt_txt"),
            "timestamp": item.get("dt"),
            "temperature_f": item["main"]["temp"],
            "feels_like_f": item["main"]["feels_like"],
            "humidity": item["main"]["humidity"],
            "weather_main": item["weather"][0]["main"],
            "weather_description": item["weather"][0]["description"],
            "wind_speed": item["wind"]["speed"],
            "raw": item,
            "inserted_at": datetime.utcnow()
        })

    if docs:
        collections["forecasts"].insert_many(docs)