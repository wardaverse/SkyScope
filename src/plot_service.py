import os
import matplotlib.pyplot as plt
from src.db import get_collections

def plot_city_temperature(city, output_dir="data/plots"):
    os.makedirs(output_dir, exist_ok=True)
    docs = list(get_collections()["forecasts"].find({"city": city}).sort("forecast_time", 1))

    if not docs:
        print(f"No data found for {city}")
        return None

    times = [doc["forecast_time"] for doc in docs]
    temps = [doc["temperature_c"] for doc in docs]

    plt.figure(figsize=(12, 6))
    plt.plot(times, temps, marker="o")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Forecast Time")
    plt.ylabel("Temperature (°C)")
    plt.title(f"Temperature Trend for {city}")
    plt.tight_layout()

    output_file = os.path.join(output_dir, f"{city.lower().replace(' ', '_')}_temperature_plot.png")
    plt.savefig(output_file)
    plt.close()
    return output_file