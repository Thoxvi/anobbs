__all__ = [
    "AnoCodeManager",
]

from typing import Optional

from anonymous_bbs.bean import AnoCode


class AnoCodeManager:
    def __init__(self):
        self.__unblocked_ac_id_set = set()

    def is_ac_blocked(self, ac_id: str) -> bool:
        return ac_id not in self.__unblocked_ac_id_set

    def get_ac(self, ac_id: str) -> Optional[AnoCode]:
        # TODO read from db
        return None

    def block_ac(self, ac_id: str) -> bool:
        ac = self.get_ac(ac_id)
        if ac:
            ac.set_status(AnoCode.Status.BLOCKED)
            # TODO save to db
            return True
        else:
            return False
