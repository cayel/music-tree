import matplotlib.pyplot as plt
import networkx as nx
import sqlite3
from models import Artist, Band, Album

def generate_er_diagram(artist_id: int = None):
    """
    Generate and display an ER diagram using networkx and matplotlib.

    Parameters:
    artist_id (int, optional): The ID of the artist for whom to generate the ER diagram.
                               If None, the diagram will include all artists, bands, and albums.

    This function creates a directed graph (DiGraph) representing the relationships between
    artists, bands, and albums. If an artist ID is provided, the graph will include only the
    specified artist and their related bands and albums. If no artist ID is provided, the graph
    will include all artists, bands, and albums in the database.

    The graph is displayed using matplotlib.
    """
    G = nx.DiGraph()

    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()

    if artist_id is None:
        # Add all artists
        cursor.execute('SELECT id, first_name, last_name FROM Artist')
        artist_rows = cursor.fetchall()
        for row in artist_rows:
            artist = Artist(row[0], row[1], row[2])
            G.add_node(artist, id=artist.id, label=f'{artist.first_name} {artist.last_name}')
        
        # Add all bands
        cursor.execute('SELECT id, name FROM Band')
        band_rows = cursor.fetchall()
        for row in band_rows:
            band = Band(row[0], row[1])
            G.add_node(band, id=band.id, label=band.name)
        
        # Add all albums
        cursor.execute('SELECT id, title, release_date FROM Album')
        album_rows = cursor.fetchall()
        for row in album_rows:
            album = Album(row[0], row[1], row[2])
            G.add_node(album, id=album.id, label=f'{album.title}\n{album.release_date}')
        
        # Add all edges between artists and bands
        cursor.execute('SELECT band_id, artist_id FROM BandArtist')
        band_artist_rows = cursor.fetchall()
        for row in band_artist_rows:
            band = [n for n in G.nodes if isinstance(n, Band) and n.id == row[0]][0]
            artist = [n for n in G.nodes if isinstance(n, Artist) and n.id == row[1]][0]
            G.add_edge(artist, band, label='member')
        
        # Add all edges between bands and albums
        cursor.execute('SELECT band_id, id FROM Album')
        band_album_rows = cursor.fetchall()
        for row in band_album_rows:
            band = [n for n in G.nodes if isinstance(n, Band) and n.id == row[0]][0]
            album = [n for n in G.nodes if isinstance(n, Album) and n.id == row[1]][0]
            G.add_edge(band, album, label='recorded')
        
        # Add all edges between artists and albums
        cursor.execute('SELECT artist_id, album_id FROM ArtistAlbum')
        artist_album_rows = cursor.fetchall()
        for row in artist_album_rows:
            artist = [n for n in G.nodes if isinstance(n, Artist) and n.id == row[0]][0]
            album = [n for n in G.nodes if isinstance(n, Album) and n.id == row[1]][0]
            G.add_edge(artist, album, label='played')
    else:
        # Add nodes for the specified artist
        cursor.execute('SELECT id, first_name, last_name FROM Artist WHERE id = ?', (artist_id,))
        artist_row = cursor.fetchone()
        if artist_row:
            artist = Artist(artist_row[0], artist_row[1], artist_row[2])
            G.add_node(artist, id=artist.id, label=f'{artist.first_name} {artist.last_name}')
            
            # Add bands the artist is a member of
            cursor.execute('''
                SELECT b.id, b.name 
                FROM Band b
                JOIN BandArtist ba ON b.id = ba.band_id
                WHERE ba.artist_id = ?
            ''', (artist_id,))
            band_rows = cursor.fetchall()
            for row in band_rows:
                band = Band(row[0], row[1])
                G.add_node(band, id=band.id, label=band.name)
                G.add_edge(artist, band, label='member')
            
            # Add albums the artist has played on
            cursor.execute('''
                SELECT al.id, al.title, al.release_date 
                FROM Album al
                JOIN ArtistAlbum aa ON al.id = aa.album_id
                WHERE aa.artist_id = ?
            ''', (artist_id,))
            album_rows = cursor.fetchall()
            for row in album_rows:
                album = Album(row[0], row[1], row[2])
                G.add_node(album, id=album.id, label=f'{album.title}\n{album.release_date}')
                G.add_edge(artist, album, label='played')
            
            # Add albums recorded by bands the artist is a member of
            cursor.execute('''
                SELECT al.id, al.title, al.release_date, b.id 
                FROM Album al
                JOIN Band b ON al.band_id = b.id
                JOIN BandArtist ba ON b.id = ba.band_id
                WHERE ba.artist_id = ?
            ''', (artist_id,))
            band_album_rows = cursor.fetchall()
            for row in band_album_rows:
                album = Album(row[0], row[1], row[2])
                band = [n for n in G.nodes if isinstance(n, Band) and n.id == row[3]][0]
                G.add_node(album, id=album.id, label=f'{album.title}\n{album.release_date}')
                G.add_edge(band, album, label='recorded')
        
    conn.close()

    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')

    node_colors = []
    for node in G.nodes(data=True):
        if isinstance(node[0], Artist):
            node_colors.append('lightblue')
        elif isinstance(node[0], Band):
            node_colors.append('lightgreen')
        elif isinstance(node[0], Album):
            node_colors.append('lightcoral')
        else:
            node_colors.append('gray')

    edge_colors = []
    for edge in G.edges(data=True):
        if edge[2].get('label') == 'recorded':
            edge_colors.append('blue')
        elif edge[2].get('label') == 'member':
            edge_colors.append('green')
        elif edge[2].get('label') == 'played':
            edge_colors.append('pink')
        else:
            edge_colors.append('black')

    nx.draw(G, pos, with_labels=True, labels=labels, node_size=1000, node_color=node_colors, font_size=10, font_weight='bold', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrows=True)

    title = f'ER Diagram for Artist ID {artist_id}' if artist_id else 'ER Diagram for All Artists'
    plt.title(title)
    plt.show()