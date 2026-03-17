from src.config_loader import load_locations, load_env
from src.workers import start_workers

def validate_env():
    env = load_env()
    missing = [k for k, v in env.items() if not v]
    if missing:
        raise ValueError(f"Missing environment variables: {missing}")

if __name__ == "__main__":
    validate_env()
    locations = load_locations()
    start_workers(locations)