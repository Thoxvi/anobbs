__all__ = [
    "Group",
]

import time
from typing import AnyStr, List, Optional

from anonymous_bbs.utils.id_utils import get_uuid
from anonymous_bbs.utils.type_utils import EnumType


class Group:
    class Keys(EnumType):
        ID = "id"
        NAME = "name"
        PAGE_ID_LIST = "page_id_list"
        CREATE_DATE = "create_date"
        HIDE = "hide"

    def __init__(self, **data):
        try:
            self.__name = data[self.Keys.NAME]
            self.__id = data.get(self.Keys.ID, get_uuid())
            self.__hide = data.get(self.Keys.HIDE, False)
            self.__create_date = data.get(self.Keys.CREATE_DATE, time.time())
            self.__page_id_list = data.get(self.Keys.PAGE_ID_LIST, [])
        except (KeyError, ValueError):
            raise RuntimeError(f"Init {self.__class__.__name__} error: {data}")

    @property
    def page_id_list(self) -> List[AnyStr]:
        return self.__page_id_list[:]

    @property
    def create_date(self) -> float:
        return self.__create_date

    @property
    def hide(self) -> bool:
        return self.__hide

    def add_page(self, pid: str) -> bool:
        self.__page_id_list.append(pid)
        return True

    def to_dict(self) -> dict:
        return {
            self.Keys.ID: self.__id,
            self.Keys.NAME: self.__name,
            self.Keys.CREATE_DATE: self.__create_date,
            self.Keys.HIDE: self.__hide,
            self.Keys.PAGE_ID_LIST: self.__page_id_list,
        }

    def to_display_dict(self) -> Optional[dict]:
        if self.__hide:
            return None

        data = self.to_dict()
        data.pop(self.Keys.HIDE, False)
        return data
