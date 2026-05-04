# NYC Citi Bike Dashboard (2022)

Operational supply and rebalancing intelligence from 1.7 million NYC Citi Bike trip records, enriched with NOAA daily weather data and deployed as an interactive Streamlit dashboard.

## Overview

This project answers one question: how should Citi Bike scale bike supply and rebalancing operations across the year — and which stations, seasons, and environmental factors drive that decision?

Starting from 12 monthly ZIP files of raw trip records and daily weather data retrieved via the NOAA API, the pipeline produces a fully deployed multi-page dashboard that quantifies seasonal demand, temperature correlation, station-level concentration, and geospatial trip clusters.

**Result:** 1.7 million trip records aggregated to daily level, merged with 365 days of NOAA weather, and deployed across 7 interactive dashboard pages — with winter demand measured at 50% of summer demand and the top 10 stations all confirmed in central Manhattan.

## Pipeline

Data Acquisition (Citi Bike ZIPs + NOAA API) → Extraction (zipfile + generator-based pd.concat) → Cleaning (timestamp parsing, 2022 filter, NOAA long→wide pivot) → Aggregation (1.7M rows → daily ride counts) → Merge (inner join on date) → Visualization (Plotly + Matplotlib + Seaborn + Kepler.gl) → Dashboard (Streamlit, 7 pages) → Deployment (Streamlit Cloud)

## Notebooks

| Notebook | Description |
|---|---|
| citi_bike_weather_2022.ipynb | Data acquisition, cleaning, aggregation, NOAA API merge |
| exercise_2_3_visualizations.ipynb | Matplotlib/Seaborn EDA: time series, dual-axis, distributions |
| exercise_2_4_seaborn_visualizations.ipynb | Seaborn scatter, regression, and seasonal breakdowns |
| exercise_2_5_kepler_map.ipynb | Kepler.gl spatial map of trip origins and arcs |
| exercise_2_6_dashboard_plotly.ipynb | Plotly interactive charts and Streamlit dashboard assembly |

## Key Findings

**1. Winter demand is ~50% of summer demand**
Monthly averages show a 3x+ spread between peak (August, ~115K rides/day) and trough (January, ~33K rides/day). Winter (Nov–Apr) averages roughly half of summer (Jun–Aug) — a direct, quantified baseline for seasonal scaling decisions.

**2. Temperature is a reliable demand predictor**
Daily rides track average temperature closely across the full year. Cold snaps reliably depress demand; warm stretches reliably increase it. NOAA forecasts could be operationalized as a forward-looking supply signal.

**3. All top-10 stations are in central Manhattan**
The highest-volume start station — W 21 St & 6 Ave — generated 128,436 trip starts in 2022. All top-10 stations are concentrated in a narrow Manhattan corridor, making them high-priority candidates for increased dock capacity and rebalancing frequency.

**4. Spatial clusters confirm hotspots beyond station rankings**
The Kepler.gl map reveals dense trip clusters in Manhattan's business district and the Hudson waterfront corridor, with secondary clusters forming in Brooklyn — movement patterns invisible in station-level aggregates alone.

**5. Generator-based loading is required at 1.7M row scale**
Loading 12 monthly CSVs naively would double memory usage. Using a generator expression inside pd.concat() streams each file sequentially — essential for large-scale local data work without a database.

## Dashboard Pages

| Page | Content |
|---|---|
| Introduction | Project context, business questions, data pipeline summary, key metrics |
| Popular Stations | Top 10 start stations bar chart — all in central Manhattan |
| Trips vs Temperature | Dual-axis time series: daily rides + NOAA average temperature |
| Monthly Trends | Season-coloured bar chart with winter/summer reference lines |
| Temperature Scatter | Scatter plot with trend line, Pearson r, and rides-per-degree slope |
| Trip Map | Kepler.gl interactive map: start points, end points, trip arcs |
| Recommendations | Live computed metrics + 4 data-backed operational recommendations |

## Live Dashboard

https://citi-bike-weather-2022-f2zr3j3vwcsduf7c5vd84m.streamlit.app/

## Dataset Scale

| Metric | Value |
|---|---|
| Individual trip records | ~1.7 million |
| Monthly source files | 12 ZIP files |
| Merged daily dataset | 365 rows x 6 columns |
| Top station trip count | 128,436 (W 21 St & 6 Ave) |
| Peak daily demand | ~115,000 rides/day (August) |
| Lowest daily demand | ~33,000 rides/day (January) |
| Weather station | USW00014732 — LaGuardia Airport |
| Weather variables | TAVG, TMIN, TMAX, PRCP |

## Data Files

| File | Description |
|---|---|
| citibike_2022_daily_with_weather.csv | Daily ride counts merged with NOAA weather (365 rows) |
| top10_stations_2022.csv | Top 10 start stations with trip counts |
| kepler_map.html | Pre-rendered Kepler.gl interactive map (12MB) |
| reduced_data_2022.csv | Sample of daily data for lightweight testing |

Raw monthly Citi Bike ZIP files are excluded due to GitHub file size limits. Download from the NYC Citi Bike system data page: https://citibikenyc.com/system-data

## Installation

```
git clone https://github.com/ageelalramadhan/citi-bike-weather-2022.git
cd citi-bike-weather-2022
pip install -r requirements.txt
streamlit run app_part_2.py
```

## Dependencies

- pandas
- - numpy
  - - plotly
    - - streamlit
      - - keplergl
        - - requests
          - - matplotlib
            - - seaborn
             
              - Full pinned versions in requirements.txt.
             
              - ## Portfolio
             
              - Full case study with all charts and findings: https://ageelalramadhan.github.io/citi-bike-case-study.html
             
              - ## Author
             
              - Ageel Alramadhan — Data Analyst · Hamburg
              - LinkedIn: https://www.linkedin.com/in/ageel-alramadhan/
              - Portfolio: https://ageelalramadhan.github.io
              - CareerFoundry Data Analytics Program · DEKRA-certified · AfA-approved · 1221 UE
