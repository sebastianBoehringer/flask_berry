from typing import List

from data.Label import Label
from data.LibraryEntry import LibraryEntry
from data.db import get_db
from error.Errors import MissingValueError


class Song(LibraryEntry):
    main_artists: List[str]
    supporting_artists: List[str]
    genre: str
    labels: List[Label]
    duration: int

    def __init__(self, name: str, location: str, main_artists: List[str], supporting_artists: List[str], genre: str,
                 labels: List[Label], duration: int, entry_id: int = None):
        super().__init__(name, location, entry_id)
        assert len(main_artists) > 0, "Song has no interprets"
        self.main_artists = main_artists
        self.supporting_artists = supporting_artists
        self.genre = genre
        self.labels = labels
        assert duration > 0, "song has invalid duration"
        self.duration = duration

    @staticmethod
    def from_db(song_id: int) -> "Song":
        db = get_db()
        song = db.execute("SELECT * FROM songs where id = ?", song_id).fetchone()
        song_id = song["id"]
        supporters = db.execute("SELECT name from song_supporting_artists where song_id = ?", (song_id,)).fetchall()
        sups = []
        for row in supporters:
            sups.append(row["name"])
        artists = db.execute("SELECT name from song_artists where song_id = ?", (song_id,)).fetchall()
        main_artists = []
        for row in artists:
            main_artists.append(row["name"])
        label_ids = db.execute("SELECT label_id from song_labels where song_id = ?", (song_id,)).fetchall()
        labels = []
        for row in label_ids:
            label = Label.from_db(row["label_id"])
            labels.append(label)
        return Song(entry_id=song_id, name=song["name"], genre=song["genre"], duration=song["duration"],
                    location=song["location"], labels=labels, main_artists=main_artists, supporting_artists=sups)

    def save(self):
        if self.id is not None:
            print("song has id set, calling update instead")
            self.update()
            return
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO songs (name, genre, duration, location) values "
                       "(?, ?, ?, ?)", (self.name, self.genre, self.duration, self.location))
        db.commit()
        self._id = cursor.lastrowid
        self.__save_relations()

    def __save_relations(self):
        db = get_db()
        for artist in self.main_artists:
            db.execute("INSERT INTO song_artists (song_id, name) VALUES (?, ?)", (self._id, artist))
            db.commit()
        for artist in self.supporting_artists:
            db.execute("INSERT INTO song_supporting_artists (song_id, name) VALUES (?, ?)", (self._id, artist))
            db.commit()
        for label in self.labels:
            db.execute("INSERT INTO song_labels (song_id, label_id) VALUES (?, ?)", (self._id, label.id))
            db.commit()

    def __delete_relations(self):
        db = get_db()
        db.execute("DELETE FROM song_artists where song_id = ?", (self._id,))
        db.execute("DELETE FROM song_supporting_artists where song_id = ?", (self._id,))
        db.execute("DELETE FROM song_labels where song_id = ?", (self._id,))
        db.commit()

    def update(self):
        if self.id is None:
            print("song has no id set, calling save instead")
            self.save()
            return
        db = get_db()
        db.execute("UPDATE songs SET name = ?, location = ?, genre = ?, duration = ? where id = ?",
                   (self.name, self.location, self.genre, self.duration, self._id))
        db.commit()
        self.__delete_relations()
        self.__save_relations()

    def delete(self):
        if self.id is None:
            raise MissingValueError("song has no id")
        db = get_db()
        db.execute("DELETE FROM songs where id = ?", (self._id,))
        db.commit()
        self.__delete_relations()
        self._id = None
