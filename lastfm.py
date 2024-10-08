import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')

def lastfm_get_artist_info(artist_name):
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_name}&api_key={API_KEY}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        artist_info = response.json()
        print(artist_info)
    else:
        print(f"Error: {response.status_code}")