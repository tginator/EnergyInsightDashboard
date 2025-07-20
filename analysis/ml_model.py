import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

def train_emissions_model(df):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
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
        'temperature_mean', 'prev_emissions',
        'coal-gwh', 'gas-gwh', 'solar-gwh', 'wind-gwh',
        'distillate-gwh', 'battery(discharging)-gwh', 'battery(charging)-gwh'
    ]

    X = df[features]
    y = df['emissionsintensity-kgco₂e/mwh']

    # Split for testing model performance
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    results_df = df.loc[X_test.index, ['date']].copy()
    results_df['actual'] = y_test.values
    results_df['predicted'] = y_pred

     # Create SHAP values (only on small sample for speed)
    import shap
    sample_X = X_test.sample(n=min(100, len(X_test)), random_state=42)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(sample_X)

    return model, rmse, results_df, shap_values, sample_X






