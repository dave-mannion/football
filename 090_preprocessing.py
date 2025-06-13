import pandas as pd
import numpy as np
from utils import get_current_time
from thefuzz import fuzz

def rtf_file_to_csv(file_path,nlines=None):

    """
    Convert an RTF file to a CSV file by extracting lines of text.
    Parameters:
    file_path (str): The path to the RTF file.
    nlines (int): The number of lines to extract from the RTF file.
    """

    print(f"{get_current_time()} Converting RTF file to CSV: {file_path}")

    counter = 0
    lines_list = []
    with open(file_path, encoding='utf-8', errors='ignore') as file:
        # Read all the RTF file's content

        text = file.read()
        for l in text.splitlines():
            split= l.split(' | ')
            split = [x.replace('|','').strip() for x in split]  # Remove empty strings

            # Skip every second line as it is part of the formatting of the RTF file and doesn't contain useful data
            if counter %2 == 0:
                lines_list.append(split)

            counter +=1
            if nlines:
                if counter > nlines:
                    break
    file.close()

    df = pd.DataFrame(lines_list)
    df.rename(columns = df.iloc[0], inplace=True)
    df = df[1:]  # Remove the first row which is now the header
    df.reset_index(drop=True, inplace=True)

    df.to_csv(file_path.replace('rtf','csv'), index=False)

    print(f"{get_current_time()} RTF file converted to CSV successfully: {file_path.replace('rtf','csv')}")



