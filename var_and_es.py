# Import useful libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %%
print(os.getcwd()) # get current working directory
# Set the directory to the path of the folder you saved the project
dir = "C:/Users/30697/Desktop/Projects/default and market risk of public us companies" 
os.chdir(dir)
# %%
# Import created daily returns
returns = pd.read_csv('data/data_created/daily_returns.csv', index_col = 'Date', parse_dates = ['Date'])
print('The first 5 daily returns per company are\n', returns.head())
# %%
print(returns)
# %% Import companies list and create years list again
companies = pd.read_csv('data/data_created/companies_list.csv')['Company_Name'].tolist()

years = [] # To store the year columns
for year in range(2012, 2023):

    years.append(str(year)) 

print(years)

# %% Calculate Historical VaR and ES per company per year
# parameters
notional_principal = 10**9 # assume we hold 1 billion euros in each stock
confidence_level = 0.05 # since we want to calculate the 95% VaR and ES

losses = -1 * returns # calculate losses 

vars = pd.DataFrame(data = None, index = years[2:], columns = companies, dtype = float ) # to store VaR

es = pd.DataFrame(data = None, index = years[2:], columns = companies, dtype = float ) # to store ES measures

for i, year in enumerate(years[2:], start = 2):

    start_year = years[i-2]
    end_year = years[i]

    start_date = pd.Timestamp(f'{start_year}-10-02').date() # turn timestamp to date
    end_date = pd.Timestamp(f'{end_year}-09-29').date()

    window_losses = losses.loc[start_date: end_date]

    loss_quantiles = window_losses.quantile(1 - confidence_level, axis = 0)

    vars.loc[year] = loss_quantiles * notional_principal

    es_year = window_losses.apply(
        lambda x: x[x >= loss_quantiles[x.name]].mean() # look at column x(e.g AAPL), get VaR threshold, keep only rows that exceed VaR and calculate mean
    )

    es.loc[year] = es_year * notional_principal


# %% Value at Risk results

# Convert to *positive* losses in millions and round to 2 decimals
vars = (vars / 1e6).round(2)
print('The Value at Risk per company er year in millions is:\n', vars.head(10).to_string()) # in millions

vars.to_csv('data/data_created/value_at_risk.csv', index_label = 'Year') # save VaR results

cs_avg_var = vars.mean(axis=1)

plt.figure(figsize=(10, 5))
plt.plot(cs_avg_var)
plt.title("Cross-Sectional Average Value At Risk (VaR)")
plt.xlabel("Time")
plt.ylabel("Value At Risk (in millions of $)")
plt.grid(True)

plt.savefig("graphs/Cross-Sectional Average Value At Risk (VaR).png", dpi=300, bbox_inches="tight")
plt.close() 
# %% Expected Shortfall results

# Convert to *positive* losses in millions and round to 2 decimals
es = (es / 1e6).round(2)
print('The Expected Shortfall per company er year in millions is:\n', es.head(10).to_string()) # in millions

es.to_csv('data/data_created/expected_shortfall.csv', index_label = 'Year') # save ES results

cs_avg_es = es.mean(axis=1)

plt.figure(figsize=(10, 5))
plt.plot(cs_avg_es)
plt.title("Cross-Sectional Average Expected Shortfall (ES)")
plt.xlabel("Time")
plt.ylabel("Expected Shortfall (in millions of $)")
plt.grid(True)

plt.savefig("graphs/Cross-Sectional Average Expected Shortfall (ES).png", dpi=300, bbox_inches="tight")
plt.close() 
