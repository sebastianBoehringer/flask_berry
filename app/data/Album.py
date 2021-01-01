from typing import List, NamedTuple

from app.data.Label import Label
from app.data.LibraryEntry import LibraryEntry
from app.data.Song import Song
from app.data.db import get_db

Timestamp = NamedTuple("Timestamp", [('start', int), ('end', int)])


class Album(LibraryEntry):
    songs: List[(Song, Timestamp)]
    artist: str
    labels: List[Label]

    @property
    def duration(self) -> int:
        return self._duration

    def __init__(self, name: str, location: str, songs: List[(Song, Timestamp)], artist: str,
                 labels: List[Label], entry_id: int = None):
        super().__init__(name, location, entry_id)
        assert len(artist) > 0, "artist of album is empty"
        self.artist = artist
        assert len(songs) > 0, "album has no songs"
        self.songs = songs
        total_duration = 0
        for s in songs:
            total_duration += s.duration
        self._duration = total_duration
        self.labels = labels

    def __repr__(self) -> str:
        da_id = self.id
        if self._id is None:
            da_id = -1
        return "Album{ id: '%i', name: '%s', location: '%s', songs: %s, artist: '%s', labels: %s}" % \
               (da_id, self.name, self.location, str(self.songs), self.artist, str(self.labels))

    def save(self):
        if self.id is not None:
            self.update()
            return
        db = get_db()
        cursor = db.cursor()
        db.commit()
        db.execute("INSERT INTO albums (name, location, artist) "
                   "VALUES (?, ?, ?)",
                   (self.name, self.location, self.artist))
        self._id = cursor.lastrowid
        self.__save_relations()

    def __save_relations(self):
        """
        safes the labels and timestamps
        """
        db = get_db()
        for label in self.labels:
            if label.id is None:
                label.save()
            db.execute("INSERT INTO album_labels (album_id, label_id)"
                       " VALUES (?, ?)", (self.id, label.id))
            db.commit()

        for (song, timestamp) in self.songs:
            if song.id is None:
                song.save()
            song.save()
            db.execute("INSERT INTO album_songs (album_id, song_id) "
                       "VALUES (?,?)", self._id, song.id)
            db.execute("INSERT INTO timestamps (album_id, song_id, start, end)"
                       " VALUES (?, ?, ?, ?)",
                       (self.id, song.id, timestamp.start, timestamp.end))
            db.commit()

    def __delete_relations(self):
        db = get_db()
        db.execute("DELETE from album_songs where album_id = ?", (self._id,))
        db.execute("DELETE from album_labels where album_id = ?", (self._id,))
        db.execute("DELETE from timestamps where album_id= ?", (self._id,))
        song_ids = db.execute("SELECT song_id from album_songs where album_id = ?", (self._id,)).fetchall()
        for row in song_ids:
            song = Song.from_db(row["song_id"])
            song.delete()
        db.commit()

    def update(self):
        if self._id is None:
            self.save()
            return
        db = get_db()
        db.execute("UPDATE albums "
                   "SET albums.name = ?, albums.location = ?, albums.artist = ?"
                   " where albums.id = ?",
                   (self.name, self.location, self.artist, self._id))
        db.commit()

        self.__delete_relations()
        self.__save_relations()

    def delete(self):
        if self.id is None:
            print(f"Can't delete an album without id, tried to delete {self}")
            return False
        db = get_db()
        db.execute("DELETE from albums where id = ?", (self.id,))
        songs = db.execute("SELECT song_id from album_songs where album_id = ?", (self._id,)).fetchall()
        for row in songs:
            song = Song.from_db(row["song_id"])
            song.delete()
        self.__delete_relations()
        db.commit()
        self._id = None
        return True

    @staticmethod
    def from_db(entity_id: int) -> "Album":
        db = get_db()
        album = db.execute("SELECT * from albums where id = ?", (entity_id,)).fetchone()
        album_id = album["id"]
        song_ids = db.execute("SELECT song_id from album_songs where album_id = ?", (album_id,)).fetchall()
        songs = []
        for row in song_ids:
            song = Song.from_db(row["song_id"])
            timestamp = db.execute("SELECT start, end from timestamps where album_id= ? AND song_id = ?",
                                   (album_id, song.id)).fetchone()
            songs.append((song, Timestamp(start=timestamp["start"], end=timestamp["end"])))
        label_ids = db.execute("SELECT label_id from album_labels where album_id = ?", (album_id,)).fetchall()
        labels = []
        for row in label_ids:
            label = Label.from_db(row["label_id"])
            labels.append(label)
        return Album(entry_id=album_id, location=album["location"], name=album["name"], artist=album["artist"],
                     songs=songs, labels=labels)
