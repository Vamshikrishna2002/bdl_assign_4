import pandas as pd
import os
import yaml
with open("params.yaml", 'r') as f:
    params = yaml.safe_load(f)
year=params['year']
# Directory containing the downloaded CSV files
data_folder = f"download_files/{year}"
output_folder=f'groundtruth/{year}'
os.makedirs(output_folder, exist_ok=True)
# List to store non-NA values of monthly average wet bulb temperature
df_list = []
monthly_fields=['MonthlyMaximumTemperature','MonthlyMinimumTemperature']
Daily_fields=['DailyMaximumDryBulbTemperature','DailyMinimumDryBulbTemperature']
list_of_fields=f'listfields/{year}'
os.makedirs(list_of_fields, exist_ok=True)
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
        # Select columns of interest
        df_filtered = df_filtered[['MONTH', 'MonthlyMaximumTemperature','MonthlyMinimumTemperature']]
        # Append filtered DataFrame to list
        output_file_path = os.path.join(output_folder, f'{os.path.splitext(file_name)[0]}_filtered.csv')
        df_filtered.to_csv(output_file_path, index=False)

file_pa = os.path.join(list_of_fields, 'fields.txt')

# Write the list to the file
with open(file_pa, 'w') as f:
    for item in Daily_fields:
        f.write("%s\n" % item)

