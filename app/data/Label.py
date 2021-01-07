from typing import Optional, Tuple

from app.data.DbEntity import DbEntity
from app.data.db import get_db


class Label(DbEntity):
    name: str

    def __init__(self, name: str, label_id: int = None):
        super().__init__(entity_id=label_id)
        assert len(name) > 0, "Label has no name"
        self.name = name

    def __repr__(self) -> str:
        da_id = -1
        if self.id is not None:
            da_id = self.id

        return "Label{ id: '%i', name: '%s'}" % (da_id, self.name)

    def __hash__(self):
        return hash(self._key())

    def _key(self) -> Tuple:
        return *super()._key(), self.name

    def __eq__(self, other: object) -> bool:
        if super().__eq__(other):
            if type(other) is type(self):
                return self.name == other.name
        return False

    def save(self):
        if self.id is not None:
            print("label has id set, calling update instead")
            self.update()
            return
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO labels (name) values (?)", (self.name,))
        db.commit()
        self._id = cursor.lastrowid

    def update(self):
        if self.id is None:
            print("label has no id set, calling save instead")
            self.save()
            return
        db = get_db()
        db.execute("UPDATE labels SET name = ? where labels.id = ?", (self.name, self._id))
        db.commit()

    def delete(self):
        if self.id is None:
            print(f"Can't delete a label without id, tried to delete {self}")
            return False
        if not self.is_in_use():
            db = get_db()
            db.execute("DELETE from labels where labels.id = ?", (self._id,))
            db.commit()
            self._id = None
            return True
        else:
            print(f"Label {self} is still in use")
            return False

    def is_in_use(self) -> bool:
        db = get_db()
        song_count = db.execute("SELECT COUNT(*) as count FROM song_labels where label_id = ?", (self.id,)).fetchone()
        if song_count["count"] > 0:
            return True
        book_count = db.execute("SELECT COUNT(*) as count FROM book_labels where label_id = ?", (self.id,)).fetchone()
        if book_count["count"] > 0:
            return True
        album_count = db.execute("SELECT COUNT(*) as count FROM album_labels where label_id = ?", (self.id,)).fetchone()
        if album_count["count"] > 0:
            return True
        return False

    @staticmethod
    def from_db(entity_id: int) -> Optional["Label"]:
        db = get_db()
        label = db.execute("SELECT * from labels where labels.id = ?", (entity_id,)).fetchone()
        if label is None:
            return None
        return Label(name=label["name"], label_id=label["id"])
