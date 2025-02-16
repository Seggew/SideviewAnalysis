import pandas as pd
import os 
import pyarrow.feather


def combine_feather_files(input_directory, output_file):
    all_files = [os.path.join(input_directory, f) for f in os.listdir(input_directory) if f.endswith('.csv')]
    
    combined_df = pd.DataFrame()
    
    for idx, file in enumerate(all_files, start=1):
        temp_df = pd.read_csv(file)
        temp_df['source_file'] = idx  # Add a column to indicate the source file
        combined_df = pd.concat([combined_df, temp_df], ignore_index=True)
    
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV saved to {output_file}")

input_directory = '/Users/seggewa/Desktop/Inputfiles0.7mm'

output_file = '/Users/seggewa/Desktop/Output/combined_data.csv'

combine_csv_files(input_directory, output_file)
