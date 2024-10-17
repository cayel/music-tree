import sqlite3

def load_artist_list():
    # Load the list of artist from the database
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name FROM Artist')
    bands = cursor.fetchall()
    conn.close()
    return bands