from database import create_database
from data import insert_local_file, fetch_data
from diagram import generate_er_diagram
from lastfm import lastfm_get_artist_info
from musicbrainz import musicbrainz_get_albums_by_artist_uid

       
if __name__ == "__main__":
    create_database()
    insert_local_file('./sample_data/data.json')
    fetch_data()
    generate_er_diagram()
    #lastfm_get_artist_info("Nick Cave")
    #musicbrainz_get_albums_by_artist_uid("5a7a3629-e608-4fce-887a-a9028eef1c72") # The Boys Next Door
    