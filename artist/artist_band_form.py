import streamlit as st
from band.band_query import load_band_list
from artist.artist_query import load_artist_list
from data import insert_artist_band_relation

def display_artist_band_form():
    # Formulaire pour enregistrer un artiste et un groupe
    with st.form(key='artist_band_form'):
        artist_list = load_artist_list()
        # Select box for the artist
        artist = st.selectbox("Artiste", artist_list, format_func=lambda x: f"{x[1]} {x[2]}")

        band_list = load_band_list()
        # Select box for the band
        band = st.selectbox("Groupe", band_list, format_func=lambda x: x[1])        
        submit_button = st.form_submit_button(label='Enregistrer')

        if submit_button:
            if artist and band :
                insert_artist_band_relation(artist[0], band[0])
                st.success("Relation Artiste-Groupe enregistrée avec succès")
            else:
                st.error("Veuillez remplir tous les champs")