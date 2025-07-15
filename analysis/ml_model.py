import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

def train_emissions_model(df):
    df = df.copy()
    df = ['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    # Time-based features
    df['month'] = df['date'].dt.month
    df['sin_month'] = np.sin(2 * np.pi * df['month'] / 12)
    df['cos_month'] = np.cos(2* np.pi * df['month'] / 12)

    # Temperature
    df['temperature_mean'] = df['temperaturemean-c']

    # Lag feature: previous month's emissions
    df['prev_emissions'] = df['emissionsintensity-kgco₂e/mwh'].shift(1)

    # Drop first row
    df = df.dropna()

    features = [
        'sin_month', 'cos_month',
        'temperature_mean', 'prev_emissions'
        'coal-gwh', 'gas-gwh', 'solar-gwh', 'wind-gwh', 'battery-gwh'
    ]

    X = df[features]
    y = df['emissionsintensity-kgco₂e/mwh']