country_names = {
    'ARG': 'Argentina',
    'BRA': 'Brazil',
    'ITA': 'Italy',
    'ESP': 'Spain',
    'ENG': 'England',
    'FRA': 'France',
    'GER': 'Germany',
    'BEL': 'Belgium',
    'ROU': 'Romania',
    'POR': 'Portugal',
    'USA': 'United States',
    'SWE': 'Sweden',
    'NOR': 'Norway',
    'HUN': 'Hungary',
    'GRE': 'Greece',
    'SUI': 'Switzerland',
    'COL': 'Colombia',
    'TUR': 'Turkey',
    'URU': 'Uruguay',
    'AUT': 'Austria',
    'MEX': 'Mexico',
    'SCO': 'Scotland',
    'CHI': 'Chile',
    'DEN': 'Denmark',
    'POL': 'Poland',
    'CHN': 'China',
    'RSA': 'South Africa',
    'CZE': 'Czech Republic',
    'NED': 'Netherlands',
    'PER': 'Peru',
    'ISR': 'Israel',
    'SRB': 'Serbia',
    'RUS': 'Russia',
    'BLR': 'Belarus',
    'MAS': 'Malaysia',
    'BUL': 'Bulgaria',
    'NIR': 'Northern Ireland',
    'UKR': 'Ukraine',
    'ISL': 'Iceland',
    'CRO': 'Croatia',
    'IRL': 'Republic of Ireland',
    'WAL': 'Wales',
    'SVN': 'Slovenia',
    'CAN': 'Canada',
    'IDN': 'Indonesia',
    'KOR': 'South Korea',
    'SVK': 'Slovakia',
    'NZL': 'New Zealand',
    'FIN': 'Finland',
    'AUS': 'Australia',
    'NGA': 'Nigeria',
    'GHA': 'Ghana',
    'LVA': 'Latvia',
    'BRU': 'Brunei',
    'IND': 'India',
    'CIV': "Ivory Coast (Côte d'Ivoire)",
    'SEN': 'Senegal',
    'BIH': 'Bosnia and Herzegovina',
    'MAR': 'Morocco',
    'ALB': 'Albania',
    'CMR': 'Cameroon',
    'SIN': 'Singapore',
    'VEN': 'Venezuela',
    'FIJ': 'Fiji',
    'KOS': 'Kosovo',
    'SOL': 'Solomon Islands',
    'HKG': 'Hong Kong',
    'VAN': 'Vanuatu',
    'NCL': 'New Caledonia',
    'COD': 'DR Congo',
    'PAR': 'Paraguay',
    'GNB': 'Guinea-Bissau',
    'MLI': 'Mali',
    'ALG': 'Algeria',
    'IRN': 'Iran',
    'SAM': 'Samoa',
    'GUI': 'Guinea',
    'JPN': 'Japan',
    'ECU': 'Ecuador',
    'TUN': 'Tunisia',
    'MKD': 'North Macedonia',
    'PNG': 'Papua New Guinea',
    'CPV': 'Cape Verde',
    'UZB': 'Uzbekistan',
    'SYR': 'Syria',
    'EGY': 'Egypt',
    'MNE': 'Montenegro',
    'KSA': 'Saudi Arabia',
    'ANG': 'Angola',
    'GAM': 'Gambia',
    'TAH': 'Tahiti',
    'BER': 'Bermuda',
    'JAM': 'Jamaica',
    'LIE': 'Liechtenstein',
    'BFA': 'Burkina Faso',
    'IRQ': 'Iraq',
    'GEO': 'Georgia',
    'BOL': 'Bolivia',
    'CRC': 'Costa Rica',
    'MDA': 'Moldova',
    'CGO': 'Congo',
    'LUX': 'Luxembourg',
    'COK': 'Cook Islands',
    'HAI': 'Haiti',
    'TOG': 'Togo',
    'ZIM': 'Zimbabwe',
    'PRK': 'North Korea',
    'TRI': 'Trinidad and Tobago',
    'THA': 'Thailand',
    'LTU': 'Lithuania',
    'GAB': 'Gabon',
    'CUW': 'Curaçao',
    'SLE': 'Sierra Leone',
    'ZAM': 'Zambia',
    'COM': 'Comoros',
    'AFG': 'Afghanistan',
    'QAT': 'Qatar',
    'CYP': 'Cyprus',
    'UGA': 'Uganda',
    'ARM': 'Armenia',
    'UAE': 'United Arab Emirates',
    'BEN': 'Benin',
    'PAN': 'Panama',
    'ASA': 'American Samoa',
    'LBR': 'Liberia',
    'JOR': 'Jordan',
    'AND': 'Andorra',
    'PLE': 'Palestine',
    'EQG': 'Equatorial Guinea',
    'BHR': 'Bahrain',
    'DOM': 'Dominican Republic',
    'MOZ': 'Mozambique',
    'SLV': 'El Salvador',
    'KEN': 'Kenya',
    'SUR': 'Suriname',
    'MTQ': 'Martinique',
    'GLP': 'Guadeloupe',
    'LIB': 'Lebanon',
    'AZE': 'Azerbaijan',
    'MLT': 'Malta',
    'HON': 'Honduras',
    'CTA': 'Central African Republic',
    'CUB': 'Cuba',
    'MTN': 'Mauritania',
    'TGA': 'Tonga',
    'PHI': 'Philippines',
    'TAN': 'Tanzania',
    'OMA': 'Oman',
    'GUY': 'Guyana',
    'MAD': 'Madagascar',
    'EST': 'Estonia',
    'FRO': 'Faroe Islands',
    'KUW': 'Kuwait',
    'TUV': 'Tuvalu',
    'BDI': 'Burundi',
    'SOM': 'Somalia',
    'KAZ': 'Kazakhstan',
    'LBY': 'Libya',
    'NIG': 'Niger',
    'PUR': 'Puerto Rico',
    'GIB': 'Gibraltar',
    'GUF': 'French Guiana',
    'NAM': 'Namibia',
    'STP': 'São Tomé and Príncipe',
    'TJK': 'Tajikistan',
    'GRN': 'Grenada',
    'ETH': 'Ethiopia',
    'ATG': 'Antigua and Barbuda',
    'RWA': 'Rwanda',
    'ERI': 'Eritrea',
    'VIE': 'Vietnam',
    'SKN': 'Saint Kitts and Nevis',
    'TKM': 'Turkmenistan',
    'FSM': 'Micronesia',
    'SUD': 'Sudan',
    'MSR': 'Montserrat',
    'KGZ': 'Kyrgyzstan',
    'GUA': 'Guatemala',
    'YEM': 'Yemen',
    'SMR': 'San Marino',
    'MWI': 'Malawi',
    'TLS': 'Timor-Leste',
    'TPE': 'Chinese Taipei',
    'SSD': 'South Sudan',
    'NEP': 'Nepal',
    'ARU': 'Aruba',
    'CHA': 'Chad',
    'SRI': 'Sri Lanka',
    'SMN': 'Saint Martin',
    'LES': 'Lesotho',
    'BRB': 'Barbados',
    'BAH': 'Bahamas',
    'LCA': 'Saint Lucia',
    'VIN': 'Saint Vincent and the Grenadines',
    'GUM': 'Guam',
    'VGB': 'British Virgin Islands',
    'BLZ': 'Belize',
    'NCA': 'Nicaragua',
    'MRI': 'Mauritius',
    'MAC': 'Macau',
    'PAK': 'Pakistan',
    'MYA': 'Myanmar',
    'CAY': 'Cayman Islands',
    'BOT': 'Botswana',
    'SMA': 'Sint Maarten',
    'VIR': 'U.S. Virgin Islands',
    'REU': 'Réunion',
    'DMA': 'Dominica',
    'TCA': 'Turks and Caicos Islands',
    'BAN': 'Bangladesh',
    'AIA': 'Anguilla',
    'SEY': 'Seychelles',
    'NMI': 'Northern Mariana Islands',
    'MAY': 'Mayotte',
    'DJI': 'Djibouti',
    'MGL': 'Mongolia',
    'SWZ': 'Eswatini (Swaziland)',
    'LAO': 'Laos',
    'BOE': 'Bonaire',
    'CAM': 'Cambodia',
    'MDV': 'Maldives',
    'MON': 'Monaco'
}

