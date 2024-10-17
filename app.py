import streamlit as st
from database import db_albums_count, db_bands_count, load_albums_with_band,execute_query
from lastfm import get_lastfm_album_image
from PIL import Image
from artist.artist_form import display_artist_form
from band.band_form import display_band_form
from album.album_form import display_album_form
from artist.artist_band_form import display_artist_band_form
from artist.artist_album_form import display_artist_album_form

def display_album_card(image_url, caption):
    """Display an image card with a given URL and caption."""
    st.markdown(
        f"""
        <div style="border: 2px solid #e6e6e6; border-radius: 10px; padding: 10px; text-align: center; box-shadow: 2px 2px 12px #aaaaaa;">
            <img src="{image_url}" style="width:100%; border-radius: 10px; border: 3px solid black;">
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    # Barre latérale avec un menu
    menu = ["Accueil", "Albums", "Admin"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Accueil":
        st.title("Bienvenue sur la page d'accueil")
        st.write("Contenu de la page d'accueil")
    elif choice == "Albums":
        st.title("Albums")
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

        # Sélecteur de groupe
        band_name = st.selectbox("Sélectionnez un groupe", ["Tous"] + [row[0] for row in execute_query('SELECT name FROM Band')])
        if band_name == "Tous":
            albums = load_albums_with_band()
        else:
            albums = load_albums_with_band(band_name)

        # Slider pour sélectionner le nombre de colonnes
        num_columns = st.slider("Sélectionnez le nombre de colonnes", min_value=1, max_value=5, value=3)

        cols = st.columns(num_columns)  # Create three columns

        for i, album in enumerate(albums):
            with cols[i % num_columns]:  # Distribute albums among columns
                image = get_lastfm_album_image(album[1], album[0])
                display_album_card(image, album[1])
    elif choice == "Admin":
        st.title("Administration")
        st.write("Administration de la base de données")

        with st.expander("Créer un artiste"):
            display_artist_form()

        with st.expander("Créer un groupe"):
            display_band_form()

        with st.expander("Créer un album"):
            display_album_form()

        with st.expander("Créer une relation Artiste-Groupe"):
            display_artist_band_form()

        with st.expander("Créer une relation Artiste-Album"):
            display_artist_album_form()

if __name__ == "__main__":
    main()