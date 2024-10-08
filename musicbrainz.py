import requests

def musicbrainz_get_artist_id(artist_name):
    url = f"https://musicbrainz.org/ws/2/artist/?query=artist:{artist_name}&fmt=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['artists']:
            return data['artists'][0]['id']
    return None

def musicbrainz_get_albums_by_artist(artist_name):
    artist_id = musicbrainz_get_artist_id(artist_name)
    if not artist_id:
        print(f"Artist {artist_name} not found.")
        return

    url = f"https://musicbrainz.org/ws/2/release-group?artist={artist_id}&type=album&fmt=json"
    response = requests.get(url)
    if response.status_code == 200:
        albums = response.json()
        for album in albums['release-groups']:            
            print(album['title']+ " - " + album['first-release-date'])
    else:
        print(f"Error: {response.status_code}")
