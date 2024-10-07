import matplotlib.pyplot as plt
import networkx as nx
from datetime import date
from typing import List
import sqlite3
from graphviz import Digraph

def create_database():
    # Connect to SQLite database
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
            last_name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Band (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Album (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            release_date DATE NOT NULL,
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
    # Commit and close connection
    conn.commit()
    conn.close()
        
def insert_sample_data():
    # Connect to SQLite database
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
    
    # Commit and close connection
    conn.commit()
    conn.close()
    
def fetch_data():
    # Connect to SQLite database
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()

    # Fetch data
    cursor.execute('''
        SELECT a.first_name, a.last_name, b.name, al.title, al.release_date
        FROM Artist a
        JOIN BandArtist ba ON a.id = ba.artist_id
        JOIN Band b ON ba.band_id = b.id
        JOIN Album al ON b.id = al.band_id
    ''')
    rows = cursor.fetchall()

    # Display data
    for row in rows:
        print(row)

    # Close connection
    conn.close()
      
def generate_er_diagram():
    class Artist:
        def __init__(self, id: int, first_name: str, last_name: str):
            self.id = id
            self.first_name = first_name
            self.last_name = last_name
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
        def __init__(self, id: int, name: str):
            self.id = id
            self.name = name
            self.records: List['Album'] = []
            self.members: List[Artist] = []

        def add_album(self, album: 'Album'):
            if album not in self.records:
                self.records.append(album)

    class Album:
        def __init__(self, id: int, title: str, release_date: date):
            self.id = id
            self.title = title
            self.release_date = release_date
            
    class ArtistAlbum:
        def __init__(self, artist: Artist, album: Album):
            self.artist = artist
            self.album = album

    # Generate ER Diagram using networkx and matplotlib
    G = nx.DiGraph()

    # Add nodes artists from database
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name FROM Artist')
    rows = cursor.fetchall()
    for row in rows:
        artist = Artist(row[0], row[1], row[2])
        G.add_node(artist, id=artist.id, label=f'{artist.first_name} {artist.last_name}')
        
    # Add nodes bands from database
    cursor.execute('SELECT id, name FROM Band')
    rows = cursor.fetchall()
    for row in rows:
        band = Band(row[0],row[1])
        G.add_node(band, id=band.id, label=band.name)
        
    # Add nodes albums from database
    cursor.execute('SELECT id, title, release_date FROM Album')
    rows = cursor.fetchall()
    for row in rows:
        album = Album(row[0], row[1], row[2])
        G.add_node(album, id=album.id, label=f'{album.title}\n{album.release_date}')
        
    # Add edges from database
    cursor.execute('SELECT band_id, artist_id FROM BandArtist')
    rows = cursor.fetchall()
    for row in rows:
        band = [n for n in G.nodes if isinstance(n, Band) and n.id == row[0]][0]
        artist = [n for n in G.nodes if isinstance(n, Artist) and n.id == row[1]][0]
        G.add_edge(artist, band, label='member')
        
    cursor.execute('SELECT band_id, id FROM Album')
    rows = cursor.fetchall()
    for row in rows:
        band = [n for n in G.nodes if isinstance(n, Band) and n.id == row[0]][0]
        album = [n for n in G.nodes if isinstance(n, Album) and n.id == row[1]][0]
        G.add_edge(band, album, label='recorded')
        
    # Add edges for artist-album relationships
    cursor.execute('SELECT artist_id, album_id FROM ArtistAlbum')
    rows = cursor.fetchall()
    for row in rows:
        artist = [n for n in G.nodes if isinstance(n, Artist) and n.id == row[0]][0]
        album = [n for n in G.nodes if isinstance(n, Album) and n.id == row[1]][0]
        G.add_edge(artist, album, label='played')   
       
    # Close connection
    conn.close

    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')

    # Define colors for each type of node
    node_colors = []
    for node in G.nodes(data=True):
        if isinstance(node[0], Artist):
            node_colors.append('lightblue')
        elif isinstance(node[0], Band):
            node_colors.append('lightgreen')
        elif isinstance(node[0], Album):
            node_colors.append('lightcoral')
        else:
            node_colors.append('gray')  # Default color for unknown types

    # Define colors for each type of edge
    edge_colors = []
    for edge in G.edges(data=True):
        if edge[2].get('label') == 'recorded':
            edge_colors.append('blue')
        elif edge[2].get('label') == 'is member of':
            edge_colors.append('green')
        elif edge[2].get('label') == 'played':
            edge_colors.append('pink')
        else:
            edge_colors.append('black')  # Default color for unknown types

    # Draw the graph with node colors
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=1000, node_color=node_colors, font_size=10, font_weight='bold', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrows=True)

    plt.title('ER Diagram')
    plt.show()

# Main program
create_database()
insert_sample_data()
fetch_data()
generate_er_diagram()
