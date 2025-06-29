
import time
import glob
import os
import random

from utils import get_current_time, get_scrapingbee_response, read_text_file_to_list

# 020_download_match_html.py
# This script downloads match HTML files from the Football Lineups website based on match codes.
# It reads match codes from a text file, constructs URLs for each match, and downloads the HTML content.


def create_match_url(match_code):
    """
    Create a match URL based on the match code.
    """
    return f"https://m.football-lineups.com/match/{match_code}/"


def download_match_html(urls,time_delay=20):

    if len(urls) == 0:
        print(f"{get_current_time()} No URLs to download. Exiting.")
        return None

    print(f'{get_current_time()} Downloading Match HTML Files...')

    for url in urls:
        try:
            response = get_scrapingbee_response(url)
        except:
            continue

        match_code = url.split("/")[-2]  # Extract match code from URL

        # Check if the request was successful
        if response.status_code == 200:
            # Save the HTML content to a file
            with open(f"data/football_lineups/downloaded_lineup_html_files/match_data_{match_code}.html", "w", encoding="utf-8") as file:
                file.write(response.text)
                file.close()
            print(f"{get_current_time()} HTML for match {match_code} saved successfully.\n")
        else:
            print(f"{get_current_time()} Failed to retrieve the page. Status code: {response.status_code}")
        print(f"Waiting for {time_delay} seconds before the next request...")

        randomised_time_delay = random.randint(time_delay-1, time_delay+1)  # Random delay between 10 and 30 seconds
        print(f"Next request will be delayed by {randomised_time_delay} seconds.")
        time.sleep(randomised_time_delay)  

    print(f"\n\n {get_current_time()} All match HTML files downloaded successfully :).")

def get_all_match_codes(filepath):
    """
    Get all match codes from the text file.
    """
    all_match_codes = []
    for filename in glob.glob(os.path.join(filepath, '*.txt')): 
        match_codes = read_text_file_to_list(filename)
        all_match_codes += match_codes

    return all_match_codes

def get_match_codes_to_be_downloaded(filepath):
    """
    Get match codes that have not been downloaded yet.
    """
    all_match_codes = get_all_match_codes(filepath)
    print(len(all_match_codes))
    match_codes_to_download = []

    for match_code in all_match_codes:
        try:
            with open(f"data/football_lineups/downloaded_lineup_html_files/match_data_{match_code}.html", "r", encoding="utf-8") as html_file:
                html_content = html_file.read()
                if 'Lineups' in html_content:
                    print(f"Match code {match_code} already downloaded.")
                else:
                    print(f"Match code {match_code} not downloaded or has no lineups. Adding to download list.")
                    match_codes_to_download.append(match_code)    
        except FileNotFoundError:
            print(f"Match code {match_code} not found. Adding to download list.")
            match_codes_to_download.append(match_code)
    
    return match_codes_to_download


match_codes_to_be_downloaded = get_match_codes_to_be_downloaded('data/football_lineups/extracted_match_codes')
urls = [create_match_url(code) for code in match_codes_to_be_downloaded]

print(f'Downloading from {len(urls)} URLs...')

download_match_html(urls, time_delay=5)
