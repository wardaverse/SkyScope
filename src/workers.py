import threading
import time
from src.api_client import fetch_forecast, save_forecast
from src.alerts import generate_alerts

def forecast_worker(location, interval_seconds=300):
    city = location["city"]
    lat = location["lat"]
    lon = location["lon"]

    while True:
        try:
            forecast = fetch_forecast(lat, lon)
            save_forecast(city, lat, lon, forecast)
            generate_alerts(city, forecast)
            print(f"[INFO] Forecast updated for {city}")
        except Exception as e:
            print(f"[ERROR] Forecast worker failed for {city}: {e}")
        time.sleep(interval_seconds)

def start_workers(locations):
    threads = []

    for location in locations:
        t = threading.Thread(target=forecast_worker, args=(location,), daemon=True)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()