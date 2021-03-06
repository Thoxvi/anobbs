__all__ = [
    "InvitationCodeDbConnector",
    "invitation_code_db_connector",
]

from typing import Optional, AnyStr

from anobbs_core.base import BaseDbConnect, get_mongo_db_uri
from anobbs_core.bean import InvitationCode


class InvitationCodeDbConnector(BaseDbConnect):
    __TABLE_NAME = "invitation_code"

    def __init__(self, uri: AnyStr):
        super().__init__(uri, self.__TABLE_NAME)

    def add_ic(self, ic: InvitationCode) -> bool:
        return self._update(ic.to_dict())

    def is_ic_used(self, ic_id: AnyStr) -> bool:
        return self._count({self._id_key: ic_id, InvitationCode.Keys.IS_USED: True}) > 0

    def get_ic(self, ic_id: AnyStr) -> Optional[InvitationCode]:
        data = self._query_one({self._id_key: ic_id})
        return InvitationCode(**data) if data else None

    def use_ic(self, ic_id: AnyStr, bid: AnyStr) -> bool:
        ic = self.get_ic(ic_id)
        if ic:
            ic.set_used(bid)
            return self._update(ic.to_dict())
        else:
            return False

    def show(self):
        print(f"InvitationCode Info:")
        print(f"\tNumber of all InvitationCode:\t{self._count()}")
        print(f"\tNumber of unused InvitationCode:\t{self._count({InvitationCode.Keys.IS_USED: False})}")
        print("\n".join([
            f"\t\t{ic.get(InvitationCode.Keys.ID)}"
            for ic
            in self._query({InvitationCode.Keys.IS_USED: False})
        ]))
        print(f"\tNumber of used InvitationCode:\t{self._count({InvitationCode.Keys.IS_USED: True})}")
        print("\n".join([
            f"\t\t{ic.get(InvitationCode.Keys.ID)}"
            for ic
            in self._query({InvitationCode.Keys.IS_USED: True})
        ]))


invitation_code_db_connector = InvitationCodeDbConnector(get_mongo_db_uri())
