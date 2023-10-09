from __init__ import CURSOR, CONN
from band import Band
from album import Album
class Song:
    all = {}
    
    def __init__(self, title, band_id, album_id, id=None):
        self.band_id = band_id
        self.album_id = album_id
        self.title = title
        self.id = id
        
    def __repr__(self):
        return f"<Song: {self.title} Album: {self.album_id} Band: {self.band_id}>"
    
    
        
        
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if title.strip() == "":
            raise ValueError("Title cannot be empty")
        if type(self).find_by_title_and_band_and_album(title, self.band_id, self.album_id):
            raise ValueError("Song by this band with this title already in database")
        self._title = title
        
    @property
    def band_id(self):
        return self._band_id
    @band_id.setter
    def band_id(self, band_id):
        if type(band_id) is not int:
            raise TypeError("Band ID must be an integer")
        if not Band.find_by_id(band_id):
            raise ValueError("Band not found")
        self._band_id = band_id
        
    @property
    def album_id(self):
        return self._album_id
    @album_id.setter
    def album_id(self, album_id):
        if type(album_id) is not int:
            raise TypeError("Album ID must be an integer")
        existing_album = Album.find_by_id(album_id)
        if not existing_album:
            raise ValueError("Album not found")
        if existing_album.band_id != self.band_id:
            raise ValueError("Album and Band mismatch")
        self._album_id = album_id
        
    @classmethod
    def create_table(cls):
        """Create the table for the song model"""
        sql = """CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                band_id INTEGER,
                album_id INTEGER,
                FOREIGN KEY(band_id) REFERENCES bands(id)
                FOREIGN KEY(album_id) REFERENCES albums(id)
            )"""
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        """Drop the table for the song model"""
        sql = """DROP TABLE IF EXISTS songs"""
        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        """Save the song to the database"""
        sql = """INSERT INTO songs (title, band_id, album_id) VALUES (?, ?)"""
        CURSOR.execute(sql, (self.title, self.band_id, self.album_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
        
    @classmethod
    def create(cls, title, band_id, album_id):
        """Create a new song"""
        song = cls(title, band_id, album_id)
        song.save()
        return song
    
    def update(self):
        """Update the song in the database"""
        sql = """UPDATE songs SET title = ?, band_id = ?, album_id = ? WHERE id = ?"""
        CURSOR.execute(sql, (self.title, self.band_id, self.album_id, self.id))
        CONN.commit()
        
    def delete(self):
        """Delete the song from the database"""
        sql = """DELETE FROM songs WHERE id = ?"""
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None
        
    @classmethod
    def find_by_id(cls, id):
        """Find a song by id"""
        sql = """SELECT * FROM songs WHERE id = ?"""
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_title_and_band_and_album(cls, title, band_id, album_id):
        """Find a song by title"""
        sql = """SELECT * FROM songs WHERE title = ? AND band_id = ? AND album_id = ?"""
        CURSOR.execute(sql, (title.lower(), band_id, album_id))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def instance_from_db(cls, row):
        """Return a song instance from a database row"""
        song = cls.all.get(row[0])
        if song:
            song.title = row[1]
            song.band_id = row[2]
            song.album_id = row[3]
        else:
            song = cls(row[1], row[2], row[3])
            song.id = row[0]
            cls.all[song.id] = song
        return song
    
    def album(self):
        """Return the album for this song"""
        return Album.find_by_id(self.album_id)
    
    def band(self):
        """Return the band for this song"""
        return Band.find_by_id(self.band_id)
    
    @classmethod
    def get_all(cls):
        sql = """SELECT * FROM songs"""
        
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]