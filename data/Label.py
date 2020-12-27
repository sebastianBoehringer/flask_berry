from data.DbEntity import DbEntity
from data.db import get_db
from error.Errors import MissingValueError


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
            raise MissingValueError("label has no id")
        # TODO labels might still be in use, fail gracefully in that case
        # TODO clean up relation tables
        db = get_db()
        db.execute("DELETE from labels where labels.id = ?", (self._id,))
        db.commit()
        self._id = None

    def __str__(self):
        da_id = -1
        if self.id is not None:
            da_id = self.id

        return "Label{ id: %i, name: %s}" % (da_id, self.name)

    @staticmethod
    def from_db(entity_id: int) -> "Label":
        db = get_db()
        label = db.execute("SELECT * from labels where labels.id = ?", (entity_id,)).fetchone()
        return Label(name=label["name"], label_id=label["id"])
