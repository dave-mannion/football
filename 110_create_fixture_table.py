import pandas as pd
import numpy as np

from utils import load_json, get_current_time, write_list_to_text_file
import os
import glob
import pandas as pd
import copy

def extract_starter_ids(lineups):
    temp_team_ids = {}
    for team,lineup in lineups.items():
        temp_team_ids[team]=[x['id'] for x in lineup['starters']]
        
    return temp_team_ids

def format_match_lineup_json(match_lineup_json):
    match_lineup_json_copy = copy.deepcopy(match_lineup_json)

    home_team = match_lineup_json['home_team']
    away_team = match_lineup_json['away_team']

    lineups = match_lineup_json_copy.pop('lineups')

    starter_ids = extract_starter_ids(lineups)
    home_starters = {f'home_starter_{i+1}':x for i,x in enumerate(starter_ids[home_team])}
    away_starters = {f'away_starter_{i+1}':x for i,x in enumerate(starter_ids[away_team])}

    match_lineup_json_copy = match_lineup_json_copy | home_starters
    match_lineup_json_copy = match_lineup_json_copy | away_starters

    return match_lineup_json_copy

def extract_match_info_from_json():

    print(f"{get_current_time()} Starting data extraction from JSON files...")
    path = "data/football_lineups/extracted_match_json_files/"
    all_match_info = []

    for filename in glob.glob(os.path.join(path, '*.json')): #only process .JSON files in folder. 
        try:
            match_lineup = load_json(filename)
            all_match_info.append(format_match_lineup_json(match_lineup))
        except FileNotFoundError:
            print(f"Error: '{filename}' not found. Please ensure the file exists in the same directory.")
            exit()

    match_info_df = pd.DataFrame.from_dict(all_match_info)

    match_info_df['home_win']=np.where(match_info_df['home_score']>match_info_df['away_score'],1,0)
    match_info_df['draw']=np.where(match_info_df['home_score']==match_info_df['away_score'],1,0)
    match_info_df['away_win']=np.where(match_info_df['home_score']<match_info_df['away_score'],1,0)

    filepath = 'data/football_lineups/matches_dataset/matches_dataset.csv'
    match_info_df.to_csv(filepath,index=False)
    print(f'{get_current_time()} Match Dataset written to {filepath}')


extract_match_info_from_json()
