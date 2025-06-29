# WA Energy Emissions & Forecasting Dashboard
#### This project aims to analyze, forecast, and simulate electricity generation and carbon emissions in Western Australia using real-world past data from the SWIS grid. It helps demonstrate how energy source changes (like increasing solar or reducing coal) can affect emissions intensity and overall grid sustainability. 

## Current Features
- Visualise electricity generation by source over the past 10+ years (2013-2025)
- Track total emissions and emissions intensity
- Forecast future emissions intensity using Linear Regression
- Simualte policy scenarios (such as an +20% solar, -10% coal) and how that would impact emissions intensity
- Download forecast data any energy generation overview

## What can we use this app for?
- Policy planning for grid decarbonisation
- Forecasting future carbon intensity
- Exploring the impact of renewables vs fossil fuels
- ESG/Net-zero analysis for companies like Western Power or Woodside Energy

## Dataset
Source: SWIS Electricty Data - WA Government / Energy Reports
Columns include:
  - Energy generation by source (GWh)
  - Emissions volume by fuel (tCO₂e)
  - Emissions intensity (kgCO₂e/MWh)
  - Market values and temperature (optional) // Currently not in use for any features

## How to Run
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/wa-energy-dashboard.git
   cd wa-energy-dashboard
2. Install dependencies:
   pip install -r requirements.txt
3. streamlit run dashboard/app.py

## Screenshots
