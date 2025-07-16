import streamlit as st
import pandas as pd
from analysis.preprocess import load_and_clean_data
from analysis.scenario import simulate_policy
from analysis.forecast import forecast_emissions_intensity
from analysis.ml_model import train_emissions_model
from visuals.energy_insights import (
    plot_energy_insights, plot_emissions_trend, plot_clean_vs_fossil_share)

df = load_and_clean_data("data/WA-energy-consumption.csv")
st.title("WA Energy Emissions & Forecasting Dashboard")



# Section 1: Trend Overview

st.header("Monthly electricity generation by source (GWh)")
st.text("This chart shows the total generation of electricity in Westerm Australia from 2013-2025 June by source, including coal, gas, wind, solar, hydro, bioenergy, distillate, and battery discharging.")
fig = plot_energy_insights(df)
st.pyplot(fig)

# For better visualization, we convert GWh to MW for this graph
df_mw = df.copy()
df_mw['total generation (MWh)'] = (df_mw['total generation (GWh)'] * 1000)

st.header("Energy Usage & Emissions Overview")
st.line_chart(df_mw.set_index('date')[['total generation (MWh)', 'total emissions (tCO2)']])




# Section 2: Forecasting

st.header("Forecasting Emissions Intensity")
st.text("This emissions intensity " \
"forecast estimates the next few months of carbon emissions per unit of electricity (kgCO₂e/MWh).It uses historical trends, seasonal patterns (monthly cycles), and average temperatures to predict how emissions may evolve based on past behavior.")
months = st.slider("Select months to forecast", 3, 12, 6)

# Generate forecast
forecast_df = forecast_emissions_intensity(df, months_ahead=months)

# Prepare actual emissions
actual = df[['date', 'emissionsintensity-kgco₂e/mwh']].copy()
actual = actual.rename(columns={'emissionsintensity-kgco₂e/mwh': 'Emissions Intensity (Actual)'})
actual.set_index('date', inplace=True)

# Prepare forecast emissions
forecast_df = forecast_df.rename(columns={'forecasted_emissions_intensity': 'Emissions Intensity (Forecast)'})
forecast_df.set_index('date', inplace=True)

# Combine actual and forecast
combined = pd.concat([actual, forecast_df])

# Plot both lines
st.line_chart(combined)

st.subheader("Download Forecasted Data")
st.download_button(
    label="Download Forecasted Emissions Intensity (CSV)",
    data=forecast_df.to_csv(index=False),
    file_name='forecasted_emissions_intensity.csv',
    mime='text/csv'
)

# Machine learning model using randomforestregressor
st.header("ML: Emissions prediction")
st.text("This model uses Random Forest to predict carbon intensity based on fuel mix, temperature, and seasonal signals.")

model, rmse, results_df = train_emissions_model(df)
st.metric("Model RMSE (kgCO₂e/MWh)", round(rmse, 2))

# Line chart... actual vs predicted
st.subheader("Actual vs Predicted Emissions Intensity")
st.line_chart(results_df.set_index('date')[['actual','predicted']])



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

st.subheader("Clean vs Fossil Energy Share Over Time")
st.line_chart(df_sim.set_index('date')[['Clean Energy Share (%)', 'Fossil Energy Share (%)']])
