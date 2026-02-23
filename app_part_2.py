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
        "Monthly Trends",
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
    - **Monthly ridership trends** (staffing and scaling decisions)
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
# PAGE: MONTHLY TRENDS
# =========================================================
elif page == "Monthly Trends":

    st.title("Monthly Trends")
    st.subheader("Average Daily Citi Bike Rides per Month (2022)")
    st.caption("Source: Daily ride counts aggregated to monthly averages.")

    daily_path = "citibike_2022_daily_with_weather.csv"

    if not os.path.exists(daily_path):
        st.error(f"Daily weather CSV not found: {daily_path}")
    else:
        df_daily = load_daily_weather(daily_path)

        required_cols = {"date", "daily_ride_count"}
        if not required_cols.issubset(df_daily.columns):
            st.error(f"Missing required columns. Needed: {required_cols}")
        else:
            df_daily["month_num"] = df_daily["date"].dt.month
            df_daily["month_name"] = df_daily["date"].dt.strftime("%b")

            monthly_avg = (
                df_daily.groupby(["month_num", "month_name"])["daily_ride_count"]
                .mean()
                .reset_index()
                .sort_values("month_num")
            )

            fig_monthly = px.line(
                monthly_avg,
                x="month_name",
                y="daily_ride_count",
                markers=True,
                title="Average Daily CitiBike Rides per Month (2022)",
                labels={
                    "month_name": "Month",
                    "daily_ride_count": "Average Daily Ride Count"
                }
            )

            fig_monthly.update_layout(
                template="plotly_white",
                height=550
            )

            st.plotly_chart(fig_monthly, use_container_width=True)

            st.markdown("""
            **Interpretation:** This chart shows strong seasonality in Citi Bike demand.  
            - Ridership climbs steadily from winter into summer  
            - The peak demand period is **June through September**  
            - Demand drops sharply starting in **October**, reaching the lowest levels in winter  

            This pattern supports scaling supply and operations based on season (more bikes and rebalancing in summer, reduced operations in winter).
            """)


# =========================================================
# PAGE: TRIP MAP
# =========================================================
elif page == "Trip Map":

    st.title("Trip Map")
    st.subheader("Kepler.gl Trip Map")
    st.caption("Spatial view of high-activity zones and common movement clusters.")

    map_file = "kepler_map.html"

    if os.path.exists(map_file):
        with open(map_file, "r", encoding="utf-8") as f:
            map_html = f.read()
        components.html(map_html, height=700, scrolling=True)

        st.markdown("""
        **Interpretation:**  
        Trip activity is highly concentrated in central Manhattan, with dense movement clusters around
        business districts and major transit corridors.

        This indicates:
        - High commuter usage in central areas  
        - Strong tourism-related activity  
        - Clear priority zones for bike rebalancing operations  

        These zones should receive more frequent restocking and operational monitoring.
        """)

    else:
        st.warning("kepler_map.html not found. Make sure it is in the same folder as app_part_2.py.")


# =========================================================
# PAGE: RECOMMENDATIONS
# =========================================================
elif page == "Recommendations":

    st.title("Recommendations")
    st.subheader("Operational Recommendations for Citi Bike Supply (2022)")
    st.caption("Recommendations are derived directly from the dashboard charts and trends.")

    # Load daily dataset so we can compute simple, explainable numbers
    daily_path = "citibike_2022_daily_with_weather.csv"

    if not os.path.exists(daily_path):
        st.warning("Dataset not found for numeric summary. Recommendations will display without computed metrics.")
        df_daily = None
    else:
        df_daily = load_daily_weather(daily_path)

        # Safety check (only compute if columns exist)
        needed = {"date", "daily_ride_count", "TAVG"}
        if not needed.issubset(df_daily.columns):
            st.warning(f"Missing columns for summary metrics: {needed}")
            df_daily = None

    # -------------------------
    # Compute simple metrics (only if we can)
    # -------------------------
    if df_daily is not None:
        df_daily = df_daily.copy()
        df_daily["month"] = df_daily["date"].dt.month
        monthly_avg = df_daily.groupby("month")["daily_ride_count"].mean()

        peak_month = int(monthly_avg.idxmax())
        peak_value = float(monthly_avg.max())

        low_month = int(monthly_avg.idxmin())
        low_value = float(monthly_avg.min())

        # Winter vs Summer comparison (simple & defensible)
        winter_months = [11, 12, 1, 2, 3, 4]   # Nov–Apr
        summer_months = [6, 7, 8]            # Jun–Aug
        winter_avg = float(df_daily[df_daily["month"].isin(winter_months)]["daily_ride_count"].mean())
        summer_avg = float(df_daily[df_daily["month"].isin(summer_months)]["daily_ride_count"].mean())

        # How much lower winter is compared to summer
        winter_scale_pct = (winter_avg / summer_avg) * 100 if summer_avg else None
        winter_reduction_pct = 100 - winter_scale_pct if winter_scale_pct is not None else None

        month_names = {
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
            5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
            9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
        }

        st.markdown("### Key numbers from the dashboard")
        col1, col2, col3 = st.columns(3)

        col1.metric("Peak month (avg/day)", f"{month_names[peak_month]}", f"{peak_value:,.0f} rides/day")
        col2.metric("Lowest month (avg/day)", f"{month_names[low_month]}", f"{low_value:,.0f} rides/day")

        if winter_scale_pct is not None:
            col3.metric("Winter vs Summer", f"{winter_scale_pct:,.0f}% of summer demand", f"-{winter_reduction_pct:,.0f}%")

        st.markdown("---")

    # -------------------------
    # Recommendations (with chart connections)
    # -------------------------
    st.markdown("""
    ## 1) Prioritize high-demand Manhattan stations
    - The **Top 10 Stations** page shows demand concentrated in central Manhattan.
    - **Action:** Increase rebalancing frequency and consider higher dock capacity at these top stations.
    - **Why it matters:** These stations are the biggest risk points for empty docks or no available bikes.

    ## 2) Use seasonality to scale supply (Nov–Apr vs Summer)
    - The **Trips vs Temperature** + **Monthly Trends** pages show strong seasonal demand.
    - **Action:** Plan seasonal rebalancing schedules and staffing:
      - Higher redistribution activity in warm months (late spring to early fall)
      - Reduced redistribution intensity during winter months
    """)

    if df_daily is not None and winter_reduction_pct is not None:
        st.markdown(f"""
    **Data support:** Winter demand (Nov–Apr) averages about **{winter_scale_pct:,.0f}%** of summer demand (Jun–Aug).  
    A practical starting point is scaling redistribution operations down by roughly **{winter_reduction_pct:,.0f}%** in winter (then fine-tune by station).
        """)

    st.markdown("""
    ## 3) Improve reliability at peak stations
    - The station chart and the map indicate consistent hotspots.
    - **Action:** Add operational routines such as:
      - Early morning restocking (before commute peaks)
      - Mid-day “check cycles” for the busiest stations
      - Targeted evening rebalancing for commuter corridors

    ## 4) Expand service in waterfront / high-growth corridors (data-driven)
    - The **Trip Map** shows movement clusters and under-served edges.
    - **Action:** Use map hotspots and repeated flows to justify new stations or dock expansions near waterfront routes.
    - **How to validate:** Compare demand intensity near the waterfront vs. existing station coverage (see follow-up question #2).
    """)