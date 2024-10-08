from database import create_database
from data import insert_sample_data, fetch_data
from diagram import generate_er_diagram
from lastfm import lastfm_get_artist_info
from musicbrainz import musicbrainz_get_albums_by_artist

       
if __name__ == "__main__":
    create_database()
    insert_sample_data()
    fetch_data()
    generate_er_diagram()
    lastfm_get_artist_info("Nick Cave")
    musicbrainz_get_albums_by_artist("Nick Cave And The Bad Seeds")
    