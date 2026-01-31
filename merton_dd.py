# Import useful libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %% Directory setup
# Set relative path to the data file
base_dir = os.path.dirname(os.path.abspath(__file__))
prices_path = os.path.join(base_dir, "data", "prices.csv")
#%% Import prices dataset
prices = pd.read_csv(prices_path) # Import prices dataset
print('The first 5 daily prices for each company are\n', prices.head())
# %%
prices["Date"] = pd.to_datetime(prices["Date"], utc=True).dt.date # Convert Date
print(prices.head()) # Check the changes
# %%
prices = prices.set_index("Date") # Set Date as index
returns = np.log(prices / prices.shift(1))  # Log returns calculation
returns = returns[1:] # Remove NaN 1st row
print('The first 5 daily returns per company are\n', returns.head())
# Save the daily returns as a csv file
returns.to_csv("data/data_created/daily_returns.csv", index = True)
# %%
results = [] # To store the yearly returns per company
years = [] # To store the year columns
for year in range(2012, 2023):

    years.append(str(year)) 

print(years)
for i in range(1, len(years)): # Years list contains years from 2012 to 2022
     
    start_year = years[i-1]
    end_year = years[i]

    start_date = pd.Timestamp(f'{start_year}-10-02').date() # Turn timestamps to dates
    end_date = pd.Timestamp(f'{end_year}-09-29').date()

    yearly_window = returns.loc[start_date: end_date] # Get each yearly window to perform calculations on it
    
    yearly_return = yearly_window.sum() # A firm's yearly log return is the sum of its daily log returns

    yearly_return.name = f"{end_year}" # Label each row according to the corresponding year

    results.append(yearly_return) # Add the yearly_return to the initiated empty list

# Create a new df to store the results
yearly_returns = pd.DataFrame(results)
yearly_returns = yearly_returns[1:] # Remove 2013 so we have 2014-2022 period for comparability with the VaR measure we will create later
print("The yearly returns per company are\n", yearly_returns.head(11))
# %%
# Estimation of historical yearly equity volatility using daily log returns for each firm

results = [] # To store the yearly volatility per company

for i in range(1, len(years)): 
    start_year = years[i-1]
    end_year = years[i]

    start_date = pd.Timestamp(f'{start_year}-10-02').date() # Turn timestamps to dates
    end_date = pd.Timestamp(f'{end_year}-09-29').date()

    yearly_window = returns.loc[start_date: end_date] # Get each yearly window to perform calculations on it

    # Sample historical yearly volaitlity calculation for 252 trading days
    yearly_volatility = yearly_window.std(ddof=1) * np.sqrt(252) # Using 1 degree of freedom: Bessel's correction
    
    yearly_volatility.name = f"{end_year}" # Label each row according to the corresponding year

    results.append(yearly_volatility) # Add the yearly_volatility to the initiated empty list

# Create a new df to store the results
sigma_e = pd.DataFrame(results)
sigma_e = sigma_e[1:] # Remove 2013 so we have 2014-2022 period for comparability with the VaR measure created earlier in the analysis
print("The equity volatility per company are\n", sigma_e.head())
# %%
# Calculation of the yearly volatility of each firm's debt
sigma_d = 0.05 + 0.25 * sigma_e
print("The debt volatility per company are\n", sigma_d.head())
# %%
# Import data that contain the equity value and face value of debt for each firm
capital_path = os.path.join(base_dir, "data", "merton_data.csv")
capital = pd.read_csv(capital_path)
print(capital.head()) # Inspect the dataset

# Further checks
print('The number of missing values per year are:\n' ,capital.isna().sum()) # Check for NAs
print('There are: ', capital.duplicated().sum(), ' duplicates') # Check for duplicates
print('The shape of the dataset is: ' ,capital.shape) # Dimensions of the dataset
print('The dataset data types are:\n', capital.dtypes) # Columns data types
# %%
print("Column names:\n", capital.columns.tolist())
capital.columns = capital.columns.str.strip() # Remove whitespace

# Transform the data frame from wide format to long format
capital_long = capital.melt(
    id_vars = ['Company', 'Capital'],
    value_vars = years,
    value_name = 'Quantity',
    var_name = 'Year'
)

print(capital_long.head())

# Pivot the table created
capital_pivot = capital_long.pivot_table(
    values = 'Quantity',
    index = 'Year',
    columns = ['Company', 'Capital']
)

print(capital_pivot.head())

# %%
# Change multindex to single index
new_cols = [] # To store new column names

for company, capital in capital_pivot.columns:

    col_name = f"{company}_{capital}".replace(" ", "_")
    new_cols.append(col_name)

capital_pivot.columns = new_cols # Rename the cols
capital_pivot = capital_pivot[2:] # Remove 2012 and 2013 so that datasets align 

print(capital_pivot.head())
# %%
# Spit the df capital_pivot into 2 dfs (Equity and Debt) for easier coding of the model

# Face value of debt dataframe
cols_f = [col for col in capital_pivot.columns if col.endswith('_F') or col == 'Year']
debt =  capital_pivot[cols_f] 
debt.columns = [col.replace('_F', '') for col in debt.columns] # align col with other df col names so we can do calculations easily

print("The face value of debt of each company per year is:\n", debt.head())

# %%
# Equity dataframe
cols_e = [col for col in capital_pivot.columns if col.endswith('_E') or col == 'Year']
equity = capital_pivot[cols_e]
equity.columns = [col.replace('_E', '') for col in equity.columns]

print("The equity value of each company per year is:\n", equity.head())

# %%
# calculation of total volatility of each firm
sigma_v = (equity / (equity + debt)) * sigma_e + (debt / (equity + debt)) * sigma_d

print("The total volatility of each company per year is:\n", sigma_v.head())
# %%
# Calculation of the Distance to Default (DD) for each firm using the Naive DD formula

T = 1 # Assume 1 year forecasting horizon. For a weekly forecast, set T = 1/52.
naive_dd = (np.log((equity + debt) / debt) + (yearly_returns - 0.5 * sigma_v ** 2) * T) / (sigma_v * np.sqrt(T))
naive_dd = naive_dd.round(2)
print("The Distance to Default (DD) for each company per year is:\n", naive_dd.to_string())

# save the DD measure as a csv file
naive_dd.to_csv("data/data_created/distance_to_default.csv", index = True)
# %%
# Cross-sectional average over time of the Distance to Default
cs_avg_dd = naive_dd.mean(axis=1)

plt.figure(figsize=(10, 5))
plt.plot(cs_avg_dd)
plt.title("Cross-Sectional Average Distance to Default")
plt.xlabel("Time")
plt.ylabel("Distance to Default (in number of standard deviations)")
plt.grid(True)

plt.savefig("graphs/Cross-Sectional Average Distance to Default Across Time.png", dpi=300, bbox_inches="tight")
plt.close() 
# %% 
# Naive probability of default calculaton using Naive DD values

from scipy.stats import norm # Import standard normal CDF object

# Assumption: According to Merton model log asset returns follow a Gaussian Distribution. Hence, since we normalize when calculating DD we apply the standard normal CDF to derive the default probs.
pi_naive = pd.DataFrame(
    norm.cdf(-naive_dd.values),
    index=naive_dd.index,
    columns=naive_dd.columns
)

assert np.all((pi_naive >= 0) & (pi_naive <= 1)) # Sanity check
print("The naive default probabilities per year per company are\n", pi_naive.round(4).to_string())

# Save the probabilities of default as a csv file
pi_naive.to_csv("data/data_created/naive_default_probabilities.csv", index = True)
