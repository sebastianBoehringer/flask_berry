import os
from abc import ABC

from app.data.DbEntity import DbEntity


class LibraryEntry(DbEntity, ABC):
    name: str = ""
    location: str

    def __init__(self, name: str, location: str, entry_id: int = None):
        super().__init__(entry_id)
        assert len(name) > 0, "LibraryEntry has no name"
        self.name = name
        assert os.path.exists(location), "Location of LibraryEntry does not exist"
        self.location = location
        assert (entry_id is None) or (entry_id >= 0), "Id of LibraryEntry is negative"
        self._id = entry_id
