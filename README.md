# Methane Emissions Predictor

This Streamlit app predicts methane emissions based on facility characteristics and climate parameters.

## Features
- Predicts annual CH4 emissions in tonnes/year
- Takes into account:
  - Facility information (location, sector, etc.)
  - Climate parameters (temperature, wind, rainfall)
  - Interaction terms

## How to Run Locally

1. Clone this repository
2. Install the requirements:
```bash
pip install -r requirements.txt
```
3. Run the Streamlit app:
```bash
streamlit run methane_prediction_app.py
```

## Input Parameters

- Year (2018-2023)
- Latitude (49.0-61.0)
- Longitude (-8.0-2.0)
- Sector (Oil&Gas, Power, Waste, Chemical)
- UK Region (North, Midlands, South, Scotland, Wales)
- Climate parameters for winter and annual periods:
  - Temperature
  - Wind speed
  - Rainfall
  - Pressure 