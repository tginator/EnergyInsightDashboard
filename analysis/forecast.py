import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def forecast_emissions_intensity(df, months_ahead=6):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])

    # Sort by date to prepare time series
    df.sort_values('date', inplace=True)

    # Feature Engineering on Historical Data
    df['time_index'] = np.arange(len(df))  # Time progression

    df['month'] = df['date'].dt.month
    df['sin_month'] = np.sin(2 * np.pi * df['month'] / 12)
    df['cos_month'] = np.cos(2 * np.pi * df['month'] / 12)

    df['temperature_mean'] = df['temperaturemean-c']  # Adjust column name as needed

    # target and features
    y = df['emissionsintensity-kgco₂e/mwh']
    X = df[['time_index', 'sin_month', 'cos_month', 'temperature_mean']]

    # Fit the model
    model = LinearRegression()
    model.fit(X, y)

    # Generate Future Inputs
    future_index = np.arange(len(df), len(df) + months_ahead)
    future_dates = pd.date_range(df['date'].max() + pd.DateOffset(months=1), periods=months_ahead, freq='MS')

    future_months = future_dates.month
    sin_month = np.sin(2 * np.pi * future_months / 12)
    cos_month = np.cos(2 * np.pi * future_months / 12)

    # the last 6 temperature means as a rough estimate
    recent_temps = df['temperature_mean'].tail(6).tolist()
    temp_forecast = (recent_temps * ((months_ahead // len(recent_temps)) + 1))[:months_ahead]

    future_df = pd.DataFrame({
        'time_index': future_index,
        'sin_month': sin_month,
        'cos_month': cos_month,
        'temperature_mean': temp_forecast
    })

    # Forecast
    future_predictions = model.predict(future_df)

    # Plot Results
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], y, label='Actual')
    plt.plot(future_dates, future_predictions, linestyle='--', color='orange', label='Forecast')
    plt.title(f'Forecasted Emissions Intensity ({months_ahead} Months Ahead)')
    plt.ylabel('Emissions Intensity (kgCO2e/MWh)')
    plt.xlabel('Date')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # --- Return Forecast Table ---
    return pd.DataFrame({
        'date': future_dates,
        'forecasted_emissions_intensity': future_predictions
    })
