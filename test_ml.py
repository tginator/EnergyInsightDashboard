from analysis.preprocess import load_and_clean_data
from analysis.ml_model import train_emissions_model

print("Loading data...")
df = load_and_clean_data("data/WA-energy-consumption.csv")
print(f"Loaded {len(df)} rows")

print("Columns in DataFrame:", df.columns.tolist())


print("Training model...")
model, rmse, test_idx, y_true, y_pred = train_emissions_model(df)

print(f"Model RMSE: {rmse:.2f} kgCO₂e/MWh")
