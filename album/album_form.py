import streamlit as st
from data import insert_album
from band.band_query import load_band_list

def display_album_form():
    # Formulaire pour enregistrer un album
    with st.form(key='album_form'):
        title = st.text_input("Titre de l'album")
        band_list = load_band_list()
        # Select box for the band
        band = st.selectbox("Groupe", band_list, format_func=lambda x: x[1])
        release_date = st.date_input("Date de sortie")  
        discogs_id = st.text_input("ID Discogs de l'album")
        submit_button = st.form_submit_button(label='Enregistrer')

    if submit_button:
        if title and discogs_id and band:
            insert_album(title, release_date, discogs_id, band[0])
            st.success("Album enregistré avec succès")
        else:
            st.error("Veuillez remplir tous les champs")