import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(
    page_title="NYC Citi Bike Dashboard 2022",
    layout="wide"
)

st.title("NYC Citi Bike Dashboard (2022)")

st.markdown("""
This dashboard analyzes Citi Bike usage patterns in New York City during 2022.

It highlights:
- The most popular start stations
- The relationship between daily trips and average temperature
- A spatial view of trips via a Kepler.gl map
""")

# -------------------------
# Helpers (cache)
# -------------------------
@st.cache_data(show_spinner=False)
def load_station_trips(trip_path: str) -> pd.DataFrame:
    csv_files = sorted([f for f in os.listdir(trip_path) if f.endswith(".csv")])

    dfs = []
    for file in csv_files:
        df_temp = pd.read_csv(
            os.path.join(trip_path, file),
            usecols=["start_station_name"]
        )
        dfs.append(df_temp)

    return pd.concat(dfs, ignore_index=True)

@st.cache_data(show_spinner=False)
def load_daily_weather(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return df

# -------------------------
# TOP 10 START STATIONS
# -------------------------
st.divider()
st.subheader("Top 10 Most Popular Citi Bike Start Stations (2022)")

trip_path = "data/2022-citibike-tripdata"

if not os.path.exists(trip_path):
    st.error(f"Tripdata folder not found: {trip_path}")
else:
    stations_full = load_station_trips(trip_path)

    popular_stations = (
        stations_full
        .dropna(subset=["start_station_name"])
        .groupby("start_station_name")
        .size()
        .reset_index(name="trip_count")
        .sort_values("trip_count", ascending=False)
    )

    top10 = popular_stations.head(10)

    fig_bar = px.bar(
        top10,
        x="trip_count",
        y="start_station_name",
        orientation="h",
        title="Top 10 Most Popular Citi Bike Start Stations (2022)",
        labels={
            "trip_count": "Number of Trips",
            "start_station_name": "Station Name"
        },
        color="trip_count",
        color_continuous_scale="Blues"
    )

    fig_bar.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        height=550
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("""
**Insight:** The top stations are concentrated in Manhattan, suggesting heavy commuter and tourist demand in central areas.
""")

# -------------------------
# DAILY TRIPS vs TEMPERATURE (DUAL AXIS)
# -------------------------
st.divider()
st.subheader("Daily Citi Bike Trips vs Average Temperature (2022)")

daily_path = "citibike_2022_daily_with_weather.csv"
if not os.path.exists(daily_path):
    st.error(f"Daily weather CSV not found: {daily_path}")
else:
    df_daily = load_daily_weather(daily_path)

    fig_line = make_subplots(specs=[[{"secondary_y": True}]])

    fig_line.add_trace(
        go.Scatter(
            x=df_daily["date"],
            y=df_daily["daily_ride_count"],
            name="Daily Ride Count",
            mode="lines"
        ),
        secondary_y=False
    )

    fig_line.add_trace(
        go.Scatter(
            x=df_daily["date"],
            y=df_daily["TAVG"],
            name="Average Temperature (°C)",
            mode="lines"
        ),
        secondary_y=True
    )

    fig_line.update_layout(
        title="Daily Citi Bike Trips vs Average Temperature (2022)",
        height=550,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig_line.update_xaxes(title_text="Date")
    fig_line.update_yaxes(title_text="Number of Trips", secondary_y=False)
    fig_line.update_yaxes(title_text="Average Temperature (°C)", secondary_y=True)

    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("""
**Insight:** Ridership generally increases as temperatures rise, with peak usage during the warmer summer months.
""")

# -------------------------
# KEPLER MAP (HTML)
# -------------------------
st.divider()
st.subheader("Kepler.gl Trip Map")

st.markdown("""
This map provides a spatial view of Citi Bike trip patterns across NYC, helping identify high-activity zones and common movement clusters.
""")

map_file = "kepler_map.html"
if os.path.exists(map_file):
    with open(map_file, "r", encoding="utf-8") as f:
        map_html = f.read()
    components.html(map_html, height=700, scrolling=True)
else:
    st.warning("kepler_map.html not found in the project folder. Make sure it's in the same folder as app.py.")