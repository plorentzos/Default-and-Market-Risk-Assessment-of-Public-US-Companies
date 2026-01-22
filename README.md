# Default-and-Market-Risk-Assessment-of-Public-US-Companies

# Project Overview
In this project I use daily prices and financial statement data of 50 public U.S companies  to create measures in order to assess their exposure to default and market risk over a time horizon of  9 years.

The analysis includes data cleaning, exploratory data analysis and the creation, assessment and visualization of robust risk-related financial metrics. 

The analysis is performed in Python using a Jupyter Notebook.  

Assumptions and theoretical background of the analysis are included in the Jupyter Notebook.

# Datasets

There are 3 datasets used for the analysis:

* The first dataset includes the daily prices of the companies. 
* The second dataset includes annual financial statements variables and accounting ratios. 
* The third dataset includes yearly equity and debt values of companies.

The datasets include information about 50 public U.S companies, continuous members of the S&amp;P 500 Index, for the period spanning from 2012 to 2022.
The companies included represent the following sectors: Information Technology, Communication Services, Healthcare, Consumer Staples, Consumer Discretionary, Industrials, Energy and Utilities.
Including different sectors allows us to obtain a more diversified portfolio. Also, it opens the door for a sector analysis if deemed necessary.


# Tools and Technologies
* Python (Libraries: Pandas, NumPy, SciPy, Matplotlib)
* Jupyter Notebook (LaTeX is used to present the mathematical equations)

# Analysis Workflow
* Import libraries and set directory.
* Create each measure sequentially starting from default risk measures.
* For each measure load the related dataset, inspect and clean it, create the measure, visualize and interpret the created measure.
* Assess the relationship between measures over time using yearly correlation matrices.

# Insights
* According to the cross-sectional  average Z-Score metric, our portfolio is considered to be in the 'safe zone' indicating a negligible risk of default. Of course, as seen in the Z-score yearly table, some of the companies in our portfolio are considered to be in the 'distress zone' as they have Z-scores less than 1.81. For these companies, we can cross-check their risk of default using Merton's DD measure (or the naive default probabilities derived using it). If both measures indicate that the company is in the 'distress zone' we should consider excluding it from our portfolio of stocks if we are a risk-averse investor.
* According to the cross-sectional average Merton's naive Distance to Default (DD) measure, our portfolio of stocks seems to have higher default risk over time with the lowest point to be in 2020 due to the COVID-19 pandemic. Calculated naive DD probabilities are also useful to get a sense of the probability of default since Merton's naive DD is measured in standard deviations.
* According to the cross-sectional average Value at Risk (VaR) and Expected Shortfall (ES), our portfolio seems to have increased market risk to extreme losses over time with a spike in 2022 due to the COVID-19 pandemic. 
* Looking at the correlation between the created risk measures we can see that Altman's Z score and VaR have very weak correlation. This is expected as VaR relies only one daily stock prices whereas Altman's Z score relies on yearly fundamental company values. DD and VaR are negatively correlated since a decreasing DD means the firm gets closer to default which signifies increased credit risk, which in turn leads to higher potential losses (VaR). Z score and DD have positive correlation as both are default risk measures.

# How to Run 

1. Clone the repository (make sure the coding file and the datasets are in the same folder!)
2. Install Python and required packages
3. Open the Jupyter Notebook
4. Run Cells sequentially (don not forget to set the path to your folder in the working directory!)







