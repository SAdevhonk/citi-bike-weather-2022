# CitiBike 2022 & Weather Impact Analysis  
## Interactive Dashboard with Streamlit

---

## 🔗 Live Dashboard

**Streamlit App:**  
https://citi-bike-weather-2022-f2zr3j3vwcsdu7c5vd84m.streamlit.app/

---

## 📌 Project Overview

This project analyzes CitiBike trip data from New York City in 2022 and investigates how weather conditions influenced daily ridership patterns.

CitiBike trip records were merged with NOAA daily weather data from LaGuardia Airport to examine:

- Seasonal trends  
- Temperature effects  
- Precipitation impact  
- Spatial ride distribution  

The final result is a fully deployed interactive Streamlit dashboard.

---

## ❓ Research Questions

1. How does precipitation affect daily CitiBike ridership?
2. Is there a correlation between average daily temperature and ride volume?
3. How does ridership vary across months and seasons in 2022?
4. Which start stations are the most popular, and where are the busiest geographic areas?

---

## 📊 Data Sources

### 🚲 CitiBike Data
- **Source:** NYC CitiBike System Data  
- **Year:** 2022  
- **Data Type:** Individual trip records  
- **Processing:** Monthly ZIP files extracted and combined into a unified dataset  

### 🌦 Weather Data
- **Source:** NOAA (National Oceanic and Atmospheric Administration)  
- **Station:** USW00014732 (LaGuardia Airport)  
- **Dataset:** GHCND Daily Summaries  

**Variables Used:**
- `TAVG` – Average Temperature  
- `TMIN` – Minimum Temperature  
- `TMAX` – Maximum Temperature  
- `PRCP` – Precipitation  

---

## 🧪 Methodology

1. Extracted and combined monthly CitiBike trip files.
2. Cleaned trip data and aggregated to daily ride counts.
3. Retrieved weather data via the NOAA API.
4. Reshaped weather data from long to wide format.
5. Merged daily ride counts with daily weather metrics.
6. Exported the final merged dataset.
7. Built interactive visualizations using Plotly.
8. Integrated visualizations and Kepler.gl map into a multi-page Streamlit dashboard.
9. Deployed the dashboard to Streamlit Cloud.

---

## 📈 Dashboard Pages

### 1️⃣ Introduction
Project background, objectives, and analytical context.

### 2️⃣ Popular Stations
- Horizontal bar chart of top 10 start stations  
- Color-scaled by ride volume  
- Highlights concentrated demand in Manhattan  

### 3️⃣ Trips vs Temperature
- Dual-axis Plotly line chart  
- Daily ride count vs average temperature  
- Seasonal ridership patterns clearly visible  

### 4️⃣ Trip Map
- Interactive Kepler.gl spatial visualization  
- Displays trip flows between stations  
- Identifies geographic demand clusters  

### 5️⃣ Recommendations
Operational suggestions based on analytical findings.

---

## 🔎 Key Insights

- CitiBike usage increases significantly as temperatures rise above ~15°C.
- Peak ridership occurs during summer months (June–August).
- Cold-weather months show substantial ridership decline.
- Midtown and central Manhattan dominate trip volume.
- Precipitation slightly suppresses daily ridership, but temperature is the stronger predictor.
- Spatial patterns reveal strong clustering in central business districts.

---

## ▶️ How to Run Locally

1. Clone this repository.
2. Navigate to the project folder.
3. Create and activate a virtual environment.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the app:
```
streamlit run app.py
```

6. Open the provided local URL (e.g., http://localhost:8501).

---
## 🛠 Technologies Used
- Python
- Pandas
- Plotly
- Streamlit
- Kepler.gl
- NOAA API
- Jupyter Notebook

---

## 📂 Project Structure

```
citi-bike-weather-2022/
│
├── app.py
├── app_part_2.py
├── exercise_2_6_dashboard_plotly.ipynb
├── citibike_2022_daily_with_weather.csv
├── kepler_map.html
├── requirements.txt
├── README.md
```
Raw CitiBike monthly files are excluded due to GitHub file size limits.

---

## 📁 Final Dataset

`citibike_2022_daily_with_weather.csv` contains:
- Date
- Daily ride count
- Daily precipitation
- Daily average temperature
- Daily minimum temperature
- Daily maximum temperature

This dataset forms the analytical backbone of the dashboard.

---

## 🎯 Project Outcome

This project demonstrates:
- Large dataset aggregation
- API data integration
- Data cleaning and transformation
- Time series analysis
- Spatial visualization
- Interactive dashboard development
- Cloud deployment

It showcases end-to-end data analysis and dashboard engineering using Python.

---