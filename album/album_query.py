import sqlite3

def load_album_list():
    # Load the list of album from the database
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title FROM Album')
    albums = cursor.fetchall()
    conn.close()
    return albums