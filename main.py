from analysis.preprocess import load_and_clean_data
from visuals.energy_insights import (
    plot_energy_insights, plot_emissions_trend, plot_clean_vs_fossil_share)
from analysis.forecast import forecast_emissions_intensity
from analysis.scenario import simulate_policy

df = load_and_clean_data("data/WA-energy-consumption.csv")

# Uncomment the following lines to visualize the data: 

# plot_energy_insights(df)
# plot_emissions_trend(df)
# plot_clean_vs_fossil_share(df)

# forecast_df = forecast_emissions_intensity(df, months_ahead=6)
# print(forecast_df)


# Define your scenario for policy simulation
scenario = {
    'coal-gwh': -0.1,  # Decrease coal generation by 10%
    'solar-gwh': 0.2,  # Increase solar generation by 20%
    'gas-gwh': -0.05   # Decrease gas generation by 5%
}

df_simulated = simulate_policy(df, scenario)

print("Original avg intensity in kgco₂e/mwh:", round(df['emissionsintensity-kgco₂e/mwh'].mean(), 2))
print("Simulated avg intensity in kgco₂e/mwh:", round(df_simulated['emissionsintensity-kgco₂e/mwh'].mean(), 2))


