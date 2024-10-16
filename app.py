import streamlit as st
import sqlite3
from lastfm import get_lastfm_album_image
from PIL import Image

def load_albums_with_band():
    """Load albums with their respective band names from the database."""
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT a.title, b.name FROM Album a JOIN Band b ON a.band_id = b.id''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def display_album_card(image_url, caption):
    """Display an image card with a given URL and caption."""
    st.markdown(
        f"""
        <div style="border: 2px solid #e6e6e6; border-radius: 10px; padding: 10px; text-align: center; box-shadow: 2px 2px 12px #aaaaaa;">
            <img src="{image_url}" style="width:100%; border-radius: 10px; border: 3px solid black;">
            <p style="font-size: 1.2em; color: #333333;">{caption}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    """Main function to set up the Streamlit app and display albums."""
    st.title("Music Tree App")
    st.write("Welcome to the Music Tree App!")

    albums = load_albums_with_band()
    cols = st.columns(3)  # Create three columns

    for i, album in enumerate(albums):
        with cols[i % 3]:  # Distribute albums among columns
            image = get_lastfm_album_image(album[1], album[0])
            display_album_card(image, album[1])

if __name__ == "__main__":
    main()