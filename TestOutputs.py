import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

data = pd.read_csv('/Users/seggewa/Desktop/Inputfiles/combined_data.csv')

# Ensure the necessary columns are present
required_columns = {'Frame', 'Cluster', 'Tracks', 'Percentage of Tracks in Clusters', 'source_file'}
if not required_columns.issubset(data.columns):
    raise ValueError(f"Input CSV must contain the following columns: {required_columns}")

# Drop rows with NaN values in 'Percentage of Tracks in Clusters' and 'source_file'
data = data.dropna(subset=['Percentage of Tracks in Clusters', 'source_file'])

# Ensure 'source_file' is an integer type for correct grouping
data['source_file'] = data['source_file'].astype(int)

# Print unique values in 'source_file' for debugging
print("Unique values in 'source_file':", data['source_file'].unique())

# Group by 'source_file' and calculate the mean and standard error for 'Percentage of Tracks in Clusters'
grouped_data = data.groupby('source_file')['Percentage of Tracks in Clusters'].agg(['mean', 'sem']).reset_index()

# Print the grouped data for debugging
print("Grouped data:\n", grouped_data)

# Perform ANOVA to compare the means across the groups
anova_result = stats.f_oneway(*(data[data['source_file'] == group]['Percentage of Tracks in Clusters'].dropna() for group in grouped_data['source_file']))

# Determine significance level
def get_significance(p_value):
    if p_value < 0.001:
        return '***'
    elif p_value < 0.01:
        return '**'
    elif p_value < 0.05:
        return '*'
    else:
        return 'ns'  # Not significant

significance = get_significance(anova_result.pvalue)

# Print results
print("ANOVA test results:")
print(f"F-statistic: {anova_result.statistic}, P-value: {anova_result.pvalue}, Significance: {significance}")

# Plotting the averages with error bars
plt.figure(figsize=(10, 6))

# Explicit bar and error bar placement
positions = np.arange(len(grouped_data))
plt.bar(positions, grouped_data['mean'], yerr=grouped_data['sem'], align='center', alpha=0.7, capsize=10)

plt.xlabel('Source File')
plt.ylabel('Percentage of Tracks in Clusters')
plt.title('Comparison of Percentage of Tracks in Clusters Across Different Groups')
plt.xticks(positions, grouped_data['source_file'])

plt.show()
