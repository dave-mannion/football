from bs4 import BeautifulSoup
import os
import json
import glob
from utils import get_current_time

def extract_player_data(html_content: str) -> dict:
    """
    Extracts player information from an HTML file.

    The function is designed to be robust and handle cases where some information
    might be missing in the HTML structure.

    Args:
        html_content: A string containing the HTML of the player's page.

    Returns:
        A dictionary with the extracted information:
        {
            'short_name': 'Common Name',
            'full_name': 'Full Legal Name',
            'date_of_birth': 'DD-Mon-YY',
            'height': 'X.XX m',
            'nationality': 'Country',
            'play_style': 'Player Position/Style'
        }
        Values will be None if the information could not be found.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    player_info = {
        'short_name': None,
        'full_name': None,
        'date_of_birth': None,
        'height': None,
        'nationality': None,
        'play_style': None,
    }

    # --- 1. Extract Names ---
    try:
        h1_tag = soup.find('h1', id='page-title')
        if h1_tag:
            # The short name is the main text content of the H1 tag itself.
            player_info['short_name'] = h1_tag.get_text(strip=True)
            
            # The full name is the text node immediately following the H1 tag.
            if h1_tag.next_sibling and isinstance(h1_tag.next_sibling, str):
                player_info['full_name'] = h1_tag.next_sibling.strip()
    except AttributeError:
        print("Warning: Could not extract player names.")

    # --- 2. Extract Date of Birth ---
    # The DOB is in a table row, identified by a 'cake' icon.
    try:
        cake_icon = soup.find('i', class_='fa-cake-candles')
        if cake_icon:
            dob_td = cake_icon.find_parent('tr').find_all('td')[1]
            full_dob_text = dob_td.get_text(strip=True)
            player_info['date_of_birth'] = full_dob_text.split('(')[0].strip()
    except (AttributeError, IndexError):
        print("Warning: Could not extract date of birth.")

    # --- 3. Extract Height ---
    # The height is in a table row, identified by a 'ruler' icon.
    try:
        ruler_icon = soup.find('i', class_='fa-ruler-vertical')
        if ruler_icon:
            height_td = ruler_icon.find_parent('tr').find_all('td')[1]
            player_info['height'] = height_td.get_text(strip=True)
    except (AttributeError, IndexError):
        print("Warning: Could not extract height.")
        
    # --- 4. Extract Nationality ---
    # Extracted from the structured JSON-LD data block for better reliability.
    try:
        json_ld_script = soup.find('script', type='application/ld+json')
        if json_ld_script:
            data = json.loads(json_ld_script.string)
            player_info['nationality'] = data.get('nationality')
    except (AttributeError, json.JSONDecodeError):
        print("Warning: Could not extract nationality from JSON-LD.")

    # --- 5. Extract Play Style ---
    # Found inside a <font> tag near the top of the player info section.
    try:
        style_font_tag = soup.find('font', attrs={'color': '#1111FF'})
        if style_font_tag:
            player_info['play_style'] = style_font_tag.get_text(strip=True)
    except AttributeError:
        print("Warning: Could not extract play style.")

    return player_info


if __name__ == "__main__":
    print(f"{get_current_time()} Starting data extraction from HTML files...")
    path = "data/football_lineups/downloaded_player_html_files/"
    failed_to_extract_player_codes = []
    for filename in glob.glob(os.path.join(path, '*.html')): #only process .JSON files in folder. 
        player_code = filename.split("/")[-1].replace("player_data_", "").replace(".html", "")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                html_file_content = f.read()
        except FileNotFoundError:
            print(f"Error: '{filename}' not found. Please ensure the file exists in the same directory.")
            exit()

        extracted_info = extract_player_data(html_file_content)
        extracted_info['id']=player_code

        if extracted_info:
            new_filename = f'data/football_lineups/extracted_player_json_files/extracted_player_data_{player_code}.json'
            with open(new_filename, 'w') as f:
                json.dump(extracted_info, f, indent=4)
            f.close()
            # print(f'{get_current_time()} Data sucessfully extracted to {new_filename}')
        else:
            print(f"{get_current_time()} Failed to extract data.")
            failed_to_extract_player_codes.append(player_code)
    if len(failed_to_extract_player_codes) > 0:
        print('Failed player Codes:',failed_to_extract_player_codes)    
    print(f"{get_current_time()} Finished data extraction to JSON files.\n")
    