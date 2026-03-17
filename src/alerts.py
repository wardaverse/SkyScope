from datetime import datetime
from src.db import get_collections

FREEZING_F = 2

def generate_alerts(city, country, forecast_json):
    collections = get_collections()
    alerts = []

    for item in forecast_json.get("list", []):
        weather_main = item["weather"][0]["main"].lower()
        temp_f = item["main"]["temp"]
        forecast_time = item.get("dt_txt")

        reasons = []
        if "rain" in weather_main:
            reasons.append("Rain expected")
        if "snow" in weather_main:
            reasons.append("Snow expected")
        if temp_f < FREEZING_F:
            reasons.append(f"Freezing temperature expected: {temp_f}F")

        if reasons:
            alert = {
                "city": city,
                "country": country,
                "forecast_time": forecast_time,
                "temperature_f": temp_f,
                "reasons": reasons,
                "created_at": datetime.utcnow()
            }
            alerts.append(alert)
            print(f"[ALERT] {city}, {country} @ {forecast_time} -> {', '.join(reasons)}")

    if alerts:
        collections["alerts"].insert_many(alerts)

    return alerts