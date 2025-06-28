import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

def forecast_emissions_intensity(df, months_ahead=6):

    """ Amount of CO2 equivalent emissions is what emissions instensity is based on.
    What can we use forecasting of this for? 
    1. Grid planning 
    2. Net zero policy, emissions targeting
    3. Carbon pricing
    """

    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])

    # sorting our dates
    df.sort_values('date', inplace=True)

    # Using a time index instead of a date for regression calculations
    df['time_index'] = np.arange(len(df))

    # Setting data for regression
    X = df[['time_index']]
    y = df['emissionsintensity-kgco₂e/mwh']

    model = LinearRegression()
    model.fit(X, y)

    # Create future focast and prepare it for scikit-learn
    future_index = np.arange(len(df), len(df) + months_ahead)
    future_df = pd.DataFrame({
        'time_index':future_index})
    future_predictions = model.predict(future_df)

    # Future dates:
    last_date = df['date'].max()
    future_dates = pd.date_range(last_date + pd.DateOffset(months=1), periods=months_ahead, freq='MS')

    # Plot results
    plt.figure(figsize=(10,5))
    plt.plot(df['date'], y, label='Actual')
    plt.plot(future_dates, future_predictions, linestyle='--', color='orange', label='Forecast')
    plt.title(f'Forecasted Emissions Intensity ({months_ahead} months ahead)')
    plt.ylabel('Emissions Intensity (kgCO2e/MWh)')
    plt.xlabel('Date')
    plt.legend()
    plt.tight_layout()
    plt.show()

    return pd.DataFrame({
        'date': future_dates,
        'forecasted_emissions_intensity': future_predictions
    })    






    
