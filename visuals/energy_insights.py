import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Functions to plot energy insights and trends

def plot_energy_insights(df):

    sources = ['coal-gwh', 'gas-gwh', 'wind-gwh', 'solar-gwh', 'hydro-gwh', 'bioenergy-gwh', 'distillate-gwh', 'battery(discharging)-gwh']

    df.set_index('date', inplace=True)

    # Plotting the total generation over time stacked on each other
    df[sources].plot(kind='area', stacked=True, figsize=(12, 6),alpha=0.7)

    plt.title('Monthly Electricity Generation by Source (GWh)')
    plt.ylabel('GWh')
    plt.xlabel('Date')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()
    df.reset_index(inplace=True)

def plot_emissions_trend(df):

    plt.figure(figsize=(10,5))
    sns.lineplot(x='date', y='total emissions (tCO2)', data=df, label='Emissions')

    plt.xlim(df['date'].min(), df['date'].max())
    plt.title('Total Emissions Over Time (tCO2)')
    plt.ylabel('Emissions (tCO2)')
    plt.xlabel('Date')
    plt.tight_layout()
    plt.show()

def plot_clean_vs_fossil_share(df):    

    plt.figure(figsize=(10, 5))
    sns.lineplot(x='date', y='clean energy share (%)', data=df, label='Clean Energy Share (%)')
    sns.lineplot(x='date', y='Fossil Energy Share (%)', data=df, label='Fossil Energy Share (%)')
    plt.title('Clean vs Fossil Energy Share Over Time')

    plt.xlim(df['date'].min(), df['date'].max())

    plt.ylabel('Energy Share (%)')
    plt.xlabel('Date')
    plt.legend()
    plt.tight_layout()
    plt.show()

