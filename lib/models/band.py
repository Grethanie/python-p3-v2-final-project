from __init__ import CURSOR, CONN
from album import Album
from song import Song
class Band:
    all = {}
    
    def __init__(self, name, genre, id=None):
        self.name, self.genre, self.id = name, genre, id
        
    def create_table(cls):
        """Create the table for the Band model"""
        sql = """CREATE TABLE IF NOT EXISTS bands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                genre TEXT
            )"""
        CURSOR.execute(sql)
        CONN.commit()
        
    def drop_table(cls):
        """Drop the table for the Band model"""
        sql = """DROP TABLE IF EXISTS bands"""
        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        """Save the band to the database"""
        sql = """INSERT INTO bands (name, genre) VALUES (?, ?)"""
        CURSOR.execute(sql, (self.name, self.genre))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
        
    def create(cls, name, genre):
        """Create a new band"""
        band = cls(name, genre)
        band.save()
        return band
    
    def update(self):
        """Update the band in the database"""
        sql = """UPDATE bands SET name = ?, genre = ? WHERE id = ?"""
        CURSOR.execute(sql, (self.name, self.genre, self.id))
        CONN.commit()
        
    def delete(self):
        """Delete the band from the database"""
        sql = """DELETE FROM bands WHERE id = ?"""
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None
        
    def find_by_id(cls, id):
        """Find a band by id"""
        sql = """SELECT * FROM bands WHERE id = ?"""
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
    
    def instance_from_db(cls, row):
        """Return a band instance from a database row"""
        band = cls.all.get(row[0])
        if band:
            band.name = row[1]
            band.genre = row[2]
        else:
            band = cls(row[1], row[2])
            band.id = row[0]
            cls.all[band.id] = band
        
    def get_all(cls):
        sql = """SELECT * FROM bands"""
        
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]