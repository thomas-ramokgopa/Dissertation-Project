import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
import os
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Methane Emissions Predictor",
    page_icon=None,
    layout="wide"
)

# Load the model
@st.cache_resource
def load_model():
    try:
        model_path = Path('xgb_strategic_optuna.pkl')
        if not model_path.exists():
            st.error("Model file not found. Please ensure 'xgb_strategic_optuna.pkl' is in the same directory as this app.")
            st.stop()
        
        # Load model using joblib
        try:
            model = joblib.load(model_path)
            return model
        except Exception as e:
            st.error(f"""
            Failed to load the model: {str(e)}
            This might be due to compatibility issues.
            Please ensure the model was saved with compatible versions.
            """)
            st.stop()
            
    except Exception as e:
        st.error(f"Error accessing model file: {str(e)}")
        st.stop()

# Try to load the model
try:
    with st.spinner('Loading model...'):
        model = load_model()
except Exception as e:
    st.error("Failed to initialize the model. Please check the error messages above.")
    st.stop()

# Title and description
st.title("Methane Emissions Predictor")
st.write("Enter facility and environmental parameters to predict methane emissions.")

# Create two columns for input widgets
col1, col2 = st.columns(2)

with col1:
    st.subheader("Facility Information")
    
    # Basic information
    year = st.number_input("Year", min_value=2018, max_value=2023, value=2023)
    latitude = st.number_input("Latitude", min_value=49.0, max_value=61.0, value=52.0)
    longitude = st.number_input("Longitude", min_value=-8.0, max_value=2.0, value=-2.0)
    
    # Categorical inputs
    sector = st.selectbox(
        "Sector",
        options=["Oil&Gas", "Power", "Waste", "Chemical"]
    )
    
    uk_region = st.selectbox(
        "UK Region",
        options=["North", "Midlands", "South", "Scotland", "Wales"]
    )
    
    facility_count = st.number_input("Facility Count (25km radius)", min_value=0, max_value=100, value=1)

with col2:
    st.subheader("Climate Parameters")
    
    # Winter climate
    mean_temp_winter = st.number_input("Mean Temperature Winter (C)", min_value=-5.0, max_value=15.0, value=5.0)
    mean_wind_winter = st.number_input("Mean Wind Winter (m/s)", min_value=0.0, max_value=20.0, value=8.0)
    total_rainfall_winter = st.number_input("Total Rainfall Winter (mm)", min_value=0.0, max_value=1000.0, value=200.0)
    
    # Annual climate
    mean_temp_annual = st.number_input("Mean Temperature Annual (C)", min_value=0.0, max_value=20.0, value=10.0)
    mean_wind_annual = st.number_input("Mean Wind Annual (m/s)", min_value=0.0, max_value=15.0, value=6.0)
    total_rainfall_annual = st.number_input("Total Rainfall Annual (mm)", min_value=0.0, max_value=3000.0, value=800.0)

# Calculate interaction terms
temp_rain_winter_interaction = mean_temp_winter * total_rainfall_winter
pressure_wind_annual_interaction = mean_wind_annual * st.number_input("Mean Pressure Annual (hPa)", min_value=980.0, max_value=1030.0, value=1013.0)

# Create prediction button
if st.button("Predict Emissions"):
    try:
        # Create input data
        input_data = pd.DataFrame({
            'Year': [year],
            'Latitude': [latitude],
            'Longitude': [longitude],
            'Sector': [sector],
            'UK_Region': [uk_region],
            'mean_temperature_winter': [mean_temp_winter],
            'mean_wind_winter': [mean_wind_winter],
            'total_rainfall_winter': [total_rainfall_winter],
            'mean_temperature_annual': [mean_temp_annual],
            'mean_wind_annual': [mean_wind_annual],
            'total_rainfall_annual': [total_rainfall_annual],
            'mean_temperature_winter_X_total_rainfall_winter': [temp_rain_winter_interaction],
            'mean_pressure_annual_X_mean_wind_annual': [pressure_wind_annual_interaction],
            'Facility_Count_25km': [facility_count]
        })
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        
        # Display prediction
        st.success("Predicted Methane Emissions")
        st.metric(
            label="Annual CH4 Emissions",
            value=f"{prediction:.2f} tonnes/year"
        )
        
        # Add some context
        st.info("""
        Note: This prediction is based on historical data and environmental parameters.
        Actual emissions may vary based on additional factors not captured in this model.
        """)
        
    except Exception as e:
        st.error(f"An error occurred during prediction: {str(e)}")
        st.info("Please check if all input values are within expected ranges.")

# Add footer with information
st.markdown("---")
st.markdown("""
    **About this tool:**
    - Uses an XGBoost model trained on historical methane emissions data
    - Combines facility characteristics with climate parameters
    - Predictions are in tonnes of CH4 per year
""") 