__all__ = [
    "FloorDbConnector",
    "floor_db_connector",
]

from typing import Optional, AnyStr

from anonymous_bbs.base import BaseDbConnect, get_mongo_db_uri
from anonymous_bbs.bean import Floor
from .ano_code import ano_code_db_connector
from .config import config_db_connector


class FloorDbConnector(BaseDbConnect):
    __TABLE_NAME = "floor"

    def __init__(self, uri: AnyStr):
        super().__init__(uri, self.__TABLE_NAME)

    def create_floor(self, ac_id: AnyStr, content: AnyStr) -> Optional[Floor]:
        if not ano_code_db_connector.check_ac(ac_id):
            return None
        if not content:
            return None
        floor = Floor(**{
            Floor.Keys.OWNER_AC: ac_id,
            Floor.Keys.CONTENT: content,
            Floor.Keys.NO: config_db_connector.get_new_floor_number(),
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


floor_db_connector = FloorDbConnector(get_mongo_db_uri())
