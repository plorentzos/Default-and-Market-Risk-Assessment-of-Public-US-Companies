# Default-and-Market-Risk-Assessment-of-Public-US-Companies

## Table of Contents
- [Project Overview](#project-overview)
- [Data](#data)
- [Tools and Technologies](#tools-and-technologies)
- [Project Workflow](#project-workflow)
- [Modeling Assumptions](#modeling-assumptions)
- [Insights](#insights)
- [How to Run](#how-to-run)



## Project Overview
In this project I use daily prices and financial statement data of 50 public U.S companies  to create measures in order to assess their exposure to default and market risk over a time horizon of  9 years.

The analysis includes data cleaning, exploratory data analysis and the creation, assessment and visualization of robust risk-related financial metrics. 

The analysis is performed in Python. 

## Data
There are 3 datasets used for the analysis:

* The first dataset includes the daily prices of the companies. 
* The second dataset includes annual financial statements variables and accounting ratios. 
* The third dataset includes yearly equity and debt values of companies.

The datasets include information about 50 public U.S companies, continuous members of the S&amp;P 500 Index, for the period spanning from 2012 to 2022.
The companies included represent the following sectors: Information Technology, Communication Services, Healthcare, Consumer Staples, Consumer Discretionary, Industrials, Energy and Utilities.
Including different sectors allows us to obtain a more diversified portfolio. Also, it opens the door for a sector analysis if deemed necessary.

Note that datasets that are generated during the analysis can be found in data_created folder in the data folder.
Note that graphs generated during the analysis can be found in the graphs folder.
Note that you can always delete the data_created and graphs folder. They will get generated again when you run the .py files.

## Tools and Technologies
* Python (Libraries: Pandas, NumPy, SciPy, Matplotlib)

## Project Workflow

### Risk Measures Creation

For each risk measure the following took place:

* Loaded the dataset and inspected it. Assessed the number of columns in the dataset and renamed any column names or row names if deemed necessary.
* Pivoted and formatted the dataset so it becomes easier to use for further analysis as well as improve readability.
* Checked for missing values and duplicates in the dataset.
* Created the risk measures based on theoretical background(See the Modeling-Assumptions section for further information).
* Plotted the cross-sectional average of the risk measure.
* Saved the risk measure in a .csv file in order to import it for correlation analysis.

### Correlations between Risk Measures
* Imported the created risk measures (Z-Score, Distance to Default, Value At Risk), which were saved as .csv files previously.
* Constructed the yearly correlations between the the three risk measures from 2014 to 2022.
* Plotted the yearly correlations of the 3 risk measures across time.

Note that additional comments regarding the code and the analysis can be found in the .py files.

## Modeling Assumptions
* Daily and yearly returns are being calculated using the standard finance textbook formulas with continuous compounding.
* For Altman's Z Score refer to the non-manufacturer bankruptcy model on https://en.wikipedia.org/wiki/Altman_Z-score
* For Merton's Distance to Default refer to "Forecasting Default with Merton Distance to Default Model" (Bharath et. al 2008) , particularly section 2.3.
* Value At Risk and Expected Shortfall are calculated using the standard textbook formulas. In any case, you can refer to Quantitative Risk Management book (McNeil et. al) chapter 2.3.

## Insights
* According to the cross-sectional average Z-Score metric, the portfolio is considered to be in the 'safe zone' indicating a negligible risk of default. However, the downward trend shows that these companies have gotten less financially "healthy" over time. As seen in the Z-score yearly table, some of the companies in the portfolio are considered to be in the 'distress zone' as they have Z-scores less than 1.10. For these companies, assessing their risk of default using Merton's DD measure would give a better idea. If both measures indicate that the company is in the 'distress zone' a risk averse investor would exclude them for their portfolio.
  
* According to the cross-sectional average Merton's naive Distance to Default (DD) measure, the portfolio seems to have higher default risk over time with the lowest point to be in 2020 due to the COVID-19 pandemic. Calculated naive DD probabilities are also useful to get a sense of the probability of default since Merton's naive DD is measured in standard deviations.

* Assume the owner of the portfolio holds 1 billion euros worth of each stock, i.e., they have invested a total of 50 billion euros in their portfolio of stocks. According to the cross-sectional average Value at Risk (VaR) and Expected Shortfall (ES), the portfolio seems to have increased market risk to extreme losses over time with a spike in 2022 due to the COVID-19 pandemic.
  
* Altman's Z score and VaR have very weak correlation. This is expected as VaR relies only one daily stock prices whereas Altman's Z score relies on yearly fundamental company values.  Additionally, during periods of distress (CoVid-19) correlations between Z score and VaR are virtually zero. DD and VaR are negatively correlated since a decreasing DD means the firm gets closer to default which signifies increased credit risk, which in turn leads to higher potential losses (VaR). Also, during periods of distress(Covid-19) correlations between DD and VaR get less negative. Z-score and DD have positive correlation as they are both default risk measures, but the level of correlation is weak since they are built using different information sources and assumptions. 

## How to Run 
1. Make sure you have Python 3.8+ installed in your personal computer. You can download it from: https://www.python.org/downloads/. Then make sure the minimum required version of Python is installed by typing in your terminal:
   ```bash
   python --version
2. Clone the repository
   ```bash
   git clone https://github.com/plorentzos/Default-and-Market-Risk-Assessment-of-Public-US-Companies.git
3. Navigate to the project directory
    ```bash
    cd Default-and-Market-Risk-Assessment-of-Public-US-Companies
4. Create a virtual environment. For more info visit: https://docs.python.org/3/library/venv.html
    ```bash
    python -m venv venv
5. Activate the virtual environment according to the operating system you use, e.g. for Windows I use:
    ```bash
    venv\Scripts\activate
6. Install the necessary libraries in the activated virtual environment
   ```bash
   python -m pip install -r requirements.txt
7. Run the Python scripts in the following order:
   ```bash
   python altman_z_score.py
   python merton_dd.py
   python var_and_es.py
   python correlations_between_risk_measures.py

   










