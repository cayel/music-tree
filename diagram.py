import matplotlib.pyplot as plt
import networkx as nx
import sqlite3
from models import Artist, Band, Album

def generate_er_diagram():
    """Generate and display an ER diagram using networkx and matplotlib."""
    G = nx.DiGraph()

    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()

    # Add nodes artists from database
    cursor.execute('SELECT id, first_name, last_name FROM Artist')
    rows = cursor.fetchall()
    for row in rows:
        artist = Artist(row[0], row[1], row[2])
        G.add_node(artist, id=artist.id, label=f'{artist.first_name} {artist.last_name}')
        
    # Add nodes bands from database
    cursor.execute('SELECT id, name FROM Band')
    rows = cursor.fetchall()
    for row in rows:
        band = Band(row[0], row[1])
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
        
    cursor.execute('SELECT artist_id, album_id FROM ArtistAlbum')
    rows = cursor.fetchall()
    for row in rows:
        artist = [n for n in G.nodes if isinstance(n, Artist) and n.id == row[0]][0]
        album = [n for n in G.nodes if isinstance(n, Album) and n.id == row[1]][0]
        G.add_edge(artist, album, label='played')   
       
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

    plt.title('ER Diagram')
    plt.show()