__all__ = [
    "InvitationCodeManager",
]

from typing import Optional

from anonymous_bbs.bean import InvitationCode


class InvitationCodeManager:
    def __init__(self):
        self.__unused_ic_id_set = set()

    def is_ic_used(self, ic_id: str) -> bool:
        return ic_id not in self.__unused_ic_id_set

    def get_ic(self, ic_id: str) -> Optional[InvitationCode]:
        # TODO read from db
        return None

    def use_ic(self, ic_id: str, bid: str) -> bool:
        # TODO update ic
        ic = self.get_ic(ic_id)
        if ic:
            ic.set_used(bid)
            # TODO write to db
            return True
        else:
            return False
