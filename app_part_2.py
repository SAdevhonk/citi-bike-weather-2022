import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NYC Citi Bike Dashboard 2022",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL DARK THEME OVERRIDE
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #0f0f0f !important;
    color: #f0f0f0 !important;
}
[data-testid="stSidebar"] {
    background-color: #161616 !important;
    border-right: 1px solid #2e2e2e;
}
[data-testid="stSidebar"] * { color: #c0c0c0 !important; }
[data-testid="stSidebar"] .stSelectbox label { color: #888 !important; font-size: 12px !important; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #1e1e1e;
    border: 1px solid #2e2e2e;
    padding: 16px 20px;
    border-radius: 0;
}
[data-testid="stMetricLabel"] { color: #888 !important; font-size: 12px !important; font-family: monospace !important; text-transform: uppercase; letter-spacing: 1px; }
[data-testid="stMetricValue"] { color: #3dd68c !important; font-size: 28px !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] { color: #00d4ff !important; }

/* ── Headings ── */
h1 { color: #f0f0f0 !important; font-family: sans-serif !important; letter-spacing: 1px; }
h2 { color: #3dd68c !important; font-family: sans-serif !important; border-bottom: 1px solid #2e2e2e; padding-bottom: 6px; margin-top: 32px !important; }
h3 { color: #f0f0f0 !important; }
p, li { color: #c0c0c0 !important; }

/* ── Caption / info ── */
[data-testid="stCaptionContainer"] p { color: #888 !important; font-family: monospace !important; font-size: 12px !important; }
[data-testid="stInfo"] { background: #1e1e1e !important; border-left: 3px solid #3dd68c !important; color: #c0c0c0 !important; }

/* ── Divider ── */
hr { border-color: #2e2e2e !important; }

/* ── Plotly chart background ── */
.js-plotly-plot .plotly { background: transparent !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border: 1px solid #2e2e2e !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
st.sidebar.markdown("""
<div style="padding: 8px 0 20px; border-bottom: 1px solid #2e2e2e; margin-bottom: 16px;">
  <div style="font-family: monospace; font-size: 11px; color: #888; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px;">Portfolio Project</div>
  <div style="font-size: 15px; font-weight: 700; color: #f0f0f0;">🚲 Citi Bike 2022</div>
  <div style="font-family: monospace; font-size: 11px; color: #3dd68c; margin-top: 4px;">Ageel Alramadhan</div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "Navigate to",
    [
        "Introduction",
        "Popular Stations",
        "Trips vs Temperature",
        "Monthly Trends",
        "Temperature Scatter",
        "Trip Map",
        "Recommendations",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-family: monospace; font-size: 11px; color: #888; line-height: 1.8;">
<b style="color:#f0f0f0">Dataset</b><br>
~1.7M trip records<br>
NYC Citi Bike (2022)<br><br>
<b style="color:#f0f0f0">Weather</b><br>
NOAA GHCND<br>
LaGuardia Airport<br><br>
<a href="https://github.com/ageelalramadhan/citi-bike-weather-2022" target="_blank" style="color:#3dd68c;">GitHub →</a><br>
<a href="https://ageelalramadhan.github.io/citi-bike-case-study.html" target="_blank" style="color:#3dd68c;">Portfolio →</a>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADER
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_daily(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df["month_num"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b")
    df["month_name_full"] = df["date"].dt.strftime("%B")
    return df.sort_values("date")

@st.cache_data(show_spinner=False)
def load_stations(path: str) -> pd.DataFrame:
    return pd.read_csv(path).sort_values("trip_count")

DAILY_PATH   = "citibike_2022_daily_with_weather.csv"
STATION_PATH = "top10_stations_2022.csv"
MAP_PATH     = "kepler_map.html"

PLOTLY_DARK = dict(
    paper_bgcolor="#0f0f0f",
    plot_bgcolor="#1e1e1e",
    font_color="#c0c0c0",
    title_font_color="#f0f0f0",
)

AXIS_DARK = dict(gridcolor="#2e2e2e", linecolor="#2e2e2e", tickcolor="#888", tickfont_color="#888")

ACCENT  = "#3dd68c"
ACCENT2 = "#00d4ff"
YELLOW  = "#f0c040"
PINK    = "#ff6b9d"

# =========================================================
# PAGE: INTRODUCTION
# =========================================================
if "Introduction" in page:

    st.markdown("## NYC Citi Bike Dashboard (2022)")
    st.markdown(
        "<div style='font-family:monospace;font-size:13px;color:#888;margin-bottom:24px;'>"
        "Python &nbsp;·&nbsp; Pandas &nbsp;·&nbsp; Plotly &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; Kepler.gl &nbsp;·&nbsp; NOAA API"
        "</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Trip Records", "~1.7M", "Full year 2022")
    col2.metric("Peak Demand", "~115K/day", "August average")
    col3.metric("Winter vs Summer", "~50%", "Nov–Apr vs Jun–Aug")
    col4.metric("Top Station", "128K trips", "W 21 St & 6 Ave")

    st.markdown("---")

    st.markdown("""
## Project Overview

Citi Bike generates millions of trip records each year, but raw trip logs don't tell operations 
teams **when to scale supply**, **which stations to prioritize**, or **how to plan for seasonal swings**.

This dashboard bridges that gap — merging 1.7 million individual ride records with NOAA daily 
weather data from LaGuardia Airport, and turning the combined dataset into actionable intelligence 
for operational decision-making.

### Business Questions
1. How should Citi Bike scale operations between winter and summer months?
2. Which stations require the highest rebalancing priority?
3. How strongly does temperature influence daily ride volume?
4. Where are the strongest geographic ride clusters in NYC?
""")

    st.info("Use the sidebar to navigate between pages.")

    st.markdown("---")
    st.markdown("""
### Data Pipeline Summary

| Step | Action |
|------|--------|
| 1. Acquire | 12 monthly Citi Bike ZIPs + NOAA API weather data |
| 2. Extract | Combined 12 CSVs using generator inside `pd.concat()` |
| 3. Clean | Parsed timestamps, filtered 2022, reshaped NOAA long→wide |
| 4. Aggregate | Grouped 1.7M rows to daily ride counts |
| 5. Merge | Inner join rides + weather on date key |
| 6. Visualize | Plotly interactive charts + Kepler.gl spatial map |
| 7. Deploy | Streamlit Cloud |
""")


# =========================================================
# PAGE: POPULAR STATIONS
# =========================================================
elif "Popular Stations" in page:

    st.markdown("## Popular Stations")
    st.caption("Source: Citi Bike trip data (2022), aggregated from monthly files.")

    if not os.path.exists(STATION_PATH):
        st.error(f"File not found: {STATION_PATH}")
    else:
        top10 = load_stations(STATION_PATH)

        fig = px.bar(
            top10,
            x="trip_count",
            y="start_station_name",
            orientation="h",
            title="Top 10 Most Popular Citi Bike Start Stations (2022)",
            labels={"trip_count": "Number of Trips", "start_station_name": "Station"},
            color="trip_count",
            color_continuous_scale=[[0, "#1a4a3a"], [0.5, "#2a9a6a"], [1.0, ACCENT]],
            text="trip_count",
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside",
                          textfont_color="#c0c0c0")
        fig.update_layout(
            **PLOTLY_DARK,
            xaxis=dict(gridcolor="#2e2e2e", linecolor="#2e2e2e", tickcolor="#888"),
            yaxis=dict(categoryorder="total ascending", gridcolor="#2e2e2e", linecolor="#2e2e2e", tickcolor="#888"),
            height=560,
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(l=10, r=80, t=50, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
### What this tells us

All 10 highest-volume start stations are in **central Manhattan**. The #1 station — 
**W 21 St & 6 Ave** — recorded over 128,000 trip starts in 2022 alone. The top 3 each 
surpassed 100,000 trips.

This concentration means a small number of stations carry a disproportionate share of 
system demand and are the **highest-risk points** for empty docks or unavailable bikes.

**Operational implication:** These stations need more frequent rebalancing cycles, higher 
dock capacity, and proactive early-morning restocking before commute peaks.
""")

        # Show data table
        with st.expander("View data table"):
            display = top10.copy().sort_values("trip_count", ascending=False)
            display["trip_count"] = display["trip_count"].apply(lambda x: f"{int(x):,}")
            display.columns = ["Station Name", "Trip Count"]
            display.index = range(1, len(display)+1)
            st.dataframe(display, use_container_width=True)


# =========================================================
# PAGE: TRIPS VS TEMPERATURE
# =========================================================
elif "Trips vs Temperature" in page:

    st.markdown("## Trips vs Temperature")
    st.caption("Source: Daily ride counts merged with NOAA weather data, LaGuardia Airport.")

    if not os.path.exists(DAILY_PATH):
        st.error(f"File not found: {DAILY_PATH}")
    else:
        df = load_daily(DAILY_PATH)

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(
                x=df["date"], y=df["daily_ride_count"],
                name="Daily Rides", mode="lines",
                line=dict(color=ACCENT, width=1.5),
                fill="tozeroy", fillcolor="rgba(61,214,140,0.08)",
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                x=df["date"], y=df["TAVG"],
                name="Avg Temp (°C)", mode="lines",
                line=dict(color=YELLOW, width=1.5, dash="dot"),
            ),
            secondary_y=True,
        )

        fig.update_layout(
            **PLOTLY_DARK,
            title="Daily Ride Count vs. Average Temperature — 2022",
            height=520,
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        xanchor="right", x=1, font_color="#c0c0c0",
                        bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=10, r=10, t=50, b=40),
        )
        fig.update_yaxes(title_text="Daily Rides", secondary_y=False,
                          title_font_color=ACCENT, tickfont_color=ACCENT,
                          gridcolor="#2e2e2e", linecolor="#2e2e2e")
        fig.update_yaxes(title_text="Avg Temp (°C)", secondary_y=True,
                          title_font_color=YELLOW, tickfont_color=YELLOW,
                          gridcolor="rgba(0,0,0,0)")
        fig.update_xaxes(title_text="Date", gridcolor="#2e2e2e", linecolor="#2e2e2e")

        st.plotly_chart(fig, use_container_width=True)

        # Key stats inline
        col1, col2, col3 = st.columns(3)
        col1.metric("Peak daily rides", f"{int(df['daily_ride_count'].max()):,}",
                    df.loc[df['daily_ride_count'].idxmax(), 'date'].strftime("%b %d"))
        col2.metric("Lowest daily rides", f"{int(df['daily_ride_count'].min()):,}",
                    df.loc[df['daily_ride_count'].idxmin(), 'date'].strftime("%b %d"))
        coldest = df.loc[df["TAVG"].idxmin()]
        col3.metric("Coldest day", f"{coldest['TAVG']:.1f}°C",
                    coldest['date'].strftime("%b %d"))

        st.markdown("""
### What this tells us

Ridership and temperature track each other closely across the full year. Cold snaps produce 
sharp drops; warm stretches push counts toward seasonal peaks.

**Operational implication:** Temperature is a reliable **forward-looking demand signal**. 
Integrating NOAA daily forecasts into supply planning would allow operations to 
anticipate demand spikes before they arrive rather than reacting after the fact.
""")


# =========================================================
# PAGE: MONTHLY TRENDS
# =========================================================
elif "Monthly Trends" in page:

    st.markdown("## Monthly Trends")
    st.caption("Source: Daily ride counts aggregated to monthly averages.")

    if not os.path.exists(DAILY_PATH):
        st.error(f"File not found: {DAILY_PATH}")
    else:
        df = load_daily(DAILY_PATH)

        monthly = (
            df.groupby(["month_num", "month_name"])["daily_ride_count"]
            .mean()
            .reset_index()
            .sort_values("month_num")
        )

        # Colour bars by season
        def season_color(m):
            if m in [12, 1, 2]: return "#4a90d9"   # winter — blue
            if m in [3, 4, 5]:  return "#f0c040"   # spring — yellow
            if m in [6, 7, 8]:  return "#3dd68c"   # summer — green
            return "#ff6b9d"                         # autumn — pink

        monthly["color"] = monthly["month_num"].apply(season_color)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly["month_name"],
            y=monthly["daily_ride_count"],
            marker_color=monthly["color"],
            text=monthly["daily_ride_count"].apply(lambda v: f"{v:,.0f}"),
            textposition="outside",
            textfont_color="#c0c0c0",
        ))
        fig.add_trace(go.Scatter(
            x=monthly["month_name"],
            y=monthly["daily_ride_count"],
            mode="lines+markers",
            line=dict(color="rgba(255,255,255,0.3)", width=1.5),
            marker=dict(color="white", size=6),
            showlegend=False,
        ))

        # Winter avg reference line
        winter_avg = df[df["month_num"].isin([11,12,1,2,3,4])]["daily_ride_count"].mean()
        summer_avg = df[df["month_num"].isin([6,7,8])]["daily_ride_count"].mean()
        fig.add_hline(y=winter_avg, line_dash="dash", line_color="#4a90d9",
                      annotation_text=f"Winter avg: {winter_avg:,.0f}", annotation_font_color="#4a90d9")
        fig.add_hline(y=summer_avg, line_dash="dash", line_color=ACCENT,
                      annotation_text=f"Summer avg: {summer_avg:,.0f}", annotation_font_color=ACCENT)

        fig.update_layout(
            **PLOTLY_DARK,
            title="Average Daily Rides per Month — 2022",
            xaxis_title="Month",
            yaxis_title="Average Daily Rides",
            height=520,
            showlegend=False,
            bargap=0.25,
            margin=dict(l=10, r=10, t=50, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        peak_row = monthly.loc[monthly["daily_ride_count"].idxmax()]
        low_row  = monthly.loc[monthly["daily_ride_count"].idxmin()]
        ratio = (winter_avg / summer_avg) * 100
        col1.metric("Peak month", peak_row["month_name"], f"{peak_row['daily_ride_count']:,.0f} rides/day")
        col2.metric("Lowest month", low_row["month_name"], f"{low_row['daily_ride_count']:,.0f} rides/day")
        col3.metric("Winter / Summer ratio", f"{ratio:.0f}%", "Nov–Apr vs Jun–Aug")

        st.markdown(f"""
### What this tells us

Ridership climbs steadily from winter into summer, peaking in **{peak_row['month_name']}** and 
dropping sharply from October onward.

Winter demand (Nov–Apr) averages **{ratio:.0f}% of summer demand** (Jun–Aug) — a direct, 
quantified baseline for seasonal scaling decisions.

**Colour key:** 🔵 Winter &nbsp; 🟡 Spring &nbsp; 🟢 Summer &nbsp; 🩷 Autumn
""")


# =========================================================
# PAGE: TEMPERATURE SCATTER
# =========================================================
elif "Scatter" in page:

    st.markdown("## Temperature vs Ridership — Scatter Analysis")
    st.caption("Each point = one day in 2022. Colour = month.")

    if not os.path.exists(DAILY_PATH):
        st.error(f"File not found: {DAILY_PATH}")
    else:
        df = load_daily(DAILY_PATH)

        import numpy as np
        z = np.polyfit(df["TAVG"].dropna(),
                       df.loc[df["TAVG"].notna(), "daily_ride_count"], 1)
        x_line = np.linspace(df["TAVG"].min(), df["TAVG"].max(), 100)
        y_line = np.poly1d(z)(x_line)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["TAVG"], y=df["daily_ride_count"],
            mode="markers",
            marker=dict(
                color=df["month_num"],
                colorscale="Plasma",
                size=8, opacity=0.75,
                colorbar=dict(
                    title="Month",
                    tickvals=[1,4,7,10,12],
                    ticktext=["Jan","Apr","Jul","Oct","Dec"],
                    tickfont_color="#888",
                    title_font_color="#888",
                ),
            ),
            text=df["date"].dt.strftime("%b %d") + "<br>" +
                 df["daily_ride_count"].apply(lambda v: f"{v:,} rides"),
            hovertemplate="%{text}<br>Temp: %{x:.1f}°C<extra></extra>",
            name="Daily observation",
        ))
        fig.add_trace(go.Scatter(
            x=x_line, y=y_line,
            mode="lines",
            line=dict(color=PINK, width=2, dash="dash"),
            name="Trend line",
        ))
        fig.update_layout(
            **PLOTLY_DARK,
            title="Daily Rides vs. Average Temperature (2022)",
            xaxis_title="Average Temperature (°C)",
            yaxis_title="Daily Ride Count",
            height=540,
            legend=dict(font_color="#c0c0c0", bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=10, r=10, t=50, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)

        corr = df[["TAVG","daily_ride_count"]].dropna().corr().iloc[0,1]
        col1, col2, col3 = st.columns(3)
        col1.metric("Pearson correlation", f"{corr:.3f}", "Rides ↔ Temperature")
        col2.metric("Trend slope", f"{z[0]:,.0f} rides/°C", "per 1°C increase")
        coldest = df.loc[df["TAVG"].idxmin()]
        warmest = df.loc[df["TAVG"].idxmax()]
        col3.metric("Temp range", f"{coldest['TAVG']:.1f}°C → {warmest['TAVG']:.1f}°C",
                    "Jan low → Jul peak")

        st.markdown(f"""
### What this tells us

The scatter confirms a strong positive relationship between temperature and daily ridership 
(Pearson r = **{corr:.3f}**). The trend line rises at approximately **{z[0]:,.0f} additional 
rides per °C** of temperature increase.

The month colour-coding (plasma scale) shows the seasonal arc embedded in the data — 
cool blues (January) in the bottom-left, warm yellows (July–August) in the top-right.

**Operational implication:** NOAA temperature forecasts could be operationalized as a 
forward-looking demand signal — allowing supply adjustments before demand spikes arrive.
""")


# =========================================================
# PAGE: TRIP MAP
# =========================================================
elif "Trip Map" in page:

    st.markdown("## Trip Map — NYC Citi Bike 2022")
    st.caption("Geospatial view of trip origins, destinations, and movement arcs. Built with Kepler.gl.")

    col1, col2, col3 = st.columns(3)
    col1.markdown("""
<div style="background:#1e1e1e;border:1px solid #2e2e2e;padding:12px 16px;">
<div style="font-family:monospace;font-size:11px;color:#888;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Layer 1</div>
<div style="color:#3dd68c;font-size:13px;font-weight:600;margin-bottom:4px;">&#9679; Start stations</div>
<div style="color:#888;font-size:12px;line-height:1.5;">Trip origin points — size and colour scale with trip volume</div>
</div>
""", unsafe_allow_html=True)

    col2.markdown("""
<div style="background:#1e1e1e;border:1px solid #2e2e2e;padding:12px 16px;">
<div style="font-family:monospace;font-size:11px;color:#888;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Layer 2</div>
<div style="color:#f0c040;font-size:13px;font-weight:600;margin-bottom:4px;">&#9679; End stations</div>
<div style="color:#888;font-size:12px;line-height:1.5;">Trip destination points — reveals where bikes accumulate</div>
</div>
""", unsafe_allow_html=True)

    col3.markdown("""
<div style="background:#1e1e1e;border:1px solid #2e2e2e;padding:12px 16px;">
<div style="font-family:monospace;font-size:11px;color:#888;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Layer 3</div>
<div style="color:#00d4ff;font-size:13px;font-weight:600;margin-bottom:4px;">&#11835; Trip arcs</div>
<div style="color:#888;font-size:12px;line-height:1.5;">Arc thickness and colour = trip frequency between station pairs</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    if os.path.exists(MAP_PATH):
        with open(MAP_PATH, "r", encoding="utf-8") as f:
            map_html = f.read()
        components.html(map_html, height=700, scrolling=True)
    else:
        st.warning("kepler_map.html not found. Make sure it is in the same folder as app.py.")

    st.markdown("""
### What this tells us

The map renders three layers: **start stations** (green), **end stations** (yellow), 
and **trip arcs** connecting the most common origin-destination pairs. 
Arc thickness and colour scale with trip frequency between each station pair.

All high-volume activity concentrates in **central Manhattan** — the business district, 
Hudson waterfront corridor, and major transit hub areas. The arc layer makes commuter 
patterns readable: thick arcs between nearby midtown stations confirm short-distance, 
high-frequency commuter usage rather than cross-borough journeys.

Secondary clusters appear along the **Hudson waterfront** and into **Brooklyn** — 
movement corridors invisible in station-level bar charts.

**Operational implication:** These spatial hotspots are the highest-priority candidates 
for more frequent restocking, higher dock capacity, and targeted monitoring. The arc 
layer identifies which specific station *pairs* drive the most volume — useful for 
targeted rebalancing between origin and destination clusters.
""")


# =========================================================
# PAGE: RECOMMENDATIONS
# =========================================================
elif "Recommendations" in page:

    st.markdown("## Operational Recommendations")
    st.caption("All recommendations derived directly from the dashboard data.")

    if not os.path.exists(DAILY_PATH) or not os.path.exists(STATION_PATH):
        st.error("Data files not found.")
    else:
        df      = load_daily(DAILY_PATH)
        top10   = load_stations(STATION_PATH)

        df["month"] = df["date"].dt.month
        monthly_avg = df.groupby("month")["daily_ride_count"].mean()

        peak_month = int(monthly_avg.idxmax())
        low_month  = int(monthly_avg.idxmin())
        peak_val   = float(monthly_avg.max())
        low_val    = float(monthly_avg.min())

        winter_avg = float(df[df["month"].isin([11,12,1,2,3,4])]["daily_ride_count"].mean())
        summer_avg = float(df[df["month"].isin([6,7,8])]["daily_ride_count"].mean())
        ratio_pct  = (winter_avg / summer_avg) * 100
        reduce_pct = 100 - ratio_pct

        month_names = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                       7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}

        col1, col2, col3 = st.columns(3)
        col1.metric("Peak month", month_names[peak_month], f"{peak_val:,.0f} rides/day avg")
        col2.metric("Lowest month", month_names[low_month], f"{low_val:,.0f} rides/day avg")
        col3.metric("Winter vs Summer demand", f"{ratio_pct:.0f}%", f"−{reduce_pct:.0f}% in winter")

        st.markdown("---")

        st.markdown(f"""
## 1) Prioritize the top 10 Manhattan stations for rebalancing

The station chart shows all top-10 start stations are in central Manhattan. 
**{top10.iloc[-1]["start_station_name"]}** alone generated 
{int(top10.iloc[-1]["trip_count"]):,} trip starts in 2022.

**Actions:**
- Increase rebalancing frequency at these 10 stations
- Add early morning restocking before commute peaks (7–9 AM)
- Run mid-day check cycles for the top 5 busiest stations
- Consider higher dock capacity at #1–3

---

## 2) Scale operations seasonally based on the 50% winter/summer ratio

Winter demand (Nov–Apr) averages **{ratio_pct:.0f}%** of summer demand (Jun–Aug).

**Actions:**
- Reduce redistribution intensity by ~{reduce_pct:.0f}% in winter (Nov–Apr), then fine-tune by station
- Begin summer ramp-up in **late April** — ridership climbs steeply from May onward
- Use **{month_names[peak_month]}** peak as the staffing high-water mark for planning

---

## 3) Use temperature forecasts as a daily demand signal

The scatter analysis confirms a strong positive relationship between temperature and daily 
ridership. Cold snaps reliably depress demand; warm stretches reliably increase it.

**Actions:**
- Integrate NOAA daily forecasts into supply planning
- Pre-position extra bikes before forecasted warm weekends
- Reduce active redistribution cycles on forecasted cold or wet days

---

## 4) Investigate waterfront and Brooklyn expansion corridors

The Kepler.gl map shows secondary clusters forming along the Hudson waterfront and into 
Brooklyn — movement corridors invisible in station-level aggregates.

**Actions:**
- Compare demand intensity near the waterfront vs. existing station coverage
- Use trip flow data to identify under-served origin/destination pairs
- Prioritize new station placement where cluster density exceeds current dock availability
""")
