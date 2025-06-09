import re
import os
import glob

filepath = 'data/football_lineups/season_match_number_html_files/'

def write_list_to_text_file(list, filepath):
    with open(filepath, 'w+') as f:
        for line in list:
            f.write(f"{line}\n")

    f.close()

    print(f"List of length {len(list)} written to {filepath} successfully.")

def extract_match_numbers(filepath):
    for filename in glob.glob(os.path.join(filepath, '*.html')): #only process .JSON files in folder. 
        with open(filename, 'r', encoding='utf-8') as f:
            html_content = f.read()
        f.close()
        
        # Step 2: Define the regular expression to find match numbers
        # The regex looks for '/match/', then captures one or more digits, then expects a '/'
        regex_pattern = r"/match/(\d+)/"

        # Step 3: Find all occurrences of the pattern in the HTML content
        # re.findall will return a list of all captured groups.
        # Since our capturing group is (\d+), it will return a list of strings, where each string is a match number.
        match_numbers = re.findall(regex_pattern, html_content)

        filename_to_write = filename.split('/')[-1].replace('.html','')  # Get the filename from the full path
        filepath_to_write = f"data/football_lineups/extracted_match_numbers/{filename_to_write}_match_numbers.txt"

        write_list_to_text_file(
            list = match_numbers,
            filepath=filepath_to_write)

extract_match_numbers(filepath)