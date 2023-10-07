class Song:
    def __init__(self, title, album, band):
        self.title, self.album, self.band = title, album, band
        
    def get_title(self): return self._title
    def get_album(self): return self._album
    def get_band(self): return self._band
    
    def set_title(self, title):
        self._title = title
    def set_album(self, album):
        self._album = album
    def set_band(self, band):
        self._band = band
    
    title = property(get_title, set_title)
    album = property(get_album, set_album)
    band = property(get_band, set_band)