import psycopg2

def dbconnect(func):
    def inner_wrapper(*args, **kwargs):
        conn = psycopg2.connect("dbname='musicbot' user='postgres' host='localhost' password='postgres'")
        cur = conn.cursor()
        result = func(cur, *args, **kwargs)
        cur.close()
        conn.commit()
        conn.close()
        return result
    return inner_wrapper

class DatabaseManager():
    
    
    @dbconnect
    def create_playlist(cur, name):
        cur.execute("""INSERT INTO playlists (name) VALUES (%s)""", (name, ))
        return cur.rowcount > 0

    @dbconnect
    def delete_playlist(cur, name):
        cur.execute("""DELETE FROM playlists WHERE name=%s""", (name, ))
        return cur.rowcount > 0

    @dbconnect
    def list_playlists(cur):
        cur.execute("""SELECT playlists.name, (SELECT COUNT(*) FROM songs WHERE playlist = playlists.name) AS songcount FROM playlists""")
        result = []
        for tup in cur:
            result.append(tup)
        return result

    @dbconnect
    def get_playlist(cur, playlist_name):
        cur.execute("""SELECT song_url, song_name FROM songs WHERE playlist = %s""", (playlist_name, ))
        result = []
        for tup in cur:
            result.append(tup)
        return result

    @dbconnect
    def get_songcount(cur, playlist_name):
        cur.execute("""SELECT COUNT(*) FROM songs WHERE playlist = %s""", (playlist_name, ))
        return cur.fetchone()[0]

    @dbconnect
    def add_song(cur, playlist_name, song_url, song_name):
        cur.execute("""INSERT INTO songs (playlist, song_url, song_name) VALUES (%s, %s, %s)""",
                    (playlist_name, song_url, song_name))
        return cur.rowcount > 0

    @dbconnect
    def delete_song(cur, playlist_name, song_url_or_name):
        cur.execute("""DELETE FROM songs WHERE playlist=%s AND (song_url=%s OR song_name=%s)""",
                    (playlist_name, song_url_or_name, song_url_or_name))
        return cur.rowcount > 0

if __name__ == "__main__":
    print(DatabaseManager.get_playlist("Test"))
    DatabaseManager.add_song("Test", "New_url", "New_name")
    print(DatabaseManager.get_playlist("Test"))
    DatabaseManager.delete_song("Test", "New_url")
    print(DatabaseManager.get_playlist("Test"))
    print(DatabaseManager.list_playlists())
    DatabaseManager.create_playlist("New_playlist") 
    print(DatabaseManager.list_playlists())
    DatabaseManager.delete_playlist("New_playlist")
    print(DatabaseManager.list_playlists())
