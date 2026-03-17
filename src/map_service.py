import os
import folium
from src.db import get_collections

def build_city_map(output_file="data/maps/city_weather_map.html"):
    os.makedirs("data/maps", exist_ok=True)
    docs = list(get_collections()["forecasts"].find())

    if not docs:
        print("No forecast data available for map")
        return None

    weather_map = folium.Map(location=[20, 0], zoom_start=2)

    latest_by_city = {}
    for doc in docs:
        key = doc["city"]
        if key not in latest_by_city or doc["forecast_time"] > latest_by_city[key]["forecast_time"]:
            latest_by_city[key] = doc

    for city, doc in latest_by_city.items():
        popup = (
            f"{city}<br>"
            f"Temp: {doc['temperature_c']}°C<br>"
            f"Precipitation: {doc['precipitation']} mm<br>"
            f"Forecast: {doc['forecast_time']}"
        )

        folium.Marker(
            location=[doc["lat"], doc["lon"]],
            popup=popup,
            tooltip=city
        ).add_to(weather_map)

    weather_map.save(output_file)
    return output_file