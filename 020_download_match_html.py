from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import glob
import os
# 020_download_match_html.py
# This script downloads match HTML files from the Football Lineups website based on match codes.
# It reads match codes from a text file, constructs URLs for each match, and downloads the HTML content.


def create_match_url(match_code):
    """
    Create a match URL based on the match code.
    """
    return f"https://m.football-lineups.com/match/{match_code}/"

def read_text_file_to_list(filepath):
    """
    Read a text file and return its contents as a list.
    Each line in the file becomes an element in the list.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    f.close()
    return [line.strip() for line in lines]


def download_match_html(urls,time_delay=20):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    print('Downloading Match HTML Files...')

    for url in urls:
        print(f"Processing URL: {url}")
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        match_code = url.split("/")[-2]  # Extract match code from URL

        # Check if the request was successful
        if response.status_code == 200:
            # Save the HTML content to a file
            with open(f"data/football_lineups/downloaded_lineup_html_files/match_data_{match_code}.html", "w", encoding="utf-8") as file:
                file.write(response.text)
                file.close()
            print(f"HTML for match {match_code} saved successfully.")
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
        print(f"Waiting for {time_delay} seconds before the next request...")
        time.sleep(time_delay)  # Delay to avoid overwhelming the server
    print("\n\nAll match HTML files downloaded successfully :).")

def get_all_match_codes(filepath):
    """
    Get all match codes from the text file.
    """
    all_match_codes = []
    for filename in glob.glob(os.path.join(filepath, '*.txt')): #only process .JSON files in folder. 
        match_codes = read_text_file_to_list(filename)
        all_match_codes += match_codes

    return all_match_codes

match_codes = get_all_match_codes('data/football_lineups/extracted_match_numbers/')
urls = [create_match_url(code) for code in match_codes]

print(f'Downloading from {len(urls)} URLs...')

download_match_html(urls, time_delay=31)
