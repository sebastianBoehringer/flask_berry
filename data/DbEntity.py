from abc import abstractmethod, ABC


class DbEntity(ABC):
    @property
    def id(self) -> int:
        return self._id

    def __init__(self, entity_id: int = None):
        assert (entity_id is None) or (entity_id >= 0), "DbEntities id is negative"
        self._id = entity_id

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def from_db(entity_id: int):
        pass
