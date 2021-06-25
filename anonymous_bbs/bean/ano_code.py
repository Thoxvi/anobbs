__all__ = [
    "AnoCode",
]

import time

from anonymous_bbs.utils.id_utils import get_uuid
from anonymous_bbs.utils.type_utils import EnumType


class AnoCode:
    class Keys(EnumType):
        ID = "id"
        LOGS = "logs"
        OWNER = "owner"
        CREATE_DATE = "create_date"
        BLOCK_DATE = "block_date"
        IS_BLOCKED = "is_blocked"

    class Status(EnumType):
        CREATED = "created"
        BLOCKED = "blocked"

    @classmethod
    def from_dict(cls, data: dict) -> "AnoCode":
        return cls(**data)

    def __init__(self, **data):
        super().__init__(**data)
        try:
            self.__owner = data[self.Keys.OWNER]

            self.__id = data.get(self.Keys.ID, get_uuid())
            self.__logs = data.get(self.Keys.LOGS, [])
            if len(self.__logs) == 0:
                self.__logs.append((self.Status.CREATED, time.time()))
        except (KeyError, ValueError):
            raise RuntimeError(f"Init {self.__class__.__name__} error: {data}")

    @property
    def id(self) -> float:
        return self.__id

    @property
    def create_date(self) -> float:
        return self.__logs[0][1]

    @property
    def is_blocked(self) -> bool:
        for status, _ in reversed(self.__logs):
            if status == self.Status.BLOCKED:
                return True
        return False

    def set_status(self, status: str) -> bool:
        if status not in self.Status.get_list():
            return False
        self.__logs.append((status, time.time()))
        return True

    def to_dict(self) -> dict:
        return {
            self.Keys.OWNER: self.__owner,
            self.Keys.ID: self.__id,
            self.Keys.LOGS: self.__logs,

            self.Keys.CREATE_DATE: self.create_date,
            self.Keys.IS_BLOCKED: self.is_blocked,
        }
