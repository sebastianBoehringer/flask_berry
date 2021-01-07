import os
from abc import ABC
from typing import Set, Tuple

from app.data.DbEntity import DbEntity
from app.data.Label import Label


class LibraryEntry(DbEntity, ABC):
    name: str
    location: str
    labels: Set[Label]

    def __init__(self, name: str, location: str, labels: Set[Label], entry_id: int = None):
        super().__init__(entry_id)
        assert len(name) > 0, "LibraryEntry has no name"
        self.name = name
        assert os.path.exists(location), "Location of LibraryEntry does not exist"
        self.location = location
        assert (entry_id is None) or (entry_id >= 0), "Id of LibraryEntry is negative"
        self._id = entry_id
        self.labels = labels

    def __eq__(self, other):
        if super().__eq__(other):
            if type(other) is type(self):
                return self.name == other.name and self.location == other.location and self.labels == other.labels
        return False

    def _key(self) -> Tuple:
        return *super()._key(), self.name, self.location, self.labels
