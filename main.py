from analysis.preprocess import load_and_clean_data
from visuals.energy_insights import (
    plot_energy_insights, plot_emissions_trend, plot_clean_vs_fossil_share)

df = load_and_clean_data("data/WA-energy-consumption.csv")

plot_energy_insights(df)
plot_emissions_trend(df)
plot_clean_vs_fossil_share(df)

