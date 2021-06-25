__all__ = [
    "Page",
]

import time

from anonymous_bbs.utils.id_utils import get_uuid
from anonymous_bbs.utils.type_utils import EnumType

DEFAULT_AC_SIZE = 5
DEFAULT_IC_SIZE = 2


class Page:
    class Keys(EnumType):
        ID = "id"
        OWNER_AC = "owner_ac"
        FIRST_FLOOR_ID = "first_floor_id"
        FLOOR_ID_LIST = "floor_id_list"
        CREATE_DATE = "create_date"
        UPDATE_DATE = "update_date"
        HIDE = "hide"

    @classmethod
    def from_dict(cls, data: dict) -> "Page":
        return cls(**data)

    def __init__(self, **data):
        super().__init__(**data)
        try:
            self.__owner_ac = data[self.Keys.OWNER_AC]
            self.__first_floor_id = data[self.Keys.FIRST_FLOOR_ID]

            self.__id = data.get(self.Keys.ID, get_uuid())
            self.__hide = data.get(self.Keys.HIDE, False)
            self.__floor_id_list = data.get(self.Keys.FLOOR_ID_LIST, [
                (self.__first_floor_id, time.time())
            ])
        except (KeyError, ValueError):
            raise RuntimeError(f"Init {self.__class__.__name__} error: {data}")

    @property
    def create_date(self) -> float:
        return self.__floor_id_list[0][1]

    @property
    def update_date(self) -> float:
        return self.__floor_id_list[-1][1]

    @property
    def hide(self) -> bool:
        return self.__hide

    def add_floor(self, fid: str) -> bool:
        self.__floor_id_list.append((fid, time.time()))
        return True

    def to_dict(self) -> dict:
        return {
            self.Keys.ID: self.__id,
            self.Keys.FLOOR_ID_LIST: self.__floor_id_list,
            self.Keys.FIRST_FLOOR_ID: self.__first_floor_id,
            self.Keys.HIDE: self.__hide,

            self.Keys.CREATE_DATE: self.create_date,
            self.Keys.UPDATE_DATE: self.update_date,
        }
