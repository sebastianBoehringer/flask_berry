from typing import List, Optional

from app.data.Label import Label
from app.data.LibraryEntry import LibraryEntry
from app.data.db import get_db


class Book(LibraryEntry):
    authors: List[str]
    publisher: str
    labels: List[Label]

    def __init__(self, authors: List[str], publisher: str, labels: List[Label], name: str, location: str,
                 entry_id: int = None):
        super().__init__(name=name, location=location, entry_id=entry_id)
        assert len(authors) > 0, "Book has no authors"
        self.authors = authors

        assert len(publisher) > 0, "publisher of book is empty"
        self.publisher = publisher
        self.labels = labels

    def __repr__(self) -> str:
        da_id = self.id
        if self._id is None:
            da_id = -1
        return "Book{ id: '%i', name: '%s', location: '%s', authors: %s, publisher: '%s', labels: %s}" % \
               (da_id, self.name, self.location, str(self.authors), self.publisher, str(self.labels))

    def save(self):
        if self.id is not None:
            print("Book has id, calling update instead")
            self.update()
            return
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO books (publisher, name, location) "
                       "VALUES (?, ?, ?)", (self.publisher, self.name, self.location))
        db.commit()
        self._id = cursor.lastrowid
        self.__save_relations()

    def __delete_relations(self):
        db = get_db()
        db.execute("DELETE from book_labels where book_id = ?", (self.id,))
        db.execute("DELETE FROM book_authors where book_id = ?", (self.id,))
        db.commit()

    def __save_relations(self):
        db = get_db()
        for author in self.authors:
            db.execute("INSERT INTO book_authors (author, book_id) VALUES (?, ?)",
                       (author, self.id))
            db.commit()
        for label in self.labels:
            if label.id is None:
                label.save()
            db.execute("INSERT INTO book_labels (book_id, label_id) VALUES (?, ?)",
                       (self.id, label.id))
            db.commit()

    def update(self):
        if self.id is None:
            print("Book has no id, calling save instead")
            self.save()
            return
        db = get_db()
        db.execute("UPDATE books SET publisher = ?, name = ?, location = ? WHERE id = ?",
                   (self.publisher, self.name, self.location, self.id))
        db.commit()
        self.__delete_relations()
        self.__save_relations()

    def delete(self):
        if self.id is None:
            print(f"Can't delete a Book without id, tried to delete {self}")
            return False
        db = get_db()
        db.execute("DELETE FROM books where id = ?", (self.id,))
        self.__delete_relations()
        self._id = None
        return True

    @staticmethod
    def from_db(entity_id: int) -> Optional["Book"]:
        db = get_db()
        book = db.execute("SELECT * FROM books where id = ?", (entity_id,)).fetchone()
        if book is None:
            return None
        book_id = book["id"]
        label_ids = db.execute("SELECT label_id from book_labels where book_id = ?", (book_id,)).fetchall()
        label_list = []
        for row in label_ids:
            label = Label.from_db(row["label_id"])
            label_list.append(label)
        author_result = db.execute("SELECT author from book_authors where book_id = ?", (book_id,)).fetchall()
        authors = []
        for row in author_result:
            authors.append(row["author"])
        return Book(entry_id=book_id, authors=authors, publisher=book["publisher"], labels=label_list,
                    name=book["name"], location=book["location"])
