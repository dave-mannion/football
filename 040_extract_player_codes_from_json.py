from utils import load_json, get_current_time, write_list_to_text_file
import os
import glob
import pandas as pd

def parse_lineups(match_json):
    """
    Parse the lineups from a match JSON object.
    
    Args:
        match_json (dict): The JSON object containing match data.
        
    Returns:
        pd.DataFrame: A DataFrame containing the parsed lineups.
    """
    lineups_list = []
    
    for team in match_json['lineups'].keys():
        starters = match_json['lineups'][team]['starters']
        substitutes = match_json['lineups'][team]['substitutes_played']

        lineups_list += starters
        lineups_list += substitutes
    
    return lineups_list

def extract_player_info_from_json():

    print(f"{get_current_time()} Starting data extraction from HTML files...")
    path = "data/football_lineups/extracted_match_json_files/"
    
    all_match_player_info = []
    for filename in glob.glob(os.path.join(path, '*.json')): #only process .JSON files in folder. 
        try:
            match_lineup = load_json(filename)
            all_match_player_info += parse_lineups(match_lineup)
        except FileNotFoundError:
            print(f"Error: '{filename}' not found. Please ensure the file exists in the same directory.")
            exit()

    return pd.DataFrame(all_match_player_info)

if __name__ == "__main__":
    player_info_df = extract_player_info_from_json()
    player_id_list = player_info_df['id'].drop_duplicates().sort_values().tolist()

    write_list_to_text_file(list=player_id_list,
                            filepath="data/football_lineups/extracted_player_codes/player_codes.txt")
    
    print(f"{get_current_time()} Player information extracted and saved to player_codes.txt'.")
