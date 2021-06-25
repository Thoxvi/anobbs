__all__ = [
    "Floor",
]

import time

from anonymous_bbs.utils.id_utils import get_uuid
from anonymous_bbs.utils.type_utils import EnumType


class Floor:
    class Keys(EnumType):
        ID = "id"
        OWNER_AC = "owner_ac"
        CONTENT = "content"
        CREATE_DATE = "create_date"
        HIDE = "hide"

    @classmethod
    def from_dict(cls, data: dict) -> "Floor":
        return cls(**data)

    def __init__(self, **data):
        super().__init__(**data)
        try:
            self.__owner_ac = data[self.Keys.OWNER_AC]
            self.__content = data[self.Keys.CONTENT]

            self.__id = data.get(self.Keys.ID, get_uuid())
            self.__hide = data.get(self.Keys.HIDE, False)
            self.__create_date = data.get(self.Keys.CREATE_DATE, time.time())
        except (KeyError, ValueError):
            raise RuntimeError(f"Init {self.__class__.__name__} error: {data}")

    @property
    def create_date(self) -> float:
        return self.__create_date

    @property
    def hide(self) -> bool:
        return self.__hide

    def to_dict(self) -> dict:
        return {
            self.Keys.ID: self.__id,
            self.Keys.OWNER_AC: self.__owner_ac,
            self.Keys.CONTENT: self.__content,
            self.Keys.HIDE: self.__hide,
            self.Keys.CREATE_DATE: self.__create_date,
        }
