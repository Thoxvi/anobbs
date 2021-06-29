__all__ = [
    "AnoCodeDbConnector",
    "ano_code_db_connector",
]

from typing import Optional, AnyStr

from anobbs_core.base import BaseDbConnect, get_mongo_db_uri
from anobbs_core.bean import AnoCode


class AnoCodeDbConnector(BaseDbConnect):
    __TABLE_NAME = "ano_code"

    def __init__(self, uri: AnyStr):
        super().__init__(uri, self.__TABLE_NAME)

    def check_ac(self, ac_id: AnyStr) -> bool:
        return self._count({
            AnoCode.Keys.ID: ac_id,
            AnoCode.Keys.IS_BLOCKED: False,
        }) == 1

    def add_ac(self, ac: AnoCode) -> bool:
        return self._update(ac.to_dict())

    def get_ac(self, ac_id: AnyStr) -> Optional[AnoCode]:
        data = self._query_one({self._id_key: ac_id})
        return AnoCode(**data) if data else None

    def block_ac(self, ac_id: AnyStr) -> bool:
        ac = self.get_ac(ac_id)
        if ac:
            ac.set_status(AnoCode.Status.BLOCKED)
            self._update(ac.to_dict())
            return True
        else:
            return False

    def show(self):
        print(f"AnoCode Info:")
        print(f"\tNumber of all AnoCode:\t{self._count()}")
        print(f"\tNumber of Unblock AnoCode:\t{self._count({AnoCode.Keys.IS_BLOCKED: False})}")
        print(f"\tNumber of block AnoCode:\t{self._count({AnoCode.Keys.IS_BLOCKED: True})}")


ano_code_db_connector = AnoCodeDbConnector(get_mongo_db_uri())
