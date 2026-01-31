# Import useful libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %% Directory setup
# Set relative path to the data file
base_dir = os.path.dirname(os.path.abspath(__file__))
fs_path = os.path.join(base_dir, "data", "financial_statements.csv")
# %%
# Import the financial statements data csv file as a pandas dataframe
fs = pd.read_csv(fs_path)
print(fs.head()) # Print the 5 first rows of the dataframe
# %%
# View the unique values of Account column
print("The Account column contains:\n", 
      fs["Account"].unique()
      ) 
# Improve column names readability
rename_accounts = {
    'CURRENT ASSETS': 'Current Assets',
    'TOTAL ASSETS': 'Total Assets',
    'Sales (Net)': 'Net Sales',
    'Retained Earnings (Net Other)': 'Retained Earnings',
    'PRETAX INCOME': 'EBIT',
    'TOTAL LIABILITIES': 'Total Liabilities',
    'TOTAL CURRENT LIABILITIES': 'Current Liabilities',
    'Mkt. Val. Equity / Book Val. Equity': 'MV Equity/BV Equity',
    "TOTAL SHAREHOLDERS' EQUITY": "Total Shareholders Equity"
}

fs["Account"] = fs["Account"].replace(rename_accounts)
# %%
print(fs.columns) # All cols are strings

years = [] # To store the year columns
for year in range(2012, 2023):

    years.append(str(year)) 

print(years)

# Transform the data from a wide format to a long format
fs_long = fs.melt(
    id_vars = ["Company", "Account"],
    value_vars = years,
    value_name = "Quantity",
    var_name = "Year"    
)

print(fs_long.head())
# %%
# Pivot the long df
fs_pivot = fs_long.pivot_table(
    values = "Quantity",
    index = "Year",
    columns = ["Company", "Account"]
)

print(fs_pivot.head()) # Now we have a multiindex
# %%
# Change the multiindex to a single index
new_cols = []

for company, account in fs_pivot.columns:

    col_name = f"{company}_{account}".replace(" ", "_")
    new_cols.append(col_name)

fs_pivot.columns = new_cols
print(fs_pivot.head())
# %%
# Inspecting the dataset
print('The number of missing values are:' ,fs_pivot.isna().sum().sum()) # Check for NAs
print('There are: ', fs_pivot.duplicated().sum(), ' duplicates') # Check for duplicates
print('The shape of the dataset is: ' ,fs_pivot.shape) # Dimensions of the dataset
print('The dataset data types are:\n', fs_pivot.dtypes) # Columns data types
# %%
# Calculation of Altman's Z-score for each company per year

years = fs_pivot.index # Take the years out of the main dataframe

# Use set since we need uniqueness (drops duplicates) and less computationally intensive
companies_set = set()  

for col in fs_pivot.columns:

    company = col.split('_')[0]
    companies_set.add(company)

companies = sorted(companies_set) # Sort the set in alphabetical order

companies_df = pd.DataFrame(companies, columns=['Company_Name'])
companies_df.to_csv("data/data_created/companies_list.csv", index = False) # Save the companies list for future use
# Create a dataframe to store Z-scores
Z_scores = pd.DataFrame(index = years, columns = companies, dtype = float)

for comp in companies:

 X_1 = (fs_pivot[f'{comp}_Current_Assets'] -  fs_pivot[f'{comp}_Current_Liabilities']) / fs_pivot[f'{comp}_Total_Assets']
 X_2 = fs_pivot[f'{comp}_Retained_Earnings'] / fs_pivot[f'{comp}_Total_Assets']
 X_3 = fs_pivot[f'{comp}_EBIT'] / fs_pivot[f'{comp}_Total_Assets']
 X_4 = fs_pivot[f'{comp}_Total_Shareholders_Equity'] / fs_pivot[f'{comp}_Total_Liabilities']

 Z_scores[comp] = 6.56 * X_1 + 3.26 * X_2 + 6.72 * X_3 + 1.05 * X_4

Z_scores = Z_scores.iloc[2:] # Remove 2012 and 2013 for comparability with other measures we will create later on
Z_scores = Z_scores.round(2) 

print("Altman's Z Scores per company per year are:\n",   Z_scores.head(11))
# %%
# Make folder to save created data
os.makedirs('data/data_created', exist_ok=True)
# save the Z-scores dataframe as a csv file
Z_scores.to_csv("data/data_created/altman_z_scores.csv", index = True)
# %%
 # Calculate the cross-sectional average to assess the overall Z-score of the firms we picked
Z_score_avg_per_year = Z_scores.mean(axis = 1)
Z_score_avg_per_year.index = Z_score_avg_per_year.index.astype(int) # Store index labels as integers to plot

# Make folder to save graphs
os.makedirs("graphs", exist_ok=True) # Make folder to save graphs

plt.figure()
plt.plot(Z_score_avg_per_year.index, Z_score_avg_per_year.values, marker='o')
plt.xlabel('Year')
plt.ylabel('Z-Score')
plt.title('Cross-Sectional Average Z-Score Across Time')
plt.grid(True)
plt.ylim(3, 5)

# Save the figure to graphs folder
plt.savefig("graphs/Cross-Sectional Average Z-Score Across Time.png", dpi=300, bbox_inches="tight")
plt.close() 
