# CitiBike 2022 & Weather Impact Analysis

## Project Overview

This project analyzes CitiBike trip data from New York City in 2022 and investigates how weather conditions influenced daily ridership patterns. The analysis integrates CitiBike trip records with NOAA daily weather data from LaGuardia Airport.

The goal is to understand how temperature and precipitation affect bike usage and to identify seasonal and geographic trends in ridership.

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

1. Extracted and combined CitiBike monthly trip files using:
   - List comprehension to generate file paths
   - A generator expression inside `pd.concat()` for memory-efficient merging

2. Cleaned and aggregated trip data to daily ride counts.

3. Retrieved daily weather data using the NOAA API.

4. Cleaned and reshaped weather data from long to wide format.

5. Merged daily ride counts with daily weather data.

6. Exported final merged dataset for dashboard development.

---

## Technologies Used

- Python
- Pandas
- NumPy
- Requests
- JupyterLab

---

## Project Structure

citi-bike-weather-2022/
-
-- citi_bike_weather_2022.ipynb
-- weather_2022_laguardia.csv
-- citibike_2022_daily_with_weather.csv
-- README.md
-- data/  (raw files excluded from GitHub due to size limits)

---

## Final Output

The final dataset `citibike_2022_daily_with_weather.csv` contains:

- Date
- Daily ride count
- Daily precipitation
- Daily average temperature
- Daily minimum temperature
- Daily maximum temperature

This dataset serves as the foundation for the final dashboard visualization.
