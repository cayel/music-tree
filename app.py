import streamlit as st
import sqlite3
import requests
from lastfm import get_lastfm_album_image


def main():
    st.title("Music Tree App")
    st.write("Welcome to the Music Tree App!")

    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()

    # load albums
    cursor.execute('SELECT id, title, release_date, discogs_id FROM Album')
    album_rows = cursor.fetchall()
    albums = []
    for row in album_rows:
        albums.append(row)
    
    # display albums
    st.write("Albums:")
    cols = st.columns(3)  # Crée trois colonnes

    for i, album in enumerate(albums):
        with cols[i % 3]:  # Répartit les albums entre les colonnes
            image = get_lastfm_album_image("Pink Floyd", "The Dark Side of the Moon")
            st.image(image, caption=album[1], use_column_width=True)
    
    conn.close()

if __name__ == "__main__":
    main()