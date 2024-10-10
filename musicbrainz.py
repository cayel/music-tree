import requests
import json
import models


def musicbrainz_get_albums_by_artist_uid(artist_uid):
    url = f"https://musicbrainz.org/ws/2/release-group?artist={artist_uid}&type=album&fmt=json"
    response = requests.get(url)
    if response.status_code == 200:
        albums = response.json()
        for album in albums['release-groups']:            
            # display only if secondary_types is not present
            if not album['secondary-types']:
                albumInfo = models.Album(album['id'], album['title'], album['first-release-date'])
                print(albumInfo)
                print(json.dumps(album, indent=4, sort_keys=True))        
    else:
        print(f"Error: {response.status_code}")