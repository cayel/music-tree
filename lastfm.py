import requests
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

API_KEY = os.getenv('API_KEY')

class AlbumInfo:
    def __init__(self, title, artist, image_small_url, image_medium_url, image_large_url, year=None):
        self.title = title
        self.artist = artist
        self.image_small_url = image_small_url
        self.image_medium_url = image_medium_url
        self.image_large_url = image_large_url
        self.year = year

    def __str__(self):
        return f"{self.title} - {self.artist}"
       

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

def get_lastfm_topsters():
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user=cayel69&api_key={API_KEY}&format=json"
    response = requests.get(url)
    data = response.json()
    albums = []
    for album in data['topalbums']['album']:
        album_info = AlbumInfo(album['name'], album['artist']['name'], album['image'][0]['#text'], album['image'][1]['#text'], album['image'][2]['#text']) 
        albums.append(album_info)
    return(albums)

def generate_css(color):
    return f"""
    <style>
    .album-info {{
        font-size: 10px;
        line-height: 1.2;
        margin-top: 0;
        color: white;
    }}
    .album-table {{
        width: 100%;
        border-collapse: collapse;
        border: 1px solid {color}; 
        background-color: {color}; 
    }}
    .album-table td {{
        padding: 2px;
        border: none;
    }}
    .album-table tr {{
        padding: 2px;
        border: none;
    }}
    .album-table img {{
        width: 100%;
    }}
    </style>
    """

def generate_table_html(albums, num_columns):
    table_html = '<table class="album-table">'
    for i in range(0, len(albums), num_columns):
        table_html += '<tr>'
        for j in range(num_columns):
            if i + j < len(albums):
                table_html += f'<td><img src="{albums[i + j].image_large_url}" alt="Album cover"></td>'
            else:
                table_html += '<td></td>'
        table_html += '<td rowspan="1">'
        for j in range(num_columns):
            if i + j < len(albums):
                table_html += f'<div class="album-info">{albums[i + j].title} - {albums[i + j].artist}</div>'
        table_html += '</td></tr>'
    table_html += '</table>'
    return table_html

def build_album_grid(albums, num_columns=5, color='black'):
    css = generate_css(color)
    table_html = generate_table_html(albums, num_columns)
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(table_html, unsafe_allow_html=True)