def prepare_medium_fm_data(fm_filepath):
    """
    
    Prepare the Football Manager data from Medium for analysis.
    Not needed for the ones scraped myself

    """
    fm_df = pd.read_csv(fm_filepath)

    print(f"{get_current_time()} Preparing Football Manager data...")

    fm_df.columns = [x.strip() for x in fm_df.columns]

    for col in fm_df.columns:
        try:
            fm_df[col] = fm_df[col].str.strip()
        except AttributeError:
            continue

    fm_df['date_of_birth'] = (pd.to_datetime(fm_df['DoB'].str.strip().str.split(' ').str[0]).dt.date).astype(str)

    fm_df['nationality'] = fm_df['Nat'].str.strip().replace(country_names)
    fm_df['date_of_birth_nationality']= fm_df['date_of_birth'] + '_' + fm_df['nationality']

    new_filepath = fm_filepath.replace('.csv','_prepared.csv')
    fm_df.to_csv(new_filepath, index=False)
    print(f"{get_current_time()} Football Manager data prepared and saved to {new_filepath}")

def prepare_fifa_data():
    fifa_filepath = 'data/fifa_data/male_players.csv'

    fifa_df = pd.read_csv(fifa_filepath,low_memory=False)
    fifa_df['date_of_birth'] = (pd.to_datetime(fifa_df['dob'],format='%Y-%m-%d').dt.date).astype(str)
    fifa_df['nationality'] = fifa_df['nationality_name']
    fifa_df['date_of_birth_nationality']= fifa_df['date_of_birth'] + '_' + fifa_df['nationality']
    # TODO: Take this out
    fifa_df = fifa_df[fifa_df['fifa_version']==24]

    new_filepath = fifa_filepath.replace('.csv','_prepared.csv')
    fifa_df.to_csv(new_filepath, index=False)

    print(f"{get_current_time()} Fifa data prepared and saved to {new_filepath}\n")

def prepare_football_lineups_player_data(football_lineups_players_filepath):

    print(f"{get_current_time()} Preparing Football Lineups player data...")

    fl_players = pd.read_csv(football_lineups_players_filepath)
    fl_players['date_of_birth'] = (pd.to_datetime(fl_players['date_of_birth']).dt.date).astype(str)
    fl_players['date_of_birth_nationality']= fl_players['date_of_birth'] + '_' + fl_players['nationality']

    new_filepath = football_lineups_players_filepath.replace('.csv','_prepared.csv')
    fl_players.to_csv(new_filepath, index=False)

    print(f"{get_current_time()} Football Lineups data prepared and saved to {new_filepath}")

def get_fuzz_score(row):

    lineupsdotcom_full_name = row['full_name']
    lineupsdotcom_short_name = row['short_name_fl']
    rating_name = row['long_name']

    if pd.isna(rating_name):
        return np.nan
    
    full_name_fuzz_score = fuzz.token_set_ratio(lineupsdotcom_full_name, rating_name)
    short_name_fuzz_score = fuzz.token_set_ratio(lineupsdotcom_short_name, rating_name)

    overall_fuzz_score = np.maximum(full_name_fuzz_score, short_name_fuzz_score)
    return overall_fuzz_score

def merge_ratings_and_fl_players(fm_filepath, fl_players_filepath):
    """
    Merge Football Manager and Football Lineups player data.
    """
    print(f"{get_current_time()} Merging Football Manager and Football Lineups player data...")

    fm_df = pd.read_csv(fm_filepath)
    fl_players = pd.read_csv(fl_players_filepath)

    merged = pd.merge(fl_players, fm_df, left_on='date_of_birth', right_on='date_of_birth', how='left', suffixes=('_fl', '_fm'))
    merged['fuzz_score'] = merged.apply(get_fuzz_score, axis=1)

    merged.sort_values(by=['full_name','fuzz_score'], ascending=False, inplace=True)
    merged.drop_duplicates(subset='full_name', keep='first',inplace=True)

    cutoff_score = 69

    # Remove players that didnt seem to be able to match 
    merged = merged[merged['fuzz_score'] >= cutoff_score]

    filepath = 'data/merged_datasets/merged_fm_fl_players.csv'
    merged.to_csv(filepath, index=False)
    print(f"{get_current_time()} Merged player data saved to {filepath}")


# fm_file_path = 'data/fm_data/fm24/epl.rtf'
# rtf_file_to_csv(fm_file_path)

# fm_filepath = 'data/fm_data/fm2023.csv'
# prepare_medium_fm_data(fm_filepath)


prepare_fifa_data()
football_lineups_players_filepath = 'data/football_lineups/player_dataset/players_dataset.csv'
prepare_football_lineups_player_data(football_lineups_players_filepath)

# merge_ratings_and_fl_players('data/fm_data/fm2023_prepared.csv', 'data/football_lineups/player_dataset/players_dataset_prepared.csv')  
merge_ratings_and_fl_players('data/fifa_data/male_players_prepared.csv', 'data/football_lineups/player_dataset/players_dataset_prepared.csv')  

