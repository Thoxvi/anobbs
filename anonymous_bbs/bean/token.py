__all__ = [
    "Token",
]

import time
from typing import AnyStr

from anonymous_bbs.utils.id_utils import get_uuid
from anonymous_bbs.utils.type_utils import EnumType


class Token:
    class Keys(EnumType):
        ID = "id"
        OWNED_ACCOUNT_ID = "owned_account_id"
        EXPIRE_DATE = "expire_date"
        CREATE_DATE = "create_date"
        IS_EXPIRED = "is_expired"

    def __init__(self, **data):
        try:
            self.__owned_account_id = data[self.Keys.OWNED_ACCOUNT_ID]
            self.__expire_date = data[self.Keys.EXPIRE_DATE]

            self.__id = data.get(self.Keys.ID, get_uuid())
            self.__create_date = data.get(self.Keys.CREATE_DATE, time.time())
        except (KeyError, ValueError):
            raise RuntimeError(f"Init {self.__class__.__name__} error: {data}")

    @property
    def id(self) -> AnyStr:
        return self.__id

    @property
    def owned_account_id(self) -> AnyStr:
        return self.__owned_account_id

    @property
    def create_date(self) -> float:
        return self.__create_date

    @property
    def expire_date(self) -> float:
        return self.__expire_date

    @property
    def is_expired(self) -> bool:
        return time.time() > self.__expire_date

    def to_dict(self) -> dict:
        return {
            self.Keys.ID: self.__id,
            self.Keys.OWNED_ACCOUNT_ID: self.__owned_account_id,
            self.Keys.EXPIRE_DATE: self.__expire_date,
            self.Keys.CREATE_DATE: self.__create_date,
            self.Keys.IS_EXPIRED: self.is_expired,
        }
