from __init__ import CURSOR, CONN
from band import Band
class Album:
    all = {}
    
    def __init__(self, title, band_id, id=None):
        self.title, self.band_id, self.id = title, band_id, id
        
        
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if title.strip() == "":
            raise ValueError("Title cannot be empty")
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
        
    @classmethod
    def create_table(cls):
        """Create the table for the album model"""
        sql = """CREATE TABLE IF NOT EXISTS albums (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                band_id INTEGER,
                FOREIGN KEY(band_id) REFERENCES bands(id)
            )"""
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        """Drop the table for the album model"""
        sql = """DROP TABLE IF EXISTS albums"""
        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        """Save the album to the database"""
        sql = """INSERT INTO albums (title, band_id) VALUES (?, ?)"""
        CURSOR.execute(sql, (self.title, self.band_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
     
    @classmethod   
    def create(cls, title, band_id):
        """Create a new album"""
        album = cls(title, band_id)
        album.save()
        return album
    
    def update(self):
        """Update the album in the database"""
        sql = """UPDATE albums SET title = ?, band_id = ? WHERE id = ?"""
        CURSOR.execute(sql, (self.title, self.band_id, self.id))
        CONN.commit()
        
    def delete(self):
        """Delete the album from the database"""
        sql = """DELETE FROM albums WHERE id = ?"""
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None
        
    @classmethod
    def find_by_id(cls, id):
        """Find a album by id"""
        sql = """SELECT * FROM albums WHERE id = ?"""
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def instance_from_db(cls, row):
        """Return a album instance from a database row"""
        album = cls.all.get(row[0])
        if album:
            album.title = row[1]
            album.band_id = row[2]
        else:
            album = cls(row[1], row[2])
            album.id = row[0]
            cls.all[album.id] = album
        return album
        
    @classmethod
    def get_all(cls):
        sql = """SELECT * FROM albums"""
        
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    def songs(self):
        from song import Song
        sql = """SELECT * FROM songs WHERE album_id = ?"""
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Song.instance_from_db(row) for row in rows]