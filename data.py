import sqlite3

def insert_sample_data():
    """Insert sample data into the database."""
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()

    # Insert sample data
    cursor.execute('''
        INSERT INTO Artist (first_name, last_name) VALUES
        ('Nick', 'Cave'),
        ('Blixa', 'Bargeld'),
        ('Alexander', 'Hacke'),
        ('Mick', 'Harvey')
    ''')
    cursor.execute('''
        INSERT INTO Band (name) VALUES
        ('Nick Cave & The Bad Seeds'),
        ('Einstürzende Neubauten'),
        ('The Birthday Party'),
        ('Grinderman'),
        ('The Boys Next Door')
    ''')
    cursor.execute('''
        INSERT INTO Album (title, release_date, band_id) VALUES
        ('Tender Prey', '2023-10-01', 1),
        ('Kollaps', '1989-07-01', 2),
        ('Prayers on Fire', '1981-04-01', 3),
        ('Grinderman', '2007-03-05', 4),
        ('Door, Door', '1979-01-01', 5)
    ''')
    cursor.execute('''
        INSERT INTO BandArtist (band_id, artist_id) VALUES
        (1, 1),
        (1, 2),
        (2, 2),
        (3, 1),
        (2, 3),
        (4, 1),
        (5, 1),
        (5, 4)
    ''')
    cursor.execute('''
        INSERT INTO ArtistAlbum (artist_id, album_id) VALUES
        (1, 1),
        (1, 4),
        (1, 5),
        (2, 2),
        (3, 3),
        (4, 4)
    ''')
    
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