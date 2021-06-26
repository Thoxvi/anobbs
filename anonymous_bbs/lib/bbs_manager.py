__all__ = [
    "BbsManager",
]

from typing import List, Optional, AnyStr

from anonymous_bbs.bean import Account, InvitationCode, AnoCode
from anonymous_bbs.utils.id_utils import get_uuid
from .account_manager import am
from .invitation_code_manager import icm
from .ano_code_manager import acm

ROOT_MAX_ANO_SIZE = 2 ** 10
ROOT_IC_MARGIN = 2 ** 10


class BbsManager:
    def __init__(self):
        self.__am = am
        self.__icm = icm
        self.__acm = acm

    def create_account_by_ic(self, ic_id: AnyStr) -> Optional[Account]:
        if self.__icm.is_ic_used(ic_id):
            return None

        bid = get_uuid()
        if not self.__icm.use_ic(ic_id, bid):
            return None

        account = Account(**{
            Account.Keys.ID: bid,
            Account.Keys.INVITER_ID: self.__icm.get_ic(ic_id).aid,
        })
        if self.__am.add_account(account):
            return account
        else:
            return None

    def create_root_account(self) -> Optional[Account]:
        account = Account(**{
            Account.Keys.MAX_ANO_SIZE: ROOT_MAX_ANO_SIZE,
            Account.Keys.IC_MARGIN: ROOT_IC_MARGIN,
        })
        if self.__am.add_account(account):
            return account
        else:
            return None

    def create_ic(self, a_id: AnyStr) -> Optional[InvitationCode]:
        return self.__am.create_ic(a_id)

    def create_ac(self, a_id: AnyStr) -> Optional[AnoCode]:
        return self.__am.create_ac(a_id)

    def get_all_root_account(self) -> List[Account]:
        return self.__am.get_all_root_accounts()

    def show(self):
        self.__icm.show()
        print("---------")
        self.__am.show()
        print("---------")
        self.__acm.show()
