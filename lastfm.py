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


def get_lastfm_album_image(artist, album):
    url = f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={API_KEY}&artist={artist}&album={album}&format=json"
    response = requests.get(url)
    data = response.json()
    return data['album']['image'][3]['#text']