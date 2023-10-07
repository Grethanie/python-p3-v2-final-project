class Band:
    def __init__(self, name, albums, genre):
        self.name, self.albums, self.genre = name, albums, genre
    def get_name(self): return self._name
    def get_albums(self): return self._albums
    def get_genre(self): return self._genre