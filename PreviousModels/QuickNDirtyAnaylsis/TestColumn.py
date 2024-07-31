import pandas as pd

# Adjust the path to your CSV file
data = pd.read_csv('/Users/seggewa/Desktop/DataAnalysis/SVData-Quantify.csv')  
print(data.columns)  # Print all column names to verify
print(data.dtypes)