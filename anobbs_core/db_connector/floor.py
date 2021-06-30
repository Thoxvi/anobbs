__all__ = [
    "FloorDbConnector",
    "floor_db_connector",
]

import time
from typing import Optional, AnyStr

from anobbs_core.base import BaseDbConnect, get_mongo_db_uri
from anobbs_core.bean import Floor, AnoCode
from .account import account_db_connector
from .ano_code import ano_code_db_connector
from .config import config_db_connector

INTERVAL_BETWEEN_TWO_SPEECHES = 5


class FloorDbConnector(BaseDbConnect):
    __TABLE_NAME = "floor"

    def __init__(self, uri: AnyStr):
        super().__init__(uri, self.__TABLE_NAME)

    def get_floor(self, floor_id: AnyStr) -> Optional[Floor]:
        floor = self.query_one({Floor.Keys.ID: floor_id})
        if floor:
            floor = Floor(**floor)
        return floor

    def create_floor(self, ac_id: AnyStr, content: AnyStr) -> Optional[Floor]:
        ac = ano_code_db_connector.get_ac(ac_id)
        if not ac:
            return None
        account = account_db_connector.get_account(ac.owner)
        if not account:
            return None
        if not account.is_root and time.time() - ac.last_speaking_time < 5:
            return None
        if not content:
            return None
        floor = Floor(**{
            Floor.Keys.OWNER_AC: ac_id,
            Floor.Keys.CONTENT: content,
            Floor.Keys.NO: config_db_connector.get_new_floor_number(),
        })
        if self._update(floor.to_dict()):
            ano_code_db_connector.update({
                **ac.to_dict(),
                AnoCode.Keys.LAST_SPEAKING_TIME: time.time()
            })
            return floor
        else:
            return None

    def show(self):
        print(f"Floor Info:")
        print(f"\tNumber of all Floor:\t{self._count()}")
        print(f"\tNumber of Not hidden Floor:\t{self._count({Floor.Keys.HIDE: False})}")
        print(f"\tNumber of Hide Floor:\t{self._count({Floor.Keys.HIDE: True})}")


floor_db_connector = FloorDbConnector(get_mongo_db_uri())
