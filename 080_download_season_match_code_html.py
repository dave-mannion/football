
from utils import get_current_time, get_scrapingbee_response
import random
import time
# 080_download_season_match_code_html.py
# This script downloads season match code HTML files from the Football Lineups website.

league_names = [
    'FA-Premier-League',
    'La-Liga',
    'Bundesliga',
    'Serie-A',
    'Ligue-1',
    'Eredivisie',
    'Portuguese-Liga',
    'Scottish-Premiership',
    'The-Championship',
    'Champions-League'
    ]

years = [
    '2020--2021',
    '2021--2022',
    '2022--2023',
    '2023--2024',
    '2024--2025',
]

def create_season_match_code_html_url(league_name, years):
    """
    Create a URL for the season match code HTML page based on the league name and years.
    """
    base_url = "https://m.football-lineups.com/tourn/"
    return f"{base_url}{league_name}-{years}/"


def download_season_html(urls,time_delay=20):

    if len(urls) == 0:
        print(f"{get_current_time()} No URLs to download. Exiting.")
        return None

    print(f'{get_current_time()} Downloading Match HTML Files...')

    for url in urls:
        response = get_scrapingbee_response(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the HTML content to a file
            league_and_year = url.replace("https://m.football-lineups.com/tourn/","").replace("/", "")
            with open(f"data/football_lineups/season_match_code_html_files/{league_and_year}.html", "w", encoding="utf-8") as file:
                file.write(response.text)
                file.close()
            print(f"{get_current_time} HTML for match {league_and_year} saved successfully.\n")
        else:
            print(f"{get_current_time} Failed to retrieve the page. Status code: {response.status_code}")
        print(f"Waiting for {time_delay} seconds before the next request...")

        randomised_time_delay = random.randint(time_delay-1, time_delay+1)  # Random delay between 10 and 30 seconds
        print(f"Next request will be delayed by {randomised_time_delay} seconds.")
        time.sleep(randomised_time_delay)  

    print(f"\n\n {get_current_time()} All match HTML files downloaded successfully :).")

urls = [create_season_match_code_html_url(league_name, year) for league_name in league_names for year in years]

download_season_html(urls=urls, time_delay=3)