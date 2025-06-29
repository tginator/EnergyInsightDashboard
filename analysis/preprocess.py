import pandas as pd
import os

def load_and_clean_data(file_path):
   
   df = pd.read_csv(file_path)

   df['date'] = pd.to_datetime(df['date'], errors='coerce')

   df.columns = df.columns.str.strip().str.replace(r'\s+', '', regex=True).str.lower()

   print("hi")
   print(os.getcwd())

   # Total generation giga watt-hours
   gen_cols = ['coal-gwh', 'gas-gwh', 'wind-gwh', 'solar-gwh', 'hydro-gwh', 'bioenergy-gwh', 'distillate-gwh',
                'battery(discharging)-gwh']
   df['total generation (GWh)'] = df[gen_cols].sum(axis=1)

   # Total emissions 
   emis_cols = ['coalemissionsvol-tco₂e', 'gasemissionsvol-tco₂e', 'bioenergyemissionsvol-tco₂e', 'distillateemissionsvol-tco₂e']
   df['total emissions (tCO2)'] = df[emis_cols].sum(axis=1)

   # Create Clean Energy % 
   df['Clean Energy Share (%)'] = (df[['wind-gwh', 'solar-gwh', 'hydro-gwh', 'battery(discharging)-gwh']].sum(axis=1) / df['total generation (GWh)']) * 100

   # Create Fossil Energy % 
   df['Fossil Energy Share (%)'] = (df[['coal-gwh', 'gas-gwh', 'distillate-gwh']].sum(axis=1) / df['total generation (GWh)']) * 100

   return df

if __name__ == "__main__":
    path = "data/WA-energy-consumption.csv"
    df_cleaned = load_and_clean_data(path)
    df_cleaned.info()
    print(df_cleaned.head())