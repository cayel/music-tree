import streamlit as st
from database import (
    db_albums_count, db_bands_count, load_albums_with_band, execute_query, 
    create_database, database_exists
)
from lastfm import get_lastfm_album_image
from PIL import Image
from artist.artist_form import display_artist_form
from band.band_form import display_band_form
from album.album_form import display_album_form
from artist.artist_band_form import display_artist_band_form
from artist.artist_album_form import display_artist_album_form
from data import insert_local_file, export_data
import logging
from diagram import generate_er_diagram
from pyvis.network import Network
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState

def diagram_flow():
    nodes = [StreamlitFlowNode(id='1', pos=(100, 100), data={'content': 'Node 1'}, node_type='input', source_position='right'),
            StreamlitFlowNode('2', (350, 50), {'content': 'Node 2'}, 'default', 'right', 'left'),
            StreamlitFlowNode('3', (350, 150), {'content': 'Node 3'}, 'default', 'right', 'left'),
            StreamlitFlowNode('4', (600, 100), {'content': 'Node 4'}, 'output', target_position='left')]

    edges = [StreamlitFlowEdge('1-2', '1', '2', animated=True),
            StreamlitFlowEdge('1-3', '1', '3', animated=True),
            StreamlitFlowEdge('2-4', '2', '4', animated=True),
            StreamlitFlowEdge('3-4', '3', '4', animated=True)]

    state = StreamlitFlowState(nodes, edges)

    streamlit_flow('minimap_controls_flow',
                    state,
                    fit_view=True,
                    show_minimap=True,
                    show_controls=True,
                    hide_watermark=True)

def test_network():
    g = Network()
    g.add_nodes([1,2,3], value=[10, 100, 400],
                            title=['I am node 1', 'node 2 here', 'and im node 3'],
                            x=[21.4, 54.2, 11.2],
                            y=[100.2, 23.54, 32.1],
                            label=['NODE 1', 'NODE 2', 'NODE 3'],
                            color=['#00ff1e', '#162347', '#dd4b39'])
    return g

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
    # Configurer le logger avec le niveau de journalisation à DEBUG
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # Barre latérale avec un menu
    menu = ["Accueil", "Albums", "Réseau", "Admin"]
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
    elif choice == "Réseau":
        st.title("Réseau")
        st.write("Visualisation du réseau")

        diagram_flow()


    elif choice == "Admin":
        st.title("Administration")
        st.write("Administration de la base de données")

        if database_exists():
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
            with st.expander("Exporter les données dans un fichier json"):
                if st.button("Exporter les données"):
                    json_file = export_data()
                    st.download_button(
                        label="Télécharger le fichier json",
                        data=json_file,
                        file_name="data.json",
                        mime="text/json",
                    )

        else:
            with st.expander("Initialiser la base de données"):
                if st.button("Initialiser la base de données"):
                    logging.info("Création de la base de données")
                    create_database()
                    logging.info("Base de données créée avec succès")
                    logging.info("Insertion des données du fichier json")
                    insert_local_file('./sample_data/data.json')
                    logging.info("Données insérées avec succès")
                    st.success("Données insérées avec succès")

if __name__ == "__main__":
    main()