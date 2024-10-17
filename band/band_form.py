import streamlit as st
from data import insert_band

def display_band_form():
    # Formulaire pour enregistrer un groupe
    with st.form(key='band_form'):
        name = st.text_input("Nom du groupe")
        discogs_id = st.text_input("ID Discogs du groupe")
        submit_button = st.form_submit_button(label='Enregistrer')

    if submit_button:
        if name and discogs_id:
            ret = insert_band(name, discogs_id)
            print(ret)
            if ret: 
                st.success("Groupe enregistré avec succès")
            else:
                st.error("Erreur lors de l'enregistrement du groupe")
        else:
            st.error("Veuillez remplir tous les champs")