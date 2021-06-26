__all__ = [
    "FloorManager",
    "fm",
]

from typing import Optional, AnyStr

from anonymous_bbs.base import BaseDbConnect, get_mongo_db_uri
from anonymous_bbs.bean import Floor
from .ano_code_manager import acm


class FloorManager(BaseDbConnect):
    __TABLE_NAME = "floor"

    def __init__(self, uri: AnyStr):
        super().__init__(uri, self.__TABLE_NAME)

    def create_floor(self, ac_id: AnyStr, content: AnyStr) -> Optional[Floor]:
        if not acm.check_ac(ac_id):
            return None
        if not content:
            return None
        floor = Floor(**{
            Floor.Keys.OWNER_AC: ac_id,
            Floor.Keys.CONTENT: content,
        })
        if self._update(floor.to_dict()):
            return floor
        else:
            return None

    def show(self):
        print(f"Floor Info:")
        print(f"\tNumber of all Floor:\t{self._count()}")
        print(f"\tNumber of Not hidden Floor:\t{self._count({Floor.Keys.HIDE: False})}")
        print(f"\tNumber of Hide Floor:\t{self._count({Floor.Keys.HIDE: True})}")


fm = FloorManager(get_mongo_db_uri())
