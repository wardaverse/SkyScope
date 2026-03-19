from pymongo import MongoClient
from src.config_loader import load_env

def get_database():
    env = load_env()
    client = MongoClient(env["mongodb_uri"])
    return client[env["mongodb_db"]]

def get_collections():
    db = get_database()
    return {
        "forecasts": db["forecasts"],
        "alerts": db["alerts"]
    }