import streamlit as st
from album.album_query import load_album_list
from artist.artist_query import load_artist_list
from data import insert_artist_album_relation

def display_artist_album_form():
    # Formulaire pour enregistrer un artiste et un groupe
    with st.form(key='artist_album_form'):
        artist_list = load_artist_list()
        # Select box for the artist
        artist = st.selectbox("Artiste", artist_list, format_func=lambda x: f"{x[1]} {x[2]}")

        album_list = load_album_list()
        # Select box for the album
        album = st.selectbox("Album", album_list, format_func=lambda x: x[1])        
        submit_button = st.form_submit_button(label='Enregistrer')

        if submit_button:
            if artist and album :
                insert_artist_album_relation(artist[0], album[0])
                st.success("Relation Artiste-Album enregistrée avec succès")
            else:
                st.error("Veuillez remplir tous les champs")