# Import useful libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %% Directory setup
# Set relative path to the data file
base_dir = os.path.dirname(os.path.abspath(__file__))
z_scores_path = os.path.join(base_dir, "data", "data_created", "altman_z_scores.csv")
naive_dd_path = os.path.join(base_dir, "data", "data_created", "distance_to_default.csv")
value_at_risk_path = os.path.join(base_dir, "data", "data_created", "value_at_risk.csv")
# %% Import created measures datasets
z_scores = pd.read_csv(z_scores_path, index_col = 'Year', parse_dates = ['Year'])
naive_dd = pd.read_csv(naive_dd_path, index_col = 'Year', parse_dates = ['Year'])
value_at_risk = pd.read_csv(value_at_risk_path, index_col = 'Year', parse_dates = ['Year'])
# %% Correlations between the 3 risk measures per year

years = [] # To store the year columns
for year in range(2014, 2023):

    years.append(str(year)) 

print(years)

all_correlations = {} # to store correlation matrices per year

for year in years:

    data_year = pd.concat(
        [
            value_at_risk.loc[year].T,
            z_scores.loc[year].T,
            naive_dd.loc[year].T
        ],
        axis=1,
        join='inner'
    )

    data_year.columns = ['VaR', 'Z_Score', 'DD'] # Names of the columns 
    corr_matrix = data_year.corr()
    all_correlations[year] = corr_matrix

    print(f"\nCorrelation Matrix for {year}:\n", corr_matrix.round(3))
# %% Graphical representation of the correlations evolution over time

corr_time = pd.DataFrame({
    'VaR_vs_Z': [all_correlations[year].loc['VaR', 'Z_Score'] for year in years],
    'VaR_vs_DD': [all_correlations[year].loc['VaR', 'DD'] for year in years],
    'Z_vs_DD': [all_correlations[year].loc['Z_Score', 'DD'] for year in years],
}, index=years
)

plt.figure()

plt.plot(corr_time.index, corr_time['VaR_vs_Z'], label='VaR vs Z')
plt.plot(corr_time.index, corr_time['VaR_vs_DD'], label='VaR vs DD')
plt.plot(corr_time.index, corr_time['Z_vs_DD'], label='Z vs DD')

plt.axhline(0, linestyle='--', linewidth=1, color='black')
plt.ylim(-1, 1)
plt.xlabel("Year")
plt.ylabel("Pearson's Correlation")
plt.title("Risk Measures Cross-Sectional Correlations Over Time")
plt.legend(loc='upper right')

plt.savefig("graphs/Correlation_Matrices_Between_Risk_Measures_Per_Year.png", dpi=300, bbox_inches="tight")
plt.close()
