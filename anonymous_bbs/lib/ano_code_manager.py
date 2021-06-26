__all__ = [
    "AnoCodeManager",
    "acm",
]

from anonymous_bbs.base import BaseDbConnect, get_mongo_db_uri

from typing import Optional, AnyStr

from anonymous_bbs.bean import AnoCode


class AnoCodeManager(BaseDbConnect):
    __TABLE_NAME = "ano_code"

    def __init__(self, uri: AnyStr):
        super().__init__(uri, self.__TABLE_NAME)

    def add_ac(self, ac: AnoCode) -> bool:
        return self._update(ac.to_dict())

    def get_ac(self, ac_id: AnyStr) -> Optional[AnoCode]:
        data = self._query_one({self.ID_KEY: ac_id})
        return AnoCode.from_dict(data) if data else None

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
        print(f"\tAll AnoCode number:\t{self._count()}")
        print(f"\tUnblock AnoCode number:\t{self._count({AnoCode.Keys.IS_BLOCKED: False})}")
        print(f"\tblock AnoCode number:\t{self._count({AnoCode.Keys.IS_BLOCKED: True})}")


acm = AnoCodeManager(get_mongo_db_uri())
