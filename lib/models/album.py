class Album:
    all = []
    def __init__(self, name, band):
        self.name, self.band = name, band
        self.band.albums.append(self)
        Album.all.append(self)
    def get_name(self): return self._name
    def get_band(self): return self._band
    def set_name(self, name):
        self._name = name
    def set_band(self, band):
        self._band = band
    name = property(get_name, set_name)
    band = property(get_band, set_band)