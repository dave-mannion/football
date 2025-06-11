from utils import load_json, get_current_time
import glob
import os
import pandas as pd

def load_player_json():

    print(f"{get_current_time()} Starting data extraction from JSON files...")
    path = "data/football_lineups/extracted_player_json_files/"
    
    all_match_player_info = []
    for filename in glob.glob(os.path.join(path, '*.json')): #only process .JSON files in folder. 
        try:
            match_lineup = load_json(filename)
            all_match_player_info.append(match_lineup)
        except FileNotFoundError:
            print(f"Error: '{filename}' not found. Please ensure the file exists in the same directory.")
            exit()

    return pd.DataFrame(all_match_player_info)

load_player_json_df = load_player_json()
load_player_json_df.to_csv("data/football_lineups/player_dataset/players_dataset.csv", index=False)