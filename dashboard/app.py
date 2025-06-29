import streamlit as st
import pandas as pd
from analysis.preprocess import load_and_clean_data
from analysis.scenario import simulate_policy
from analysis.forecast import forecast_emissions_intensity
from visuals.energy_insights import (
    plot_energy_insights, plot_emissions_trend, plot_clean_vs_fossil_share)

df = load_and_clean_data("data/WA-energy-consumption.csv")
st.title("WA Energy Emissions & Forecasting Dashboard")

# Section 1: Trend Overview

st.header("Monthly electricity generation by source (GWh)")
st.text("This chart shows the total generation of electricity in Westerm Australia from 2013-2025 June by source, including coal, gas, wind, solar, hydro, bioenergy, distillate, and battery discharging.")
st.pyplot(plot_energy_insights(df))

st.header("Energy Usage & Emissions Overview")
st.line_chart(df.set_index('date')[['total generation (GWh)', 'total emissions (tCO2)']])

# Section 2: Forecasting
st.header("Forecasting Emissions Intensity")
months = st.slider("Select months to forecast", 3, 12, 6)
forecast_df = forecast_emissions_intensity(df, months_ahead=months)
st.line_chart(forecast_df.set_index('date'))

# Section 3: Scenario simulation
st.header("Energy Change Simulation")

col1, col2 = st.columns(2)

with col1:
    coal_change = st.slider("Coal Change (%)", -100.0, 100.0, 0.0)
    gas_change = st.slider("Gas Change (%)", -100.0, 100.0, 0.0)

with col2:
    solar_change = st.slider("Solar Change (%)", -100.0, 100.0, 0.0)
    wind_change = st.slider("Wind Change (%)", -100.0, 100.0, 0.0)

# Run changes:
changes = {
    'coal-gwh': coal_change / 100,
    'gas-gwh': gas_change / 100,
    'solar-gwh': solar_change / 100,
    'wind-gwh': wind_change / 100
}

df_sim = simulate_policy(df, changes)

# Comparison:
st.subheader("Comparison of Original vs Simulated Emissions Intensity")
colA, colB = st.columns(2)
with colA:
    st.metric("Original Avg Intensity (kgCO2e/MWh)", round(df['emissionsintensity-kgco₂e/mwh'].mean(), 2))
with colB:
    st.metric("Simulated Avg Intensity (kgCO2e/MWh)", round(df_sim['emissionsintensity-kgco₂e/mwh'].mean(), 2))



# Display clean vs fossil energy share
st.line_chart(df_sim.set_index('date')[['Clean Energy Share (%)', 'Fossil Energy Share (%)']])
