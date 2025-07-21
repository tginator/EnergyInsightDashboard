import pandas as pd 

def simulate_policy(df, changes):
    """ Apply percentage changes to energy sources and recalculate impact realistically
        - Adjusts both generation and emissions for each source
        - Uses historical emissions factors (tCO2e/GWh) for each source
        - Recalculates total emissions and intensity
    """

    df_sim = df.copy()

    # Define mapping from source to generation and emissions columns
    source_map = {
        'coal-gwh': 'coalemissionsvol-tco₂e',
        'gas-gwh': 'gasemissionsvol-tco₂e',
        'bioenergy-gwh': 'bioenergyemissionsvol-tco₂e',
        'distillate-gwh': 'distillateemissionsvol-tco₂e',
        # renewables (wind, solar, hydro, battery) assumed zero emissions
    }

    # Calculate historical emissions factors (tCO2e/GWh) for each source
    emissions_factors = {}
    for gen_col, emis_col in source_map.items():
        # Avoid division by zero
        with pd.option_context('mode.use_inf_as_na', True):
            factor = (df[emis_col] / df[gen_col]).replace([float('inf'), -float('inf')], pd.NA)
            emissions_factors[gen_col] = factor.fillna(0)

    # Apply changes to generation and emissions
    for gen_col, change in changes.items():
        if gen_col in df_sim.columns:
            df_sim[gen_col] = df_sim[gen_col] * (1 + change)
            # If this source has emissions, update emissions using historical factor
            if gen_col in source_map:
                emis_col = source_map[gen_col]
                # Use row-wise historical factor for realism
                df_sim[emis_col] = df_sim[gen_col] * emissions_factors[gen_col]

    # Recalculate totals
    gen_cols = ['coal-gwh', 'gas-gwh', 'wind-gwh', 'solar-gwh', 'hydro-gwh', 'bioenergy-gwh', 'distillate-gwh', 'battery(discharging)-gwh']
    emis_cols = ['coalemissionsvol-tco₂e', 'gasemissionsvol-tco₂e', 'bioenergyemissionsvol-tco₂e', 'distillateemissionsvol-tco₂e']

    df_sim['total generation (GWh)'] = df_sim[gen_cols].sum(axis=1)
    df_sim['total emissions (tCO2)'] = df_sim[emis_cols].sum(axis=1)
    df_sim['emissionsintensity-kgco₂e/mwh'] = ((df_sim['total emissions (tCO2)'] * 1000) / (df_sim['total generation (GWh)'] * 1000))

    # Recalculate clean/fossil shares if needed
    df_sim['Clean Energy Share (%)'] = (df_sim[['wind-gwh', 'solar-gwh', 'hydro-gwh', 'battery(discharging)-gwh']].sum(axis=1) / df_sim['total generation (GWh)']) * 100
    df_sim['Fossil Energy Share (%)'] = (df_sim[['coal-gwh', 'gas-gwh', 'distillate-gwh']].sum(axis=1) / df_sim['total generation (GWh)']) * 100

    return df_sim 