from datetime import date
from typing import List

class Artist:
    def __init__(self, id: int, first_name: str, last_name: str, discogs_id: str = None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.discogs_id = discogs_id
        self.bands: List['Band'] = []
        self.albums: List['Album'] = []

    def join_band(self, band: 'Band'):
        if band not in self.bands:
            self.bands.append(band)
            band.members.append(self)
    
    def play_album(self, album: 'Album'):
        if album not in self.albums:
            self.albums.append(album)

class Band:
    def __init__(self, id: int, name: str, discogs_id: str = None):
        self.id = id
        self.name = name
        self.discogs_id = discogs_id
        self.records: List['Album'] = []
        self.members: List[Artist] = []

    def add_album(self, album: 'Album'):
        if album not in self.records:
            self.records.append(album)

class Album:
    def __init__(self, id: int, title: str, release_date: date, discogs_id: str = None):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.discogs = discogs_id
    # Display the album id, title and date when the object is printed
    def __str__(self):
        return f"{self.id}: {self.title} ({self.release_date})"

class ArtistAlbum:
    def __init__(self, artist: Artist, album: Album):
        self.artist = artist
        self.album = album