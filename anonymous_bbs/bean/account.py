__all__ = [
    "Account",
]

import time
from typing import Optional, AnyStr

from anonymous_bbs.utils.id_utils import get_uuid
from anonymous_bbs.utils.type_utils import EnumType
from .ano_code import AnoCode
from .invitation_code import InvitationCode

DEFAULT_AC_SIZE = 5
DEFAULT_IC_SIZE = 2


class Account:
    class Keys(EnumType):
        ID = "id"
        MAX_ANO_SIZE = "max_ano_size"
        IC_MARGIN = "ic_margin"
        AC_ID_LIST = "ac_id_list"
        INVITER_ID = "inviter_id"
        LOGS = "logs"
        CREATE_DATE = "create_date"
        UPDATE_DATE = "update_date"
        IS_BLOCKED = "is_blocked"
        IS_DELETED = "is_deleted"
        IS_ROOT = "is_root"

    class Status(EnumType):
        CREATED = "created"
        BLOCKED = "blocked"
        UNBLOCKED = "unblocked"
        DELETED = "deleted"
        UNDELETED = "undeleted"

    def __init__(self, **data):
        try:
            self.__id = data.get(self.Keys.ID, get_uuid())
            self.__max_ano_size = data.get(self.Keys.MAX_ANO_SIZE, DEFAULT_AC_SIZE)
            self.__ac_id_list = data.get(self.Keys.AC_ID_LIST, [])
            self.__inviter = data.get(self.Keys.INVITER_ID)
            self.__ic_margin = data.get(self.Keys.IC_MARGIN, DEFAULT_IC_SIZE)
            self.__logs = data.get(self.Keys.LOGS, [])
            if len(self.__logs) == 0:
                self.__logs.append((self.Status.CREATED, time.time()))
        except (KeyError, ValueError):
            raise RuntimeError(f"Init {self.__class__.__name__} error: {data}")

    @property
    def id(self) -> AnyStr:
        return self.__id

    @property
    def create_date(self) -> float:
        return self.__logs[0][1]

    @property
    def update_date(self) -> float:
        return self.__logs[-1][1]

    @property
    def is_blocked(self) -> bool:
        for status, _ in reversed(self.__logs):
            if status == self.Status.BLOCKED:
                return True
            if status == self.Status.UNBLOCKED:
                return False
        return False

    @property
    def is_deleted(self) -> bool:
        for status, _ in reversed(self.__logs):
            if status == self.Status.DELETED:
                return True
            if status == self.Status.UNDELETED:
                return False
        return False

    @property
    def is_root(self) -> bool:
        return self.__inviter is None

    def set_status(self, status: AnyStr) -> bool:
        if status not in self.Status.get_list():
            return False
        self.__logs.append((status, time.time()))
        return True

    def create_ac(self) -> Optional[AnoCode]:
        if len(self.__ac_id_list) < self.__max_ano_size:
            ac = AnoCode(**{
                AnoCode.Keys.OWNER: self.__id,
            })
            self.__ac_id_list.append(ac.id)
            return ac
        else:
            return None

    def create_ic(self) -> Optional[InvitationCode]:
        if self.__ic_margin > 0:
            self.__ic_margin -= 1
            ic = InvitationCode(**{
                InvitationCode.Keys.AID: self.__id
            })
            return ic
        else:
            return None

    def to_dict(self) -> dict:
        return {
            self.Keys.ID: self.__id,
            self.Keys.MAX_ANO_SIZE: self.__max_ano_size,
            self.Keys.AC_ID_LIST: self.__ac_id_list,
            self.Keys.INVITER_ID: self.__inviter,
            self.Keys.LOGS: self.__logs,
            self.Keys.IC_MARGIN: self.__ic_margin,

            self.Keys.CREATE_DATE: self.create_date,
            self.Keys.UPDATE_DATE: self.update_date,
            self.Keys.IS_DELETED: self.is_deleted,
            self.Keys.IS_BLOCKED: self.is_blocked,
            self.Keys.IS_ROOT: self.is_root,
        }
