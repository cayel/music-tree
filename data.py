import sqlite3
import json

def insert_artist_album_relation(artist_id, album_id):
    """Insert a relation between an artist and an album."""
    ret = True
    try:
        conn = sqlite3.connect('music.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO ArtistAlbum (artist_id, album_id) VALUES (?, ?)
        ''', (artist_id, album_id))

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        ret = False
    finally:
        if conn:
            conn.close()
        return ret

def insert_artist_band_relation(artist_id, band_id):
    """Insert a relation between an artist and a band."""
    ret = True
    try:
        conn = sqlite3.connect('music.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO BandArtist (artist_id, band_id) VALUES (?, ?)
        ''', (artist_id, band_id))

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        ret = False
    finally:
        if conn:
            conn.close()
        return ret

def insert_album(title, release_date, discogs_id, band_id):
    """Insert an album into the database."""
    ret = True
    try:
        conn = sqlite3.connect('music.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Album (title, release_date, discogs_id, band_id) VALUES (?, ?, ?, ?)
        ''', (title, release_date, discogs_id, band_id))

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        ret = False
    finally:
        if conn:
            conn.close()
        return ret
    
def insert_artist(first_name, last_name, discogs_id):
    """Insert an artist into the database."""
    ret = True
    try:
        conn = sqlite3.connect('music.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Artist (first_name, last_name, discogs_id) VALUES (?, ?, ?)
        ''', (first_name, last_name, discogs_id))

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        ret = False
    finally:
        if conn:
            conn.close()
        return ret

def insert_band(name, discogs_id):
    """Insert a band into the database."""
    ret=True
    try:
        conn = sqlite3.connect('music.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Band (name, discogs_id) VALUES (?, ?)
        ''', (name, discogs_id))

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        ret=False
    finally:
        if conn:
            conn.close()
        return ret

def insert_uploaded_file(uploaded_file):
    # Read the content of the uploaded file
    file_content = uploaded_file.read()
    data = json.loads(file_content)
    insert_data(data)

def insert_local_file(filename):
    """Insert sample data into the database."""
    # Load sample data from JSON file
    with open(filename, 'r') as file:
        data = json.load(file)
    insert_data(data)

def insert_data(data):
    # Insert artists
    for artist in data['artists']:
        insert_artist(artist['first_name'], artist['last_name'], artist['discogs_id'])

    # Insert bands
    for band in data['bands']:
        insert_band(band['name'], band['discogs_id'])

   # Insert albums
    for album in data['albums']:
        insert_album(album['title'], album['release_date'], album['discogs_id'], album['band_id'])

    # Insert band-artist relationships
    for ba in data['band_artists']:
        insert_artist_band_relation(ba['artist_id'], ba['band_id'])

    # Insert artist-album relationships
    for aa in data['artist_albums']:
        insert_artist_album_relation(aa['artist_id'], aa['album_id'])
    
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

def export_data():
    """Export data from the database to a JSON file."""
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM Artist
    ''')
    artists = cursor.fetchall()

    cursor.execute('''
        SELECT * FROM Band
    ''')
    bands = cursor.fetchall()

    cursor.execute('''
        SELECT * FROM Album
    ''')
    albums = cursor.fetchall()

    cursor.execute('''
        SELECT * FROM BandArtist
    ''')
    band_artists = cursor.fetchall()

    cursor.execute('''
        SELECT * FROM ArtistAlbum
    ''')
    artist_albums = cursor.fetchall()

    conn.close()

    data = {
        'artists': artists,
        'bands': bands,
        'albums': albums,
        'band_artists': band_artists,
        'artist_albums': artist_albums
    }

    return(json.dumps(data, indent=4))
