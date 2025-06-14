
import time
import glob
import os
import random

from utils import get_current_time, get_scrapingbee_response, read_text_file_to_list

# 020_download_player_html.py
# This script downloads player HTML files from the Football Lineups website based on player codes.
# It reads player codes from a text file, constructs URLs for each player, and downloads the HTML content.


def create_player_url(player_code):
    """
    Create a player URL based on the player code.
    """
    return f"https://m.football-lineups.com/footballer/{player_code}/"


def download_player_html(urls,time_delay=20):

    if len(urls) == 0:
        print(f"{get_current_time()} No URLs to download. Exiting.")
        return None

    print(f'{get_current_time()} Downloading player HTML Files...')

    for url in urls:
        try:
            response = get_scrapingbee_response(url)
        except:
            print(f"{get_current_time()} failed to download {url} due to response error")
            continue
        
        player_code = url.split("/")[-2]  # Extract player code from URL

        # Check if the request was successful
        if response.status_code == 200:
            # Save the HTML content to a file
            with open(f"data/football_lineups/downloaded_player_html_files/player_data_{player_code}.html", "w", encoding="utf-8") as file:
                file.write(response.text)
                file.close()
            print(f"{get_current_time()} HTML for player {player_code} saved successfully.\n")
        else:
            print(f"{get_current_time()} Failed to retrieve the page. Status code: {response.status_code}")
        print(f"{get_current_time()} Waiting for {time_delay} seconds before the next request...")

        randomised_time_delay = random.randint(time_delay-2, time_delay+2)  # Random delay between 10 and 30 seconds
        print(f"Next request will be delayed by {randomised_time_delay} seconds.")
        time.sleep(randomised_time_delay)  

    print(f"\n\n {get_current_time()} All player HTML files downloaded successfully :).")

def get_all_player_codes(filepath):
    """
    Get all player codes from the text file.
    """

    player_codes = read_text_file_to_list(filepath)

    return player_codes

def get_player_codes_to_be_downloaded(filepath):
    """
    Get player codes that have not been downloaded yet.
    """
    all_player_codes = get_all_player_codes(filepath)
    print(len(all_player_codes))
    player_codes_to_download = []

    for player_code in all_player_codes:
        try:
            with open(f"data/football_lineups/downloaded_player_html_files/player_data_{player_code}.html", "r", encoding="utf-8") as html_file:
                html_content = html_file.read()
                if 'FootballLineups' in html_content:
                    print(f"player code {player_code} already downloaded.")
                else:
                    print(f"player code {player_code} not downloaded or has no lineups. Adding to download list.")
                    player_codes_to_download.append(player_code)    
        except FileNotFoundError:
            print(f"player code {player_code} not found. Adding to download list.")
            player_codes_to_download.append(player_code)
    
    return player_codes_to_download


player_codes_to_be_downloaded = get_player_codes_to_be_downloaded('data/football_lineups/extracted_player_codes/player_codes.txt')
urls = [create_player_url(code) for code in player_codes_to_be_downloaded]
print(f'Downloading from {len(urls)} URLs...')

download_player_html(urls, time_delay=5)
