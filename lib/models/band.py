from __init__ import CURSOR, CONN
class Band:
    all = {}
    
    def __init__(self, name, genre, id=None):
        self.name, self.genre, self.id = name, genre, id
        
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if name.strip() == "":
            raise ValueError("name cannot be empty")
        
        self._name = name
        
    @property
    def genre(self):
        return self._genre
    @genre.setter
    def genre(self, genre):
        if not isinstance(genre, str):
            raise TypeError("genre must be a string")
        if genre.strip() == "":
            raise ValueError("genre cannot be empty")
        self._genre = genre
        
    @classmethod
    def create_table(cls):
        """Create the table for the Band model"""
        sql = """CREATE TABLE IF NOT EXISTS bands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                genre TEXT
            )"""
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
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
        
    @classmethod
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
        
    @classmethod
    def find_by_id(cls, id):
        """Find a band by id"""
        sql = """SELECT * FROM bands WHERE id = ?"""
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        """Find a band by name"""
        sql = """SELECT * FROM bands WHERE name = ?"""
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
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
        return band
        
    @classmethod
    def get_all(cls):
        sql = """SELECT * FROM bands"""
        
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    def albums(self):
        from album import Album
        sql = """SELECT * FROM albums WHERE band_id = ?"""
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Album.instance_from_db(row) for row in rows]
    
    def songs(self):
        from song import Song
        sql = """SELECT * FROM songs WHERE band_id = ?"""
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Song.instance_from_db(row) for row in rows]