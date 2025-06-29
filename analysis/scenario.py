import pandas as pd 

def simulate_policy(df, changes):
    """ Apply percentage changes to energy sources and recalculate impact
    
        Param:
        df: DataFrame containing energy data
        changes: Dictionary of source changes (... 'Coal: -0.1, 'Solar: +0.2)

        Retruns:
        Dataframe with updated generation, emissions and intensity
    """

    # For our simualtions
    df_sim = df.copy()

    # Apply changes to the energy sources using a dictionary
    for source, change in changes.items():
        if source in df_sim.columns:
            df_sim[source] *= (1 + change)

    # Gathering our columns for recalculation
    gen_cols = ['coal-gwh', 'gas-gwh', 'wind-gwh', 'solar-gwh', 'hydro-gwh', 'bioenergy-gwh', 'distillate-gwh', 'battery(discharging)-gwh']
    emis_cols = ['coalemissionsvol-tco₂e', 'gasemissionsvol-tco₂e', 'bioenergyemissionsvol-tco₂e', 'distillateemissionsvol-tco₂e']


    # TO BE IMPLEMENTED: Impact on emissions given a change in generation of a source 
    df_sim['total generation (GWh)'] = df_sim[gen_cols].sum(axis=1)
    df_sim['total emissions (tCO2)'] = df_sim[emis_cols].sum(axis=1)
    
    # Recalculate emissions intensity
    df_sim['emissionsintensity-kgco₂e/mwh'] = ((df_sim['total emissions (tCO2)'] * 1000) / (df_sim['total generation (GWh)'] * 1000))

    return df_sim 