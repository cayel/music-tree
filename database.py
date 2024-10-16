import sqlite3

def execute_query(query, params=()):
    """Execute a query and return the results."""
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def db_albums_count():
    """Count the number of albums in the database."""
    query = 'SELECT COUNT(*) FROM Album'
    count = execute_query(query)[0][0]
    return count

def db_bands_count():
    """Count the number of bands in the database."""
    query = 'SELECT COUNT(*) FROM Band'
    count = execute_query(query)[0][0]
    return count

def load_albums_with_band(band_name=None):
    """Load albums with their respective band names from the database."""
    if band_name:
        query = '''SELECT a.title, b.name FROM Album a JOIN Band b ON a.band_id = b.id WHERE b.name = ?'''
        rows = execute_query(query, (band_name,))
    else:
        query = '''SELECT a.title, b.name FROM Album a JOIN Band b ON a.band_id = b.id'''
        rows = execute_query(query)
    return rows

def create_database():
    """Create the SQLite database and tables."""
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()

    # Drop tables if they exist
    cursor.execute('DROP TABLE IF EXISTS Artist')
    cursor.execute('DROP TABLE IF EXISTS Band')
    cursor.execute('DROP TABLE IF EXISTS Album')
    cursor.execute('DROP TABLE IF EXISTS BandArtist')
    cursor.execute('DROP TABLE IF EXISTS ArtistAlbum')
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Artist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            discogs_id TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Band (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            discogs_id TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Album (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            release_date DATE NOT NULL,
            discogs_id TEXT UNIQUE,
            band_id INTEGER,
            FOREIGN KEY (band_id) REFERENCES Band(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BandArtist (
            band_id INTEGER,
            artist_id INTEGER,
            FOREIGN KEY (band_id) REFERENCES Band(id),
            FOREIGN KEY (artist_id) REFERENCES Artist(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE ArtistAlbum (
            artist_id INTEGER,
            album_id INTEGER,
            FOREIGN KEY (artist_id) REFERENCES Artist(id),
            FOREIGN KEY (album_id) REFERENCES Album(id)
        )
    ''')
    conn.commit()
    conn.close()