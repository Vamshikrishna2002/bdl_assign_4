import pandas as pd
import os
from sklearn.metrics import r2_score

import yaml
with open("params.yaml", 'r') as f:
    params = yaml.safe_load(f)
year=params['year']

df_ground=[]
ground_path=f'groundtruth/{year}'
for file_name in os.listdir(ground_path):
    df_ground.append(file_name)

df_predict=[]
predict_path=f'predicted/{year}'
for file_name in os.listdir(predict_path):
    df_predict.append(file_name)

ground = f'listfields/{year}' 
file_path = f'{ground}/fields.txt'

# Initialize an empty list to store the lines from the text file
monthly_fields = []

# Read the contents of the text file and add each line to the list
with open(file_path, 'r') as file:
    for line in file:
        monthly_fields.append(line.strip())  # Remove leading/trailing whitespace and add to the list

# Now monthly_list contains all the fields read from the text file

output_folder=f'r2score/{year}'
os.makedirs(output_folder, exist_ok=True)
res=[]
for i in range(len(df_ground)):
    
    temp1=os.path.join(ground_path,df_ground[i])
    temp2=os.path.join(predict_path,df_predict[i])
    temp_ground=pd.read_csv(temp1)
    temp_predict=pd.read_csv(temp2)
    temp_predict=temp_predict[:len(temp_ground)]

    temp_predict['MonthlyMaximumTemperature']=temp_predict['DailyMaximumDryBulbTemperature']
    temp_predict['MonthlyMinimumTemperature']=temp_predict['DailyMinimumDryBulbTemperature']
    temp_predict=temp_predict.drop(columns=monthly_fields)
    res.append({df_ground[i]:r2_score(temp_ground,temp_predict)})
    

file_path = os.path.join(output_folder, 'res.txt')

# Write the list to the file
with open(file_path, 'w') as f:
    for item in res:
        f.write("%s\n" % item)