

from bs4 import BeautifulSoup
import re
import json
import glob
import os
from utils import get_current_time


# Helper function to parse lineup and substitute tables for a team
def parse_lineup_tables(team_lineup_h1_tag, team_name_key, lineups_dict):
    """
    Parses starters, substitutes, and coach for a given team.
    Modifies lineups_dict directly.
    """
    if not team_lineup_h1_tag:
        print(f"Warning: Lineup H1 for {team_name_key} not found. Skipping lineup parsing.")
        return

    starters_section = team_lineup_h1_tag.find_next_sibling('section', id=lambda x: x and x.startswith('team-lineup'))
    subs_section = None
    if starters_section:
            subs_section = starters_section.find_next_sibling('section', id=lambda x: x and x.startswith('tmlnps'))

    if starters_section:
        for row in starters_section.find('tbody').find_all('tr'):
            cells = row.find_all('td')
            if len(cells) >= 2:
                number = cells[0].get_text(strip=True)
                player_name_tag = cells[1].find('a')
                player_name = "Unknown Player"
                player_id = "Unknown"
                if player_name_tag:
                    player_name = player_name_tag.get_text(strip=True)
                    href = player_name_tag.get('href', '')
                    id_match = re.search(r'/footballer/(\d+)', href)
                    if id_match:
                        player_id = id_match.group(1)
                
                sub_off_time = None
                if len(cells) > 2 and cells[2].get_text(strip=True) and "'" in cells[2].get_text(strip=True): # Substituted off
                    sub_off_time = cells[2].get_text(strip=True).replace(" '", "'")

                lineups_dict[team_name_key]['starters'].append({
                    "number": number,
                    "name": player_name,
                    "id": player_id,
                    "sub_off_at": sub_off_time
                })
    else:
        print(f"Warning: Starters section for {team_name_key} not found.")

    if subs_section:
        for row in subs_section.find('tbody').find_all('tr'):
            cells = row.find_all('td')
            if len(cells) >= 3: # Need at least 3 cells for sub info
                sub_on_time_text = cells[2].get_text(strip=True)
                if sub_on_time_text and "'" in sub_on_time_text: # Player came on
                    number = cells[0].get_text(strip=True)
                    player_name_tag = cells[1].find('a')
                    player_name = "Unknown Player"
                    player_id = "Unknown"
                    if player_name_tag:
                        player_name = player_name_tag.get_text(strip=True)
                        href = player_name_tag.get('href', '')
                        id_match = re.search(r'/footballer/(\d+)', href)
                        if id_match:
                            player_id = id_match.group(1)

                    lineups_dict[team_name_key]['substitutes_played'].append({
                        "number": number,
                        "name": player_name,
                        "id": player_id,
                        "sub_on_at": sub_on_time_text.replace(" '", "'")
                    })
        
        # Find Coach (located after the substitutes section)
        coach_b_tag = subs_section.find_next_sibling('b', string=re.compile(r'Coach', re.IGNORECASE))
        if coach_b_tag and coach_b_tag.next_sibling:
            # The name is usually in the next_sibling text node, formatted like '   : Moyes  '
            coach_text = coach_b_tag.next_sibling
            if isinstance(coach_text, str):
                coach_name = coach_text.strip().lstrip(':').strip()
                if coach_name:
                        lineups_dict[team_name_key]['coach'] = coach_name
                        # NOTE: The provided HTML does not contain a link or ID for the coach.
                        lineups_dict[team_name_key]['coach_id'] = "Unknown"
    else:
        print(f"Warning: Substitutes section for {team_name_key} not found, cannot find coach.")


def extract_match_data(html_content):
    """
    Extracts match data from the HTML content of a football-lineups.com match page.

    Args:
        html_content (str): The HTML content of the match page.

    Returns:
        dict: A dictionary containing the extracted match data.
              Returns None if essential data cannot be found.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {}

    # 1. Identify Main Title Team Links and Hrefs (for matching lineup H1s)
    title_h1_main = soup.find('h1', id='page-title nowrap')
    if not title_h1_main:
        print("Error: Main title H1 (id='page-title nowrap') not found.")
        return None
    
    team_links_in_main_title = title_h1_main.find_all('a', href=lambda x: x and '/team/' in x)
    if len(team_links_in_main_title) < 2:
        print("Error: Team links not found in main title H1.")
        return None

    main_title_home_team_href = team_links_in_main_title[0]['href']
    main_title_away_team_href = team_links_in_main_title[1]['href']
    
    # Initialize team names with potentially short versions from main title (as fallback)
    data['home_team'] = team_links_in_main_title[0].get_text(strip=True)
    data['away_team'] = team_links_in_main_title[1].get_text(strip=True)

    # 2. Find Lineup H1s and determine definitive Home/Away Team Names
    # These H1s usually have the fuller team names.
    home_lineup_h1_tag = None
    away_lineup_h1_tag = None
    
    all_lineup_h1_candidates = soup.find_all('h1', id='page-title') # These are <h1 id="page-title"> for lineups

    for h1_tag_candidate in all_lineup_h1_candidates:
        lineup_h1_a_tag = h1_tag_candidate.find('a', href=lambda x: x and x.startswith('/team/'))
        if not lineup_h1_a_tag:
            continue
        
        current_lineup_href = lineup_h1_a_tag['href']
        current_lineup_team_name_display = lineup_h1_a_tag.get_text(strip=True)

        # Match based on href. Lineup href is usually shorter or equal.
        if main_title_home_team_href.startswith(current_lineup_href):
            home_lineup_h1_tag = h1_tag_candidate
            data['home_team'] = current_lineup_team_name_display # Update to full name
        elif main_title_away_team_href.startswith(current_lineup_href):
            away_lineup_h1_tag = h1_tag_candidate
            data['away_team'] = current_lineup_team_name_display # Update to full name
    
    if not home_lineup_h1_tag:
        print(f"Warning: Home lineup H1 could not be definitively identified. Using fallback name: {data['home_team']}")
    if not away_lineup_h1_tag:
        print(f"Warning: Away lineup H1 could not be definitively identified. Using fallback name: {data['away_team']}")

    # 3. Score (from main title h1)
    score_text_node = team_links_in_main_title[0].next_sibling
    if score_text_node and isinstance(score_text_node, str):
        score_parts = score_text_node.strip().split(':')
        if len(score_parts) == 2:
            data['home_score'] = score_parts[0].strip()
            data['away_score'] = score_parts[1].strip()
        else:
            data['home_score'], data['away_score'] = "N/A", "N/A"
            print(f"Warning: Could not parse score from '{score_text_node.strip()}'")
    else:
        data['home_score'], data['away_score'] = "N/A", "N/A"
        print("Warning: Score text not found or not a string.")

    # 4. Date and Time of the match
    meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
    full_date_str = "Unknown"
    if meta_desc_tag and meta_desc_tag.get('content'):
        meta_content = meta_desc_tag['content']
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', meta_content)
        if date_match:
            full_date_str = date_match.group(1)

    match_info_div = soup.find('div', class_='align-center col-expand')
    time_str = "Unknown"
    if match_info_div:
        matchday_link = match_info_div.find('a', href=lambda x: x and 'matchday' in x)
        if matchday_link and matchday_link.next_sibling:
            date_time_text = matchday_link.next_sibling.strip()
            time_match = re.search(r'(\d{2}:\d{2})', date_time_text)
            if time_match:
                time_str = time_match.group(1)
    data['match_datetime'] = f"{full_date_str} {time_str}" if full_date_str != "Unknown" and time_str != "Unknown" else "Unknown"

    # 5. Referee Name
    data['referee'] = "Unknown"
    data['referee_id'] = "Unknown"
    if match_info_div:
        referee_link = match_info_div.find('a', href=lambda x: x and '/referee/' in x)
        if referee_link:
            data['referee'] = referee_link.get_text(strip=True)
            ref_href = referee_link.get('href', '')
            id_match = re.search(r'/referee/(\d+)', ref_href)
            if id_match:
                data['referee_id'] = id_match.group(1)


    # 6. Who Scored (Goals) - This will now use the updated full team names
    data['goals'] = []
    events_table = soup.find('section', id='match-events')
    if events_table:
        for row in events_table.find('tbody').find_all('tr'):
            cells = row.find_all('td')
            if len(cells) < 6:
                continue

            goal_img_cell = cells[3]
            goal_img = goal_img_cell.find('img', title=lambda t: t and 'goal' in t.lower())

            if goal_img:
                time = cells[2].get_text(strip=True) + "'"
                goal_type_title = goal_img['title'].lower()
                
                goal_type = "Goal" 
                if "head goal" in goal_type_title: goal_type = "Head"
                elif "penalty goal" in goal_type_title: goal_type = "Penalty"

                scorer_name, scorer_id, team_scored, assist_by, assist_by_id = "Unknown", "Unknown", "Unknown", None, None
                
                # Check home scorer cell (index 0) OR away scorer cell (index 4)
                home_scorer_cell_content = cells[0].get_text(strip=True)
                away_scorer_cell_content = cells[4].get_text(strip=True)

                if home_scorer_cell_content: # Content in home scorer column
                    home_scorer_link = cells[0].find('a')
                    if home_scorer_link:
                        scorer_name = home_scorer_link.get_text(strip=True)
                        team_scored = data['home_team']
                        href = home_scorer_link.get('href', '')
                        id_match = re.search(r'/footballer/(\d+)', href)
                        if id_match:
                            scorer_id = id_match.group(1)

                        assist_img_home = home_scorer_link.find_next_sibling('img', title='Assist ')
                        if assist_img_home:
                            assist_link_home = assist_img_home.find_next_sibling('a')
                            if assist_link_home: 
                                assist_by = assist_link_home.get_text(strip=True)
                                href = assist_link_home.get('href', '')
                                id_match = re.search(r'/footballer/(\d+)', href)
                                if id_match:
                                    assist_by_id = id_match.group(1)

                elif away_scorer_cell_content: # Content in away scorer column
                    away_scorer_link = cells[4].find('a')
                    if away_scorer_link:
                        scorer_name = away_scorer_link.get_text(strip=True)
                        team_scored = data['away_team']
                        href = away_scorer_link.get('href', '')
                        id_match = re.search(r'/footballer/(\d+)', href)
                        if id_match:
                            scorer_id = id_match.group(1)

                        assist_img_away = away_scorer_link.find_next_sibling('img', title='Assist ')
                        if assist_img_away:
                            assist_link_away = assist_img_away.find_next_sibling('a')
                            if assist_link_away:
                                assist_by = assist_link_away.get_text(strip=True)
                                href = assist_link_away.get('href', '')
                                id_match = re.search(r'/footballer/(\d+)', href)
                                if id_match:
                                    assist_by_id = id_match.group(1)
                
                goal_event = {"time": time, "team": team_scored, "scorer": scorer_name, "scorer_id": scorer_id, "type": goal_type}
                if assist_by: 
                    goal_event["assisted_by"] = assist_by
                    goal_event["assisted_by_id"] = assist_by_id
                data['goals'].append(goal_event)
    else:
        print("Warning: Match events table not found.")

    # 7. Lineups - Initialize with definitive (fuller) team names
    data['lineups'] = {
        data['home_team']: {"coach": "Unknown", "coach_id": "Unknown", "starters": [], "substitutes_played": []},
        data['away_team']: {"coach": "Unknown", "coach_id": "Unknown", "starters": [], "substitutes_played": []}
    }
    
    # Parse lineups using the identified H1 tags and full team names
    parse_lineup_tables(home_lineup_h1_tag, data['home_team'], data['lineups'])
    parse_lineup_tables(away_lineup_h1_tag, data['away_team'], data['lineups'])

    return data

# def get_current_time():
#     """
#     Get the current time in a formatted string.
#     """
#     return datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")

# --- START OF SCRIPT EXECUTION ---

if __name__ == "__main__":
    print(f"{get_current_time()} Starting data extraction from HTML files...")
    path = "data/football_lineups/downloaded_lineup_html_files/"
    failed_to_extract_match_codes = []
    for filename in glob.glob(os.path.join(path, '*.html')): #only process .JSON files in folder. 
        match_code = filename.split("/")[-1].replace("match_data_", "").replace(".html", "")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                html_file_content = f.read()
        except FileNotFoundError:
            print(f"Error: '{filename}' not found. Please ensure the file exists in the same directory.")
            exit()

        extracted_info = extract_match_data(html_file_content)

        if extracted_info:
            new_filename = f'data/football_lineups/extracted_match_json_files/extracted_match_data_{match_code}.json'
            with open(new_filename, 'w') as f:
                json.dump(extracted_info, f, indent=4)
            f.close()
            # print(f'{get_current_time()} Data sucessfully extracted to {new_filename}')
        else:
            print(f"{get_current_time()} Failed to extract data.")
            failed_to_extract_match_codes.append(match_code)
    if len(failed_to_extract_match_codes) > 0:
        print('Failed Match Codes:',failed_to_extract_match_codes)    
    print(f"{get_current_time()} Finished data extraction from HTML files...\n")