import streamlit as st
from data import insert_artist

def display_artist_form():
    # Formulaire pour enregistrer un artiste
    with st.form(key='artist_form'):
        first_name = st.text_input("Prénom de l'artiste")
        last_name = st.text_input("Nom de l'artiste")
        discogs_id = st.text_input("ID Discogs de l'artiste")
        submit_button = st.form_submit_button(label='Enregistrer')

    if submit_button:
        if last_name and discogs_id:
            insert_artist(first_name, last_name, discogs_id)
            st.success("Artiste enregistré avec succès")
        else:
            st.error("Veuillez remplir tous les champs")