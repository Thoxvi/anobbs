__all__ = [
    "BbsManager",
]

from anonymous_bbs.bean import Account
from anonymous_bbs.utils.id_utils import get_uuid
from .account_manager import AccountManager
from .invitation_code_manager import InvitationCodeManager

ROOT_MAX_ANO_SIZE = 2 ** 10
ROOT_IC_MARGIN = 2 ** 10


class BbsManager:
    def __init__(self):
        self.__am = AccountManager()
        self.__icm = InvitationCodeManager()

    def add_account_by_ic(self, ic_id: str) -> bool:
        if self.__icm.is_ic_used(ic_id):
            return False

        bid = get_uuid()
        if not self.__icm.use_ic(ic_id, bid):
            return False

        return self.__am.add_account(Account(**{
            Account.Keys.ID: bid,
            Account.Keys.INVITER_ID: self.__icm.get_ic(ic_id).aid,
        }))

    def add_root_account(self) -> bool:
        return self.__am.add_account(Account(**{
            Account.Keys.MAX_ANO_SIZE: ROOT_MAX_ANO_SIZE,
            Account.Keys.IC_MARGIN: ROOT_IC_MARGIN,
        }))
