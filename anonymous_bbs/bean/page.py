__all__ = [
    "Page",
]

from typing import AnyStr, List, Optional

from anonymous_bbs.utils.id_utils import get_uuid
from anonymous_bbs.utils.type_utils import EnumType


class Page:
    class Keys(EnumType):
        ID = "id"
        OWNER_AC = "owner_ac"
        FIRST_FLOOR_ID = "first_floor_id"
        FLOOR_ID_LIST = "floor_id_list"
        CREATE_DATE = "create_date"
        UPDATE_DATE = "update_date"
        HIDE = "hide"

    def __init__(self, **data):
        try:
            self.__owner_ac = data[self.Keys.OWNER_AC]
            self.__first_floor_id = data[self.Keys.FIRST_FLOOR_ID]

            self.__id = data.get(self.Keys.ID, get_uuid())
            self.__hide = data.get(self.Keys.HIDE, False)
            self.__floor_id_list = data.get(self.Keys.FLOOR_ID_LIST, [self.__first_floor_id])
        except (KeyError, ValueError):
            raise RuntimeError(f"Init {self.__class__.__name__} error: {data}")

    @property
    def id(self) -> AnyStr:
        return self.__id

    @property
    def floor_id_list(self) -> List[AnyStr]:
        return self.__floor_id_list[:]

    @property
    def owner_ac(self) -> AnyStr:
        return self.__owner_ac

    @property
    def create_date(self) -> float:
        return self.__floor_id_list[0]

    @property
    def update_date(self) -> float:
        return self.__floor_id_list[-1]

    @property
    def hide(self) -> bool:
        return self.__hide

    def add_floor(self, fid: str) -> bool:
        self.__floor_id_list.append(fid)
        return True

    def to_dict(self) -> dict:
        return {
            self.Keys.ID: self.__id,
            self.Keys.FLOOR_ID_LIST: self.__floor_id_list,
            self.Keys.OWNER_AC: self.__owner_ac,
            self.Keys.FIRST_FLOOR_ID: self.__first_floor_id,
            self.Keys.HIDE: self.__hide,

            self.Keys.CREATE_DATE: self.create_date,
            self.Keys.UPDATE_DATE: self.update_date,
        }

    def to_display_dict(self) -> Optional[dict]:
        if self.__hide:
            return None

        data = self.to_dict()
        data.pop(self.Keys.HIDE, False)
        data[self.Keys.OWNER_AC] = data[self.Keys.ID][:8]
        return data
