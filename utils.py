import datetime
from scrapingbee import ScrapingBeeClient
import json

def get_current_time():
    """
    Get the current time in a formatted string.
    """
    return datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")

def get_scrapingbee_response(url,verbose=0):
    """
    Get a ScrapingBee client instance.
    """
    if verbose > 0:
        print(f"{get_current_time()} Getting ScrapingBee response for URL: {url}")
    API_KEY = 'TAKN8UIR1O36S12TWBADOT7ULZPBQ23YR9YB7REMVFWLS833MF4B79RBRQC6AEXDOJZXB2C45KB8CILN' 
    client = ScrapingBeeClient(api_key=API_KEY)

    response = client.get(url,params={
        'premium_proxy': 'True',
        'render_js':'False'
        })
    
    return response

def write_list_to_text_file(list, filepath):
    with open(filepath, 'w+') as f:
        for line in list:
            f.write(f"{line}\n")

    f.close()

    print(f"List of length {len(list)} written to {filepath} successfully.")

def read_text_file_to_list(filepath):
    """
    Read a text file and return its contents as a list.
    Each line in the file becomes an element in the list.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    f.close()
    return [line.strip() for line in lines]

def load_json(file_path):
    """
    Load a JSON Lines file into a list of dictionaries.
    
    Args:
        file_path (str): Path to the JSON Lines file.
        
    Returns:
        list: A list of dictionaries representing the JSON objects in the file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
