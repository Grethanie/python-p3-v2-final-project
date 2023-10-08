from __init__ import CURSOR, CONN
from band import Band
class Song:
    all = {}
    
    def __init__(self, title, band_id, album_id, id=None):
        self.title, self.band_id, self.album_id, self.id = title, band_id, album_id, id
        
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
        
    @classmethod
    def get_all(cls):
        sql = """SELECT * FROM songs"""
        
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]