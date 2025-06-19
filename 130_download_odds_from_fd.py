import pandas as pd

league_codes = {
    'FA-Premier-League':'E0',
    'La-Liga':'SP1',
    'Bundesliga':'D1',
    'Serie-A':'I1',
    'Ligue-1':'F1',
    'Eredivisie':'N1',
    'Portuguese-Liga':'P1',
    'Scottish-Premiership':'SC0',
    'The-Championship':'E1'
}

years = [
    '1516',
    '1617',
    '1718',
    '1819',
    '1920',
    '2021',
    '2122',
    '2223',
    '2324',
    '2425'
]

download = False
if download:
    print('downloading historical odds')
    for league,league_code in league_codes.items():
        for year in years:
            url = f'https://www.football-data.co.uk/mmz4281/{year}/{league_code}'
            try:
                temp_df = pd.read_csv(url)
                temp_df.to_csv(f'data/football_data/{league}_{year}_historical_odds.csv',index=False)
            except:
                print(f'Failed: {url}')
                continue

    print('Done Downloading')

dfs = []
for league,league_code in league_codes.items():
    for year in years:
        try:
            temp_df=pd.read_csv(f'data/football_data/{league}_{year}_historical_odds.csv')
        except:
            temp_df=pd.read_csv(f'data/football_data/{league}_{year}_historical_odds.csv',encoding='windows-1254')

        dfs.append(temp_df)

filepath = 'data/football_data/historical_odds.csv'
all_dfs = pd.concat(dfs)
all_dfs.to_csv(filepath,index=False)
print(f'Historical Odds dataset of shape {all_dfs.shape} written to {filepath}')

