import pandas as pd
df = pd.read_csv('/Users/seggewa/Desktop/2024-02-05_all-labels_tracks.v007.000_2023_11_13_white_ON_1800,1100_totalpixels-1980000_new.analysis.csv')
df = df.drop(['instance.score', 'head.x', 'head.y', 'head.score', 'mouthhooks.x', 'mouthhooks.y', 'mouthhooks.score', 'body.score', 'tail.x', 'tail.y', 'tail.score', 'spiracle.x', 'spiracle.y', 'spiracle.score'], axis=1)
print(df.head())
df.to_csv('/Users/seggewa/Desktop/DataAnalysis/RelevantColumns.csv', index=False)

