from datetime import datetime
from src.db import get_collections

RAIN_CODES = [51, 53, 55, 61, 63, 65, 80, 81, 82]
SNOW_CODES = [71, 73, 75, 77, 85, 86]

def generate_alerts(city, forecast_json):
    collections = get_collections()
    hourly = forecast_json.get("hourly", {})

    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    weather_codes = hourly.get("weather_code", [])

    alerts = []

    for i in range(len(times)):
        reasons = []

        if weather_codes[i] in RAIN_CODES:
            reasons.append("Rain expected")

        if weather_codes[i] in SNOW_CODES:
            reasons.append("Snow expected")

        if temps[i] < 0:
            reasons.append(f"Freezing temperature expected: {temps[i]}°C")

        if reasons:
            alert = {
                "city": city,
                "forecast_time": times[i],
                "temperature_c": temps[i],
                "weather_code": weather_codes[i],
                "reasons": reasons,
                "created_at": datetime.utcnow()
            }
            alerts.append(alert)
            print(f"[ALERT] {city} @ {times[i]} -> {', '.join(reasons)}")

    if alerts:
        collections["alerts"].insert_many(alerts)

    return alerts