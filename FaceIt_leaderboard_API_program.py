#By Nicholas Odeh 

#needed imports
import json
import requests
import colorama
import time
import sqlite3
import re

#used for troubleshoot input
yes = [ 'Yes','Y','yes','y']
no = [ 'No','N','no','n']


# things to change for api 
api_key = "YOUR KEY HERE"
game_id = "csgo"
region = "SA"
off_set_limit = '0'
position_request_limit = 100



# URL for the Faceit Data API endpoint
url = f'https://open.faceit.com/data/v4/rankings/games/{game_id}/regions/{region}?offset={off_set_limit}&limit={position_request_limit}'

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_key}"
}

response = requests.get(url, headers=headers)
general_call_response = response.raise_for_status


#asks if you need a troubleshooting response code, will give response code regardless of what it is
ask_if_want_gen_response = input (f'Do you need the troubleshooting response code? \n \n Y/N: ')
if ask_if_want_gen_response in yes:
  print (f'{colorama.Fore.YELLOW}{general_call_response}{colorama.Style.RESET_ALL} for the FACEIT API call: {colorama.Fore.YELLOW}{url}{colorama.Style.RESET_ALL}')
  time.sleep(1)
else:
  print(" ")
  print("Troubleshooting  not requested")
  print(" ")
  print(" ")
  print(" ")
  print(" ")

#if status code is good, code will contiune and get json data from faceit api
if response.status_code == 200:
    callback_code = "Response: 200"
    data = response.json()
    move_forward = input(f'\n{colorama.Fore.RED} Call request successful ({colorama.Fore.GREEN}{callback_code}{colorama.Style.RESET_ALL}{colorama.Fore.RED}), press any button to start displaying the api data:{colorama.Style.RESET_ALL} ')
    print(f'\n{colorama.Fore.YELLOW}Fetched Data:{colorama.Style.RESET_ALL}\n \n {data}')

else:
    print("Error:", response.status_code)


#creates a json file to write FACEIT API response
rank_values = 'stored_rank_values.json'
with open(rank_values, 'a') as file_object:
  #puts api json data into stored_rank_values.json
  json.dump(data, file_object, indent=2)
  
  
#####################      PART TWO OF CODE  |  JSON TO EXCEL CONVERTER #####################


# Read JSON data from file
with open('stored_rank_values.json', 'r') as json_file:
    data = json_file.read()

# Convert JSON data to dictionary
data_dict = json.loads(data)

# Convert JSON data to DataFrame
df = pd.DataFrame(data_dict["items"])

# Write DataFrame to Excel file
excel_file_path = "player_data.xlsx"
df.to_excel(excel_file_path, index=False)

print("Excel file created:", excel_file_path)
