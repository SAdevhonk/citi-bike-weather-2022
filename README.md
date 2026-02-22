# CitiBike 2022 & Weather Impact Analysis  
## Interactive Dashboard with Streamlit

---

## Project Overview

This project analyzes CitiBike trip data from New York City in 2022 and investigates how weather conditions influenced daily ridership patterns. The analysis integrates CitiBike trip records with NOAA daily weather data from LaGuardia Airport.

The final result is an interactive Streamlit dashboard that visualizes:

- The most popular start stations
- The relationship between temperature and ride volume
- Geographic trip patterns using a Kepler.gl map

---

## Research Questions

1. How does precipitation affect daily CitiBike ridership?
2. Is there a correlation between average daily temperature and ride volume?
3. How does ridership vary across months and seasons in 2022?
4. Which start stations are the most popular, and where are the busiest geographic areas?

---

## Data Sources

### CitiBike Data
- Source: NYC CitiBike System Data
- Year: 2022
- Data Type: Individual trip records
- Processing: Monthly ZIP files extracted and combined into one dataset using list comprehension and generator expressions.

### Weather Data
- Source: NOAA (National Oceanic and Atmospheric Administration)
- Station: USW00014732 (LaGuardia Airport)
- Dataset: GHCND Daily Summaries
- Variables used:
  - TAVG (Average Temperature)
  - TMIN (Minimum Temperature)
  - TMAX (Maximum Temperature)
  - PRCP (Precipitation)

---

## Methodology

1. Extracted and combined CitiBike monthly trip files.
2. Cleaned and aggregated trip data to daily ride counts.
3. Retrieved daily weather data using the NOAA API.
4. Cleaned and reshaped weather data from long to wide format.
5. Merged daily ride counts with daily weather data.
6. Exported final merged dataset for dashboard development.
7. Built interactive visualizations using Plotly.
8. Integrated charts and Kepler.gl map into a Streamlit dashboard.

---

## Dashboard Features

The Streamlit dashboard includes:

- **Top 10 Start Stations (Plotly Bar Chart)**
  - Horizontal bar chart
  - Color-scaled by ride volume
  - Clearly labeled axes and titles

- **Daily Trips vs Temperature (Dual-Axis Plotly Line Chart)**
  - Ride count on primary axis
  - Temperature on secondary axis
  - Seasonal trends clearly visible

- **Kepler.gl Interactive Map**
  - Visualizes trip flows between stations
  - Highlights busiest geographic zones
  - Fully interactive spatial exploration

---

## How to Run the Dashboard

1. Navigate to the project folder.
2. Activate your virtual environment.
3. Run: streamlit run app.py

---

4. Open the local URL in your browser (e.g., http://localhost:8501).

---

## Technologies Used

- Python
- Pandas
- Plotly
- Streamlit
- Kepler.gl
- NOAA API
- JupyterLab

---

## Project Structure

citi-bike-weather-2022/
│
├── app.py
├── exercise_2_6_dashboard_plotly.ipynb
├── citibike_2022_daily_with_weather.csv
├── kepler_map.html
├── README.md
└── data/ (trip CSV files excluded from repo if >25MB)

Note: Raw CitiBike trip files are excluded from this repository due to GitHub size limitations.

---

## Key Insights

- Midtown Manhattan stations dominate ridership.
- CitiBike usage increases significantly during warmer months.
- Spatial patterns show heavy clustering in central business districts.
- Temperature is positively correlated with daily ride volume.

---

## Final Output

The dataset `citibike_2022_daily_with_weather.csv` serves as the analytical foundation for the dashboard and contains:

- Date
- Daily ride count
- Daily precipitation
- Daily average temperature
- Daily minimum temperature
- Daily maximum temperature

This project demonstrates data cleaning, API integration, aggregation, visualization design, and dashboard deployment in Python.