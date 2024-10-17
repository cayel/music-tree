import sqlite3

def load_band_list():
    # Load the list of bands from the database
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM Band')
    bands = cursor.fetchall()
    conn.close()
    return bands