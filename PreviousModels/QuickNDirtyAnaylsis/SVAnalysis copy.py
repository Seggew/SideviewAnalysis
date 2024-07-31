import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Load data from CSV
data = pd.read_csv('/Users/seggewa/Desktop/SVData - Quantify.csv')

# Columns to process
percent_columns = ['1.30%', '2.30%', '3.30%']

# Calculate the mean of percentage columns grouped by the 'condition' column
means = data.groupby('condition')[percent_columns].mean()

# Standardize the mean values
standardized_means = (means - means.mean()) / means.std()

# Statistical comparison using ANOVA (if more than two groups) or t-test (if two groups)
if len(means) > 2:
    F, p = stats.f_oneway(*(data[data['condition'] == cond][percent_columns].values.ravel() for cond in data['condition'].unique()))
    print("ANOVA test results: F =", F, "p =", p)
else:
    t, p = stats.ttest_ind(data[data['condition'] == data['condition'].unique()[0]][percent_columns].values.ravel(),
                           data[data['condition'] == data['condition'].unique()[1]][percent_columns].values.ravel())
    print("T-test results: t =", t, "p =", p)

# Function to plot bar charts for the averages of two conditions with error bars
def plot_comparison(cond1, cond2):
    conds = [cond1, cond2]
    means_subset = means.loc[conds]
    errors = data.groupby('condition')[percent_columns].sem().loc[conds]

    fig, ax = plt.subplots()
    means_subset.T.plot(kind='bar', yerr=errors.T, ax=ax, capsize=4)
    ax.set_title('Comparison of Conditions: {} vs {}'.format(cond1, cond2))
    ax.set_ylabel('Average %')
    ax.set_xlabel('Percentage Metrics')
    plt.xticks(rotation=0)
    plt.legend(title='Condition')
    plt.show()

# Example usage of the plotting function
plot_comparison('Condition1', 'Condition2')  # Replace 'Condition1' and 'Condition2' with actual condition names from your data

