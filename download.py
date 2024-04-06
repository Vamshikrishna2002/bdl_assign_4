import requests
import os
import zipfile
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import yaml

with open("params.yaml", 'r') as f:
    params = yaml.safe_load(f)
    print(params) 

def download_csv_files(year, n_locs):
    base_url = f'https://www.ncei.noaa.gov/data/local-climatological-data/access/{year}'
    output_folder = f"download_files/{year}"
    
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    res = requests.get(base_url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find('table')
        if table:
            anchors = table.find_all('a')
            anchors.reverse()  # Reverse the order of the anchors list
            files_downloaded = 0
            
            for anchor in anchors:
                if files_downloaded >= n_locs:
                    break
                
                file_name = anchor.text
                if file_name.endswith('.csv'):
                    file_url = f'{base_url}/{file_name}'
                    try:
                        # Download CSV file and save it to the specified directory
                        res_file = requests.get(file_url)
                        if res_file.status_code == 200:
                            with open(os.path.join(output_folder, file_name), 'wb') as f:
                                f.write(res_file.content)
                            files_downloaded += 1
                            print(f"Downloaded: {file_name}")
                        else:
                            print(f"Failed to download: {file_url}")
                    except Exception as e:
                        print(f"An error occurred while downloading: {file_url}. Error: {e}")
        else:
            print("No table found in the page.")
    else:
        print(f"Failed to retrieve data for year {year}")

download_csv_files(params['year'],params['n_locs'])




































