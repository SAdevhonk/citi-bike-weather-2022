# CitiBike 2022 & Weather Impact Analysis  
## Interactive Operational Dashboard (Streamlit)

---

## 🔗 Live Dashboard

**Streamlit App:**  
https://citi-bike-weather-2022-f2zr3j3vwcsdu7c5vd84m.streamlit.app/

---

## 📌 Project Overview

This project analyzes CitiBike trip data from New York City in 2022 to support **bike supply and rebalancing strategy decisions**.

CitiBike trip records were merged with NOAA daily weather data from LaGuardia Airport to evaluate:

- Seasonal demand fluctuations  
- Temperature impact on ridership  
- Monthly scaling requirements  
- High-demand station concentration  
- Spatial demand clustering  

The final result is a fully deployed multi-page Streamlit dashboard designed to support operational decision-making.

---

## ❓ Business Questions

1. How should CitiBike scale operations between winter and summer months?
2. Which stations require the highest rebalancing priority?
3. How strongly does temperature influence daily ride volume?
4. Where are the strongest geographic ride clusters?

---

## 📊 Data Sources

### 🚲 CitiBike Data
- **Source:** NYC CitiBike System Data  
- **Year:** 2022  
- **Data Type:** Individual trip records  
- **Processing:** Monthly ZIP files extracted and aggregated to daily counts  

### 🌦 Weather Data
- **Source:** NOAA (National Oceanic and Atmospheric Administration)  
- **Station:** USW00014732 (LaGuardia Airport)  
- **Dataset:** GHCND Daily Summaries  

**Weather Variables Used:**
- `TAVG` – Average Temperature  
- `TMIN` – Minimum Temperature  
- `TMAX` – Maximum Temperature  
- `PRCP` – Precipitation  

---

## 🧪 Methodology

1. Combined monthly CitiBike trip files.
2. Aggregated individual rides to daily ride counts.
3. Retrieved NOAA weather data via API.
4. Cleaned and reshaped weather data.
5. Merged daily ride counts with daily weather metrics.
6. Built interactive visualizations with Plotly.
7. Created a multi-page Streamlit dashboard.
8. Added spatial visualization using Kepler.gl.
9. Deployed the dashboard to Streamlit Cloud.

---

## 📈 Dashboard Pages

### 1️⃣ Introduction
Project objectives and operational context.

### 2️⃣ Popular Stations
- Top 10 start stations (interactive bar chart)
- Highlights concentrated demand in Manhattan

### 3️⃣ Trips vs Temperature
- Dual-axis interactive Plotly line chart
- Demonstrates strong seasonal demand patterns

### 4️⃣ Monthly Trends
- Average daily rides per month
- Quantifies peak vs low-demand months
- Enables seasonal scaling decisions

### 5️⃣ Trip Map
- Interactive Kepler.gl visualization
- Identifies geographic demand clusters

### 6️⃣ Recommendations
- Data-backed operational scaling suggestions
- Quantified winter vs summer demand differences
- Station prioritization strategy

---

## 🔎 Key Insights

- Ridership increases significantly as temperatures rise.
- Peak demand occurs in August (~115k avg rides/day).
- Lowest demand occurs in January (~33k avg rides/day).
- Winter demand (Nov–Apr) averages roughly **50% of summer demand**, supporting seasonal scaling.
- Manhattan stations dominate usage and require priority rebalancing.
- Spatial clustering confirms high commuter and business district concentration.

---

## ▶️ How to Run Locally

1. Clone this repository.
2. Navigate to the project folder.
3. Create and activate a virtual environment.
4. Install dependencies:
```
pip install -r requirements.txt
```
5. Run the dashboard:
```
streamlit run app_part_2.py
```
6. Open the provided local URL.

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
├── app_part_2.py
├── exercise_2_6_dashboard_plotly.ipynb
├── citibike_2022_daily_with_weather.csv
├── top10_stations_2022.csv
├── kepler_map.html
├── requirements.txt
├── README.md
```
Raw CitiBike monthly files are excluded due to GitHub file size limits.

---

## 🎯 Project Outcome

This project demonstrates:

- Large-scale dataset aggregation
- API integration
- Data cleaning and transformation
- Time-series and seasonal analysis
- Spatial visualization
- Interactive dashboard development
- Cloud deployment
- Data-driven operational recommendation design

It showcases end-to-end data analytics and business-oriented dashboard engineering using Python.