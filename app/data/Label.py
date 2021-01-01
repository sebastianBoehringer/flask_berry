from app.data.DbEntity import DbEntity
from app.data.db import get_db


class Label(DbEntity):
    name: str

    def __init__(self, name: str, label_id: int = None):
        super().__init__(entity_id=label_id)
        assert len(name) > 0, "Label has no name"
        self.name = name

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
        db = get_db()
        if not self.is_in_use():
            db.execute("DELETE from labels where labels.id = ?", (self._id,))
            db.commit()
            self._id = None
            return True
        else:
            print(f"Label {self} is still in use")
            return False

    def is_in_use(self) -> bool:
        db = get_db()
        song_count = db.execute("SELECT COUNT(*) as count FROM song_labels where label_id = ?", (self.id,))
        if song_count["count"] > 0:
            return True
        book_count = db.execute("SELECT COUNT(*) as count FROM book_labels where label_id = ?", (self.id,))
        if book_count["count"] > 0:
            return True
        album_count = db.execute("SELECT COUNT(*) as count FROM album_labels where label_id = ?", (self.id,))
        if album_count["count"] > 0:
            return True
        return False

    def __repr__(self) -> str:
        da_id = -1
        if self.id is not None:
            da_id = self.id

        return "Label{ id: '%i', name: '%s'}" % (da_id, self.name)

    @staticmethod
    def from_db(entity_id: int) -> "Label":
        db = get_db()
        label = db.execute("SELECT * from labels where labels.id = ?", (entity_id,)).fetchone()
        return Label(name=label["name"], label_id=label["id"])
