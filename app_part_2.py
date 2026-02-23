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

# -------------------------
# Sidebar Navigation
# -------------------------
page = st.sidebar.selectbox(
    "Select Page",
    [
        "Introduction",
        "Popular Stations",
        "Trips vs Temperature",
        "Trip Map",
        "Recommendations"
    ]
)

# -------------------------
# Helpers (cache)
# -------------------------
@st.cache_data(show_spinner=False)
def load_daily_weather(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return df


# =========================================================
# PAGE: INTRODUCTION
# =========================================================
if page == "Introduction":

    st.title("NYC Citi Bike Dashboard (2022)")

    st.markdown("""
    This dashboard analyzes Citi Bike usage patterns in New York City during 2022 to support **bike supply and rebalancing decisions**.

    **What you’ll find inside:**
    - The **top 10 most popular start stations** (high-demand areas)
    - The relationship between **daily trips and average temperature** (seasonality)
    - A **Kepler.gl map** to explore trip patterns spatially
    """)

    st.info("Use the sidebar to navigate between pages.")


# =========================================================
# PAGE: POPULAR STATIONS
# =========================================================
elif page == "Popular Stations":

    st.title("Popular Stations")
    st.subheader("Top 10 Most Popular Citi Bike Start Stations (2022)")
    st.caption("Source: Citi Bike trip data (2022), aggregated from monthly files.")

    top10_path = "top10_stations_2022.csv"

    if not os.path.exists(top10_path):
        st.error(f"File not found: {top10_path}")
    else:
        top10 = pd.read_csv(top10_path)

        # Safety check
        if "start_station_name" not in top10.columns or "trip_count" not in top10.columns:
            st.error("Expected columns not found. Required: start_station_name, trip_count")
        else:
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
            **Interpretation:** The highest-demand start stations are concentrated in central Manhattan.  
            These locations are strong candidates for:
            - **More frequent rebalancing**
            - **Higher dock capacity**
            - **Proactive stocking during peak hours**
            """)


# =========================================================
# PAGE: TRIPS VS TEMPERATURE
# =========================================================
elif page == "Trips vs Temperature":

    st.title("Trips vs Temperature")
    st.subheader("Daily Citi Bike Trips vs Average Temperature (2022)")
    st.caption("Source: Daily ride counts merged with NOAA weather data.")

    daily_path = "citibike_2022_daily_with_weather.csv"

    if not os.path.exists(daily_path):
        st.error(f"Daily weather CSV not found: {daily_path}")
    else:
        df_daily = load_daily_weather(daily_path)

        # Ensure required columns exist
        required_cols = {"date", "daily_ride_count", "TAVG"}
        if not required_cols.issubset(df_daily.columns):
            st.error(f"Missing required columns. Needed: {required_cols}")
        else:
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
            **Interpretation:** Ridership increases during warmer periods and drops sharply in colder months.  
            This supports **seasonal rebalancing planning** (more bikes in summer, fewer in winter).
            """)


# =========================================================
# PAGE: TRIP MAP
# =========================================================
elif page == "Trip Map":

    st.title("Trip Map")
    st.subheader("Kepler.gl Trip Map")
    st.caption("Spatial view of high-activity zones and common movement clusters.")

    st.markdown("""
    **Interpretation:** Trips cluster heavily in Manhattan, reflecting dense commuting and tourism patterns.
    This helps identify where rebalancing operations should be prioritized.
    """)

    map_file = "kepler_map.html"

    if os.path.exists(map_file):
        with open(map_file, "r", encoding="utf-8") as f:
            map_html = f.read()
        components.html(map_html, height=700, scrolling=True)
    else:
        st.warning("kepler_map.html not found. Make sure it is in the same folder as app_part_2.py.")


# =========================================================
# PAGE: RECOMMENDATIONS
# =========================================================
elif page == "Recommendations":

    st.title("Recommendations")
    st.subheader("Operational Recommendations for Citi Bike Supply (2022)")

    st.markdown("""
    Based on the dashboard results:

    **1) Prioritize high-demand Manhattan stations**
    - The top stations show concentrated demand in central Manhattan.
    - Increase **rebalancing frequency** and consider **higher dock capacity** at those locations.

    **2) Use temperature/seasonality for planning**
    - Trips rise with warmer temperatures and fall during colder months.
    - Scale staffing and redistribution schedules seasonally (more active rebalancing in summer).

    **3) Improve reliability at peak stations**
    - Add operational tactics such as:
      - early morning restocking,
      - mid-day check cycles,
      - and targeted evening rebalancing for commuter areas.
    """)