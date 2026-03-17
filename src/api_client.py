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