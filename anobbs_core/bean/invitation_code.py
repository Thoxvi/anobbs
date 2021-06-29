__all__ = [
    "InvitationCode",
]

import time
from typing import Optional, AnyStr

from anobbs_core.utils.id_utils import get_uuid
from anobbs_core.utils.type_utils import EnumType


class InvitationCode:
    class Keys(EnumType):
        ID = "id"
        LOGS = "logs"
        AID = "aid"
        BID = "bid"
        CREATE_DATE = "create_date"
        USED_DATE = "used_date"
        IS_USED = "is_used"

    class Status(EnumType):
        CREATED = "created"
        USED = "used"

    def __set_status(self, status: AnyStr) -> bool:
        if status not in self.Status.get_list():
            return False
        self.__logs.append((status, time.time()))
        return True

    def __init__(self, **data):
        try:
            self.__aid = data[self.Keys.AID]
            self.__bid = data.get(self.Keys.BID)

            self.__id = data.get(self.Keys.ID, get_uuid())
            self.__logs = data.get(self.Keys.LOGS, [])
            if len(self.__logs) == 0:
                self.__logs.append((self.Status.CREATED, time.time()))
        except (KeyError, ValueError):
            raise RuntimeError(f"Init {self.__class__.__name__} error: {data}")

    @property
    def id(self) -> AnyStr:
        return self.__id

    @property
    def aid(self) -> AnyStr:
        return self.__aid

    @property
    def bid(self) -> AnyStr:
        return self.__bid

    @property
    def create_date(self) -> float:
        return self.__logs[0][1]

    @property
    def used_date(self) -> Optional[float]:
        if self.is_used:
            return self.__logs[-1][1]
        else:
            return None

    @property
    def is_used(self) -> bool:
        for status, _ in reversed(self.__logs):
            if status == self.Status.USED:
                return True
        return False

    def set_used(self, bid: AnyStr):
        self.__bid = bid
        self.__set_status(self.Status.USED)

    def to_dict(self) -> dict:
        return {
            self.Keys.ID: self.__id,
            self.Keys.AID: self.__aid,
            self.Keys.BID: self.__bid,
            self.Keys.LOGS: self.__logs,

            self.Keys.CREATE_DATE: self.create_date,
            self.Keys.USED_DATE: self.used_date,
            self.Keys.IS_USED: self.is_used,
        }

    def to_display_dict(self) -> dict:
        data = self.to_dict()
        data[self.Keys.AID] = data[self.Keys.AID][:8]
        bid = data.get(self.Keys.BID)
        if bid:
            data[self.Keys.BID] = bid[:8]
        data.pop(self.Keys.LOGS, None)
        return data
