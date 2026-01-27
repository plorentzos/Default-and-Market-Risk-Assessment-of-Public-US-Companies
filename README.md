# Default-and-Market-Risk-Assessment-of-Public-US-Companies

## Table of Contents
#### Project Overview
#### Data
#### Tools and Technologies
#### Analysis Workflow
#### Modeling Assumptions
#### Insights
#### How to Run


## Project Overview
In this project I use daily prices and financial statement data of 50 public U.S companies  to create measures in order to assess their exposure to default and market risk over a time horizon of  9 years.

The analysis includes data cleaning, exploratory data analysis and the creation, assessment and visualization of robust risk-related financial metrics. 

The analysis is performed in Python..  

## Data

There are 3 datasets used for the analysis:

* The first dataset includes the daily prices of the companies. 
* The second dataset includes annual financial statements variables and accounting ratios. 
* The third dataset includes yearly equity and debt values of companies.

The datasets include information about 50 public U.S companies, continuous members of the S&amp;P 500 Index, for the period spanning from 2012 to 2022.
The companies included represent the following sectors: Information Technology, Communication Services, Healthcare, Consumer Staples, Consumer Discretionary, Industrials, Energy and Utilities.
Including different sectors allows us to obtain a more diversified portfolio. Also, it opens the door for a sector analysis if deemed necessary.

Note that created datasets during the analysis can be found in data_created folder in the data folder.
Note that created graphs of the analysis can be found in the graphs folder.

## Tools and Technologies
* Python (Libraries: Pandas, NumPy, SciPy, Matplotlib)

## Analysis Workflow
* Run the .py files in this order: altman_z_score.py -> merton_dd.py -> var_and_es.py -> correlations_between_measures.py
* You can run the .py files in any order you want but this order is indicative of the analysis workflow.
* Each file contains each measure created and graphs produced. The correlations_between_measures.py contains the correlations claculation and visualization between the 3 risk measures.

## Modeling Assumptions
* Daily and yearly returns are being calculated using the standard industry formulas with continuous compounding.
* For Altman's Z Score refer to the non-manufacturer bankruptcy model on https://en.wikipedia.org/wiki/Altman_Z-score
* For Merton's Distance to Default refer to "Forecasting Default with Merton Distance to Default Model" (Bharath et. al 2008) , particularly section 2.3.
* Value At Risk and Expected Shortfall are calculated using the standard textbook formulas. In any case you can refer to Quantitative Risk Management book (McNeil et. al) chapter 2.3.

## Insights
* According to the cross-sectional  average Z-Score metric, our portfolio is considered to be in the 'safe zone' indicating a negligible risk of default. However, it seems that there is an downward trend over time, showing that these companies have gotten less financially "healthy" over time. Of course, as seen in the Z-score yearly table, some of the companies in our portfolio are considered to be in the 'distress zone' as they have Z-scores less than 1.10. For these companies, we can cross-check their risk of default using Merton's DD measure (or the naive default probabilities derived using it). If both measures indicate that the company is in the 'distress zone' we should consider excluding it from our portfolio of stocks if we are a risk-averse investor.
  
* According to the cross-sectional average Merton's naive Distance to Default (DD) measure, our portfolio of stocks seems to have higher default risk over time with the lowest point to be in 2020 due to the COVID-19 pandemic. Calculated naive DD probabilities are also useful to get a sense of the probability of default since Merton's naive DD is measured in standard deviations.

* Assume we hold 1 billion euros worth of each stock, i.e., we have invested a total of 50 billion euros in our portfolio of stocks. According to the cross-sectional average Value at Risk (VaR) and Expected Shortfall (ES), our portfolio seems to have increased market risk to extreme losses over time with a spike in 2022 due to the COVID-19 pandemic.
  
* Looking at the correlation between the created risk measures we can see that Altman's Z score and VaR have very weak correlation. This is expected as VaR relies only one daily stock prices whereas Altman's Z score relies on yearly fundamental company values.  We also see that during periods of distress (CoVid-19) correlations between Z score and VaR are virtually zero. DD and VaR are negatively correlated since a decreasing DD means the firm gets closer to default which signifies increased credit risk, which in turn leads to higher potential losses (VaR). We also see that during periods of distress(Covid-19) correlations between DD and VaR get less negative.Z score and DD have positive correlation as they are both default risk measures, but the level of correlation is weak since they are built using different variables and assumptions. 

## How to Run 

1. Clone the repository 
2. Install Python and required packages found in requirement.txt file. You can type pip install -r requirements.txt in your terminal to install the necessary versions of the libraries.
3. Do not forget to set your working directory, each file provides code that with minimal changes can get you there.







