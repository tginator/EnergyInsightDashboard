import pandas as pd

def load_and_clean_data(file_path):
   
   df = pd.read_csv(file_path)

   df['date'] = pd.to_datetime(df['date'], errors='coerce')

   df.columns = df.columns.str.strip().str.replace(r'\s+', '', regex=True).str.lower()

   # Total generation giga watt-hours

   df.head()