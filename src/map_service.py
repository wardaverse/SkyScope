import os
import requests
from datetime import datetime
from src.config_loader import load_env
from src.db import get_collections

MAP_LAYER = "TA2"  # example temperature layer

def download_weather_map(z=2, x=2, y=1):
    env = load_env()
    url = f"https://maps.openweathermap.org/maps/2.0/weather/{MAP_LAYER}/{z}/{x}/{y}"
    params = {
        "appid": env["openweather_api_key"]
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    os.makedirs("data/maps", exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_path = f"data/maps/{MAP_LAYER}_{timestamp}.png"

    with open(file_path, "wb") as f:
        f.write(response.content)

    get_collections()["maps"].insert_one({
        "layer": MAP_LAYER,
        "file_path": file_path,
        "downloaded_at": datetime.utcnow()
    })

    return file_path