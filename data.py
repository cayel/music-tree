import sqlite3
import json

def insert_sample_data():
    """Insert sample data into the database."""
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()

    # Load sample data from JSON file
    with open('./sample_data/sample_data.json', 'r') as file:
        data = json.load(file)

    # Insert artists
    for artist in data['artists']:
        cursor.execute('''
            INSERT INTO Artist (first_name, last_name) VALUES (?, ?)
        ''', (artist['first_name'], artist['last_name']))
        
    # Insert bands
    for band in data['bands']:
        cursor.execute('''
            INSERT INTO Band (name) VALUES (?)
        ''', (band['name'],))

   # Insert albums
    for album in data['albums']:
        cursor.execute('''
            INSERT INTO Album (title, release_date, band_id) VALUES (?, ?, ?)
        ''', (album['title'], album['release_date'], album['band_id']))

    # Insert band-artist relationships
    for ba in data['band_artists']:
        cursor.execute('''
            INSERT INTO BandArtist (band_id, artist_id) VALUES (?, ?)
        ''', (ba['band_id'], ba['artist_id']))

    # Insert artist-album relationships
    for aa in data['artist_albums']:
        cursor.execute('''
            INSERT INTO ArtistAlbum (artist_id, album_id) VALUES (?, ?)
        ''', (aa['artist_id'], aa['album_id']))
    
    conn.commit()
    conn.close()

def fetch_data():
    """Fetch and display data from the database."""
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT a.first_name, a.last_name, b.name, al.title, al.release_date
        FROM Artist a
        JOIN BandArtist ba ON a.id = ba.artist_id
        JOIN Band b ON ba.band_id = b.id
        JOIN Album al ON b.id = al.band_id
    ''')
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()