import streamlit as st
from database import db_albums_count, db_bands_count, load_albums_with_band
from lastfm import get_lastfm_album_image
from PIL import Image

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

    # Compter les albums et les groupes
    albums_count = db_albums_count()
    bands_count = db_bands_count()

    # Afficher le texte formaté
    st.markdown(f"""
        <div style="text-align: left; font-size: 24px; color: black;">
            <p>Il y a <strong>{albums_count}</strong> albums dans la base de données.</p>
            <p>Il y a <strong>{bands_count}</strong> groupes dans la base de données.</p>
        </div>
    """, unsafe_allow_html=True)

    albums = load_albums_with_band()
    cols = st.columns(3)  # Create three columns

    for i, album in enumerate(albums):
        with cols[i % 3]:  # Distribute albums among columns
            image = get_lastfm_album_image(album[1], album[0])
            display_album_card(image, album[1])

if __name__ == "__main__":
    main()