from album import Album
from song import Song
class Band:
    all = []
    
    def __init__(self, name, genre):
        self.name, self.genre = name, genre
        self.albums = [album for album in Album.all if album.band == self]
        self.songs = [song for song in Song.all if song.band == self]
        
    def get_name(self): return self._name
    def get_albums(self): return self._albums
    def get_genre(self): return self._genre
    
    def set_name(self, name):
        self._name = name
    def set_albums(self, albums):
        self._albums = albums
    def set_genre(self, genre):
        self._genre = genre
        
    name = property(get_name, set_name)
    albums = property(get_albums, set_albums)
    genre = property(get_genre, set_genre)