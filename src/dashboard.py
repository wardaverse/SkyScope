import pandas as pd
import streamlit as st
from pymongo import DESCENDING

from src.db import get_collections

st.set_page_config(
    page_title="SkyScope Weather Dashboard",
    page_icon="🌦️",
    layout="wide"
)

@st.cache_data(ttl=300)
def load_forecast_data(city=None):
    collections = get_collections()
    query = {}
    if city and city != "All":
        query["city"] = city

    docs = list(
        collections["forecasts"]
        .find(query, {"_id": 0})
        .sort("forecast_time", 1)
    )
    return pd.DataFrame(docs)

@st.cache_data(ttl=300)
def load_alerts_data(city=None):
    collections = get_collections()
    query = {}
    if city and city != "All":
        query["city"] = city

    docs = list(
        collections["alerts"]
        .find(query, {"_id": 0})
        .sort("created_at", DESCENDING)
    )
    return pd.DataFrame(docs)

@st.cache_data(ttl=300)
def load_available_cities():
    collections = get_collections()
    cities = collections["forecasts"].distinct("city")
    cities = sorted([c for c in cities if c])
    return ["All"] + cities

st.title("🌦️ SkyScope Weather Dashboard")
st.caption("Weather forecasts, alerts, and trends from Open-Meteo + MongoDB")

cities = load_available_cities()
selected_city = st.sidebar.selectbox("Select city", cities)

forecast_df = load_forecast_data(selected_city)
alerts_df = load_alerts_data(selected_city)

if forecast_df.empty:
    st.warning("No forecast data found in MongoDB yet. Run the ingestion app first.")
    st.stop()

latest_df = (
    forecast_df.sort_values("forecast_time")
    .groupby("city", as_index=False)
    .tail(1)
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tracked Cities", latest_df["city"].nunique())

with col2:
    st.metric("Forecast Records", len(forecast_df))

with col3:
    st.metric("Alerts Found", 0 if alerts_df.empty else len(alerts_df))

st.subheader("Latest Conditions")

latest_display = latest_df[[
    "city",
    "forecast_time",
    "temperature_c",
    "precipitation",
    "weather_code"
]].copy()

latest_display = latest_display.rename(columns={
    "forecast_time": "Forecast Time",
    "temperature_c": "Temperature (°C)",
    "precipitation": "Precipitation (mm)",
    "weather_code": "Weather Code"
})

st.dataframe(latest_display, use_container_width=True, hide_index=True)

st.subheader("Temperature Trend")

chart_df = forecast_df[["forecast_time", "temperature_c", "city"]].copy()
chart_df["forecast_time"] = pd.to_datetime(chart_df["forecast_time"])

if selected_city == "All":
    pivot_df = chart_df.pivot_table(
        index="forecast_time",
        columns="city",
        values="temperature_c",
        aggfunc="last"
    )
    st.line_chart(pivot_df)
else:
    city_chart = chart_df.set_index("forecast_time")[["temperature_c"]]
    st.line_chart(city_chart)

st.subheader("Forecast Table")

table_df = forecast_df.copy()
if "inserted_at" in table_df.columns:
    table_df["inserted_at"] = pd.to_datetime(table_df["inserted_at"], errors="coerce")

display_cols = [c for c in [
    "city",
    "forecast_time",
    "temperature_c",
    "precipitation",
    "weather_code",
    "lat",
    "lon"
] if c in table_df.columns]

st.dataframe(table_df[display_cols], use_container_width=True, hide_index=True)

st.subheader("Map")

map_df = latest_df[["city", "lat", "lon", "temperature_c"]].dropna().copy()
map_df = map_df.rename(columns={"lat": "latitude", "lon": "longitude"})

if not map_df.empty:
    st.map(map_df[["latitude", "longitude"]])
    st.dataframe(map_df, use_container_width=True, hide_index=True)
else:
    st.info("No coordinates available to display on the map.")

st.subheader("Recent Alerts")

if alerts_df.empty:
    st.success("No rain, snow, or freezing alerts found for the selected scope.")
else:
    st.dataframe(alerts_df, use_container_width=True, hide_index=True)