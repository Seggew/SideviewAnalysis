import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Assuming data loading and initial processing are done correctly
data = pd.read_csv('/Users/seggewa/Desktop/DataAnalysis/SVData-Quantify.csv')

# Calculate the average of the percentage columns for each condition
data['AvgPercentage'] = data[['1.3', '2.3', '3.3']].mean(axis=1)

# Columns to process for statistical analysis
percent_columns = ['1.3', '2.3', '3.3']

# Calculate the mean and standard error of the average percentage column grouped by the 'condition' column
means = data.groupby('condition')['AvgPercentage'].mean()
errors = data.groupby('condition')['AvgPercentage'].sem()

# Function to plot bar charts for the averages of four conditions with error bars
def plot_comparison():
    # Define labels for the conditions
    condition_mapping = {1: '0.8mm', 2: '0.5mm', 3: '0.8mm/f+', 4: '0.5mm/f+'}

    # Select the data for 'AvgPercentage'
    groups_data = means.loc[[1, 2, 3, 4]]
    group_errors = errors.loc[[1, 2, 3, 4]]

    # Perform a t-test between each pair of groups
    group1 = data[data['condition'] == 1]['AvgPercentage']
    group2 = data[data['condition'] == 2]['AvgPercentage']
    group3 = data[data['condition'] == 3]['AvgPercentage']
    group4 = data[data['condition'] == 4]['AvgPercentage']
    
    t_stat_12, p_value_12 = stats.ttest_ind(group1, group2)
    t_stat_13, p_value_13 = stats.ttest_ind(group1, group3)
    t_stat_14, p_value_14 = stats.ttest_ind(group1, group4)
    t_stat_23, p_value_23 = stats.ttest_ind(group2, group3)
    t_stat_24, p_value_24 = stats.ttest_ind(group2, group4)
    t_stat_34, p_value_34 = stats.ttest_ind(group3, group4)

    # Determine significance levels
    def get_significance(p_value):
        if p_value < 0.001:
            return '***'
        elif p_value < 0.01:
            return '**'
        elif p_value < 0.05:
            return '*'
        else:
            return 'ns'  # Not significant

    significance_12 = get_significance(p_value_12)
    significance_13 = get_significance(p_value_13)
    significance_14 = get_significance(p_value_14)
    significance_23 = get_significance(p_value_23)
    significance_24 = get_significance(p_value_24)
    significance_34 = get_significance(p_value_34)

    # Define figure size
    fig, ax = plt.subplots(figsize=(4, 4))  # Adjusted width for four bars

    # Define absolute bar positions and width
    positions = [0.2, 0.5, 0.8, 1.1]  # Absolute positions for each bar on the x-axis
    bar_width = 0.2  # Absolute bar width

    # Colors for each group
    colors = ['#30694F', '#B8CCC3', '#56917B', '#3A7871']  # Specific colors for each condition

    # Plot bars at specified positions
    max_height = 0
    for pos, cond, color in zip(positions, sorted(condition_mapping.keys()), colors):
        bar = ax.bar(pos, groups_data.loc[cond], bar_width, color=color, yerr=group_errors.loc[cond], capsize=4)
        max_height = max(max_height, bar[0].get_height() + group_errors.loc[cond])

    # Set axis labels and title
    ax.set_xlabel('Conditions')
    ax.set_ylabel('Fraction of clustering larvae')
 
    ax.set_xticks(positions)
    ax.set_xticklabels([condition_mapping[cond] for cond in sorted(condition_mapping.keys())])

    # Add significance lines and annotations if there is significance
    y_max = max_height + 0.1  # Adjust height for the line

    if significance_12 != 'ns':
        ax.plot([positions[0], positions[1]], [y_max, y_max], color='black')
        ax.text((positions[0] + positions[1]) / 2, y_max + 0.02, significance_12, ha='center')

    if significance_13 != 'ns':
        y_max_13 = y_max + 0.5
        ax.plot([positions[0], positions[2]], [y_max_13, y_max_13], color='black')
        ax.text((positions[0] + positions[2]) / 2, y_max_13 + 0.02, significance_13, ha='center')

    if significance_14 != 'ns':
        y_max_14 = y_max + 1.1
        ax.plot([positions[0], positions[3]], [y_max_14, y_max_14], color='black')
        ax.text((positions[0] + positions[3]) / 2, y_max_14 + 0.02, significance_14, ha='center')

    if significance_23 != 'ns':
        y_max_23 = y_max + 2.5
        ax.plot([positions[1], positions[2]], [y_max_23, y_max_23], color='black')
        ax.text((positions[1] + positions[2]) / 2, y_max_23 + 0.02, significance_23, ha='center')

    if significance_24 != 'ns':
        y_max_24 = y_max + 1.7
        ax.plot([positions[1], positions[3]], [y_max_24, y_max_24], color='black')
        ax.text((positions[1] + positions[3]) / 2, y_max_24 + 0.02, significance_24, ha='center')

    if significance_34 != 'ns':
        y_max_34 = y_max + 1.7
        ax.plot([positions[2], positions[3]], [y_max_34, y_max_34], color='black')
        ax.text((positions[2] + positions[3]) / 2, y_max_34 + 0.02, significance_34, ha='center')

    # Remove the top and right spines (outer frame) while keeping the x and y axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.show()

# Call the function to plot
plot_comparison()
