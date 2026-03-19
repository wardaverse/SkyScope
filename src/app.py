from src.config_loader import load_locations, load_env
from src.workers import start_workers
from src.api_client import fetch_forecast, save_forecast
from src.alerts import generate_alerts

def validate_env():
    env = load_env()
    required_keys = ["mongodb_uri"]
    missing = [k for k in required_keys if not env.get(k)]
    if missing:
        raise ValueError(f"Missing environment variables: {missing}")

def run_once(locations):
    for location in locations:
        city = location["city"]
        lat = location["lat"]
        lon = location["lon"]


        forecast = fetch_forecast(lat, lon)
        save_forecast(city, lat, lon, forecast)
        generate_alerts(city, forecast)
        print(f"[INFO] One-time forecast saved for {city}")

if __name__ == "__main__":
    validate_env()
    locations = load_locations()
    run_once(locations)