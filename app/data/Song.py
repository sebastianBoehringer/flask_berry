from typing import Optional, Set, Tuple

from app.data.Label import Label
from app.data.LibraryEntry import LibraryEntry
from app.data.db import get_db


class Song(LibraryEntry):
    main_artists: Set[str]
    supporting_artists: Set[str]
    genre: str
    duration: int

    def __init__(self, name: str, location: str, main_artists: Set[str], supporting_artists: Set[str], genre: str,
                 labels: Set[Label], duration: int, entry_id: int = None):
        super().__init__(name, location, labels, entry_id)
        assert len(main_artists) > 0, "Song has no interprets"
        self.main_artists = main_artists
        self.supporting_artists = supporting_artists
        self.genre = genre
        assert duration > 0, "song has invalid duration"
        self.duration = duration

    def __repr__(self) -> str:
        da_id = self.id
        if da_id is None:
            da_id = -1
        return "Song{ id: '%i', name: '%s', location: '%s', main_artists: %s, supporting_artists: %s, genre: '%s'," \
               " labels: %s, duration: '%i'" % \
               (da_id, self.name, self.location, str(self.main_artists), str(self.supporting_artists), self.genre,
                str(self.labels), self.duration)

    def __hash__(self):
        return hash(self._key())

    def _key(self) -> Tuple:
        return *super()._key(), self.main_artists, self.supporting_artists, self.genre, self.duration

    def __eq__(self, other):
        if super().__eq__(other):
            if type(other) is type(self):
                return self.main_artists == other.main_artists and self.supporting_artists == other.supporting_artists and self.genre == other.genre and self.duration == other.duration
        return False

    @staticmethod
    def from_db(entity_id: int) -> Optional["Song"]:
        db = get_db()
        song = db.execute("SELECT * FROM songs where id = ?", (entity_id,)).fetchone()
        if song is None:
            return None
        song_id = song["id"]
        supporters = db.execute("SELECT name from song_supporting_artists where song_id = ?", (song_id,)).fetchall()
        sups = set()
        for row in supporters:
            sups.add(row["name"])
        artists = db.execute("SELECT name from song_artists where song_id = ?", (song_id,)).fetchall()
        main_artists = set()
        for row in artists:
            main_artists.add(row["name"])
        label_ids = db.execute("SELECT label_id from song_labels where song_id = ?", (song_id,)).fetchall()
        labels = set()
        for row in label_ids:
            label = Label.from_db(row["label_id"])
            labels.add(label)
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
            print(f"Can't delete a Song without id, tried to delete {self}")
            return False
        db = get_db()
        db.execute("DELETE FROM songs where id = ?", (self._id,))
        db.commit()
        self.__delete_relations()
        self._id = None
        return True

    def __save_relations(self):
        db = get_db()
        for artist in self.main_artists:
            db.execute("INSERT INTO song_artists (song_id, name) VALUES (?, ?)", (self._id, artist))
            db.commit()
        for artist in self.supporting_artists:
            db.execute("INSERT INTO song_supporting_artists (song_id, name) VALUES (?, ?)", (self._id, artist))
            db.commit()
        for label in self.labels:
            if label.id is None:
                label.save()
            db.execute("INSERT INTO song_labels (song_id, label_id) VALUES (?, ?)", (self._id, label.id))
            db.commit()

    def __delete_relations(self):
        db = get_db()
        db.execute("DELETE FROM song_artists where song_id = ?", (self._id,))
        db.execute("DELETE FROM song_supporting_artists where song_id = ?", (self._id,))
        db.execute("DELETE FROM song_labels where song_id = ?", (self._id,))
        db.commit()

    def as_dict(self) -> dict:
        json_dict = super().as_dict()
        json_dict['main_artists'] = [artist for artist in self.main_artists]
        json_dict['supporting_artists'] = [artist for artist in self.supporting_artists]
        json_dict['genre'] = self.genre
        json_dict['duration'] = self.duration
        return json_dict
