import numpy as np
import pandas as pd
import os 
import yaml
import re

with open("params.yaml", 'r') as f:
    params = yaml.safe_load(f)
    
year=params['year']
data_folder = f"download_files/{year}"
output_folder=f'predicted/{year}'
os.makedirs(output_folder, exist_ok=True)
# List to store non-NA values of monthly average wet bulb temperature
df_list = []


ground_path = f'listfields/{year}' 
file_path = f'{ground_path}/fields.txt'

# Initialize an empty list to store the lines from the text file
monthly_fields = []

# Read the contents of the text file and add each line to the list
with open(file_path, 'r') as file:
    for line in file:
        monthly_fields.append(line.strip())  # Remove leading/trailing whitespace and add to the list

# Now monthly_list contains all the fields read from the text file


# Iterate over CSV files in the data folder
for file_name in os.listdir(data_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(data_folder, file_name)
        # Read CSV file into DataFrame
        df = pd.read_csv(file_path)
        # Filter rows where MonthlyDepartureFromNormalAverageTemperature is not NA
        df_filtered = df.dropna(subset=monthly_fields, axis=0)
         # Convert 'DATE' column to datetime and extract month
        df_filtered['MONTH'] = pd.to_datetime(df_filtered['DATE']).dt.month
        for i in monthly_fields:
            df_filtered[i] = df_filtered[i].astype(str).str.replace('[a-zA-Z]','',regex=True)
        df_filtered.replace({'':np.nan},inplace=True)
        df_filtered = df_filtered.dropna(subset=monthly_fields, axis=0)
        for i in monthly_fields:
            df_filtered[i]=df_filtered[i].astype(float)

        # Select columns of interest
        monthly_aggregrate = df_filtered.groupby('MONTH',as_index=False)[monthly_fields[0]].mean()
        for i in range(1,len(monthly_fields)):
            temp = df_filtered.groupby('MONTH',as_index=False)[monthly_fields[i]].mean()
            monthly_aggregrate=pd.concat([temp.set_index('MONTH'),monthly_aggregrate.set_index('MONTH')],axis=1)
        output_file_path = os.path.join(output_folder, f'{os.path.splitext(file_name)[0]}_filtered.csv')
        
        monthly_aggregrate.to_csv(output_file_path, index=True)
        
        

