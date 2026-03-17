import json
import os
from dotenv import load_dotenv

load_dotenv()

def load_env():
    return {
        "openweather_api_key": os.getenv("OPENWEATHER_API_KEY"),
        "mongodb_uri": os.getenv("MONGODB_URI"),
        "mongodb_db": os.getenv("MONGODB_DB", "weather_monitor"),
    }

def load_locations(path="config/locations.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["locations"]