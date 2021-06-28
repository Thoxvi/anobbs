__all__ = [
    "BbsManager",
]

import logging
from typing import List, Optional, AnyStr

from anonymous_bbs.bean import Account, InvitationCode, AnoCode, Page, Group, Token
from anonymous_bbs.utils.id_utils import get_uuid
from .account_manager import am
from .ano_code_manager import acm
from .floor_manager import fm
from .group_manager import gm
from .invitation_code_manager import icm
from .page_manager import pm
from .token_manager import tm

ROOT_MAX_ANO_SIZE = 2 ** 10
ROOT_IC_MARGIN = 2 ** 10

logger = logging.getLogger("AnoBBS")


class BbsManager:
    def __init__(self):
        self.__am = am
        self.__icm = icm
        self.__acm = acm
        self.__pm = pm
        self.__fm = fm
        self.__gm = gm
        self.__tm = tm

    def init(self) -> bool:
        # 1. Create admin
        admin = self.get_admin_account()
        if not admin:
            logger.error("Create admin error")
            return False
        else:
            logger.info(f"Admin ID: {admin.id}")

    def login(self, a_id: AnyStr) -> Optional[Token]:
        return self.__am.login(a_id)

    def get_owner_id_by_token_id(self, tid: AnyStr) -> Optional[AnyStr]:
        return self.__tm.get_owner_id_by_token_id(tid)

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
            logger.info(
                f"InvitationCode used:"
                f"\tIC: {ic_id}"
                f"\tInviter: {account.inviter_id}"
                f"\tAccount: {account.id}"
            )
            return account
        else:
            return None

    def create_root_account(self) -> Optional[Account]:
        account = Account(**{
            Account.Keys.MAX_ANO_SIZE: ROOT_MAX_ANO_SIZE,
            Account.Keys.IC_MARGIN: ROOT_IC_MARGIN,
        })
        if self.__am.add_account(account):
            logger.info(
                f"Root Account created:"
                f"\tID: {account.id}"
            )
            return account
        else:
            return None

    def create_invitation_code(self, a_id: AnyStr) -> Optional[InvitationCode]:
        ic = self.__am.create_ic(a_id)
        if ic:
            logger.info(
                f"InvitationCode Created"
                f"\tAccount: {ic.aid}"
                f"\tInvitationCode: {ic.id}"
            )
        return ic

    def create_ano_code(self, a_id: AnyStr) -> Optional[AnoCode]:
        ac = self.__am.create_ac(a_id)
        if ac:
            logger.info(
                f"AnoCode Created:"
                f"\tAccount: {ac.owner}"
                f"\tAnoCode: {ac.id}"
            )
        return ac

    def post_page(
            self,
            ac_id: AnyStr,
            content: AnyStr,
            group_name: AnyStr = gm.DEFAULT_ALL
    ) -> Optional[Page]:
        if not self.__acm.check_ac(ac_id):
            return None
        page = pm.create_page(ac_id, content)
        if page:
            if self.__gm.post_page_into_group(page.id, group_name):
                logger.info(
                    f"Page Created:"
                    f"\tAnoCode: {page.owner_ac}"
                    f"\tGroup: {group_name}"
                    f"\tPage: {page.id}"
                    f"\tContent: {content}"
                )
                return page
        return None

    def append_page(
            self,
            page_id: AnyStr,
            ac_id: AnyStr,
            content: AnyStr,
    ) -> Optional[Page]:
        page = self.__pm.append_content(page_id, ac_id, content)
        if page:
            logger.info(
                f"Page Appended:"
                f"\tPage: {page.id}"
                f"\tAnoCode: {ac_id}"
                f"\tContent: {content}"
            )
        return page

    def get_all_root_account(self) -> List[Account]:
        return self.__am.get_all_root_accounts()

    def get_admin_account(self) -> Optional[Account]:
        admin = self.__am.get_first_root_account()
        if not admin:
            admin = self.create_root_account()
        return admin

    def get_all_group(self) -> List[Group]:
        return self.__gm.get_all_group()

    def get_no_not_hidden(self) -> List[Group]:
        return self.__gm.get_no_not_hidden()

    def get_account_by_token(self, token_id: AnyStr) -> Optional[Account]:
        a_id = self.__tm.get_owner_id_by_token_id(token_id)
        if a_id:
            return self.__am.get_account(a_id)
        return None

    def get_page_with_floors(
            self,
            page_id: AnyStr,
            page_size: int = 50,
            page_index: int = 1,
    ) -> Optional[dict]:
        page = self.__pm.get_page(page_id)
        if not page:
            return None
        if page.hide:
            return None

        page_data = page.to_display_dict()
        if not page_data:
            return None
        page_data["floors_count"] = len(page_data.pop(Page.Keys.FLOOR_ID_LIST, []))

        floors = self.__pm.get_floors(page_id, page_size, page_index)
        page_data["floors"] = [
            floor.to_display_dict()
            for floor
            in floors
            if not floor.hide
        ]
        return page_data

    def get_group_with_pages(
            self,
            group_name: AnyStr,
            page_size: int = 50,
            page_index: int = 1,
    ) -> Optional[dict]:
        group = self.__gm.get_group_by_name(group_name)
        if not group:
            return None
        group_data = group.to_display_dict()
        if not group_data:
            return None
        group_data["pages_count"] = len(group_data.pop(Group.Keys.PAGE_ID_LIST, []))
        group_data["pages"] = self.__gm.get_pages(group_name, page_size, page_index)
        return group_data

    def show(self):
        self.__icm.show()
        print("---------")
        self.__am.show()
        print("---------")
        self.__acm.show()
        print("---------")
        self.__gm.show()
        print("---------")
        self.__pm.show()
        print("---------")
        self.__tm.show()
        print("---------")
        self.__fm.show()
