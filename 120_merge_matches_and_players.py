import pandas as pd
import numpy as np

from utils import get_current_time

def merge_matches_and_players():
    filepath = 'data/merged_datasets/merged_fifa_and_fl_players.csv'
    merged_players = pd.read_csv(filepath)
    merged_players['update_as_of'] = pd.to_datetime(merged_players['update_as_of'],format='%Y-%m-%d')

    # mappings for fifa versions
    # we use this to map what version of fifa was out when a match was played
    # this is to prevent data leakage :)

    fifa_version_dict = merged_players.groupby('fifa_version')['update_as_of'].min().sort_values(ascending=False).to_dict()

    # TODO: Reminder, fifa 25 is not downloaded meaning fifa 24 ratings will be applied to 25 games,
    # possibly leading to worse results :( update to fifa 25! 

    matches_dataset = pd.read_csv('data/football_lineups/matches_dataset/matches_dataset.csv')
    matches_dataset['match_datetime']=pd.to_datetime(matches_dataset['match_datetime'])
    conditions = [matches_dataset['match_datetime'] >= x for x in fifa_version_dict.values()]
    choices = [x for x in fifa_version_dict.keys()]

    matches_dataset['fifa_version'] = np.select(conditions, choices,default=-1)

    # TODO: make this better

    starter_cols = [x for x in matches_dataset.filter(regex='starter_id').columns]
    for col in starter_cols:
        matches_dataset[f'{col}_fifa_version']=matches_dataset[col].astype(int).astype(str) + '_' + matches_dataset['fifa_version'].astype(int).astype(str)


    


    new_filepath = filepath.replace('merged_fifa_and_fl_players','merged_players_and_matches')
    matches_dataset.to_csv(new_filepath,index=False)
    print(f'{get_current_time()} Match and player attribute dataset written to {new_filepath}')



merge_matches_and_players()