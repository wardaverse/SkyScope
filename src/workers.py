import threading
import time
from src.api_client import fetch_forecast, save_forecast
from src.alerts import generate_alerts
from src.map_service import download_weather_map

def forecast_worker(location, interval_seconds=300):
    city = location["city"]
    country = location["country"]

    while True:
        try:
            forecast = fetch_forecast(city, country)
            save_forecast(city, country, forecast)
            generate_alerts(city, country, forecast)
            print(f"[INFO] Forecast updated for {city}, {country}")
        except Exception as e:
            print(f"[ERROR] Forecast worker failed for {city}: {e}")
        time.sleep(interval_seconds)

def map_worker(interval_seconds=600):
    while True:
        try:
            path = download_weather_map()
            print(f"[INFO] Map downloaded: {path}")
        except Exception as e:
            print(f"[ERROR] Map worker failed: {e}")
        time.sleep(interval_seconds)

def start_workers(locations):
    threads = []

    for location in locations:
        t = threading.Thread(target=forecast_worker, args=(location,), daemon=True)
        threads.append(t)

    t_map = threading.Thread(target=map_worker, daemon=True)
    threads.append(t_map)

    for t in threads:
        t.start()

    for t in threads:
        t.join()