__all__ = [
    "Floor",
]

import time
from typing import AnyStr, Optional

from anobbs_core.utils.id_utils import get_uuid
from anobbs_core.utils.type_utils import EnumType


class Floor:
    class Keys(EnumType):
        ID = "id"
        NO = "no"
        OWNER_AC = "owner_ac"
        CONTENT = "content"
        CREATE_DATE = "create_date"
        HIDE = "hide"

    def __init__(self, **data):
        try:
            self.__owner_ac = data[self.Keys.OWNER_AC]
            self.__content = data[self.Keys.CONTENT]

            self.__id = data.get(self.Keys.ID, get_uuid())
            self.__no = data.get(self.Keys.NO, "")
            self.__hide = data.get(self.Keys.HIDE, False)
            self.__create_date = data.get(self.Keys.CREATE_DATE, time.time())
        except (KeyError, ValueError):
            raise RuntimeError(f"Init {self.__class__.__name__} error: {data}")

    @property
    def id(self) -> AnyStr:
        return self.__id

    @property
    def owner_ac(self) -> AnyStr:
        return self.__owner_ac

    @property
    def content(self) -> AnyStr:
        return self.__content

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
            self.Keys.NO: self.__no,
        }

    def to_display_dict(self) -> Optional[dict]:
        if self.__hide:
            return None

        data = self.to_dict()
        data.pop(self.Keys.HIDE, False)
        data[self.Keys.OWNER_AC] = data[self.Keys.OWNER_AC][:8]
        return data
