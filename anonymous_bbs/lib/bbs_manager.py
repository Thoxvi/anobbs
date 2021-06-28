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
    def init(self) -> bool:
        # 1. Create admin
        admin = self.get_admin_account()
        if not admin:
            logger.error("Create admin error")
            return False
        else:
            logger.info(f"Admin ID: {admin.id}")

    @staticmethod
    def login(a_id: AnyStr) -> Optional[Token]:
        return am.login(a_id)

    @staticmethod
    def get_owner_id_by_token_id(tid: AnyStr) -> Optional[AnyStr]:
        return tm.get_owner_id_by_token_id(tid)

    @staticmethod
    def create_account_by_ic(ic_id: AnyStr) -> Optional[Account]:
        if icm.is_ic_used(ic_id):
            return None

        bid = get_uuid()
        if not icm.use_ic(ic_id, bid):
            return None

        account = Account(**{
            Account.Keys.ID: bid,
            Account.Keys.INVITER_ID: icm.get_ic(ic_id).aid,
        })
        if am.add_account(account):
            logger.info(
                f"InvitationCode used:"
                f"\tIC: {ic_id}"
                f"\tInviter: {account.inviter_id}"
                f"\tAccount: {account.id}"
            )
            return account
        else:
            return None

    @staticmethod
    def create_root_account() -> Optional[Account]:
        account = Account(**{
            Account.Keys.MAX_ANO_SIZE: ROOT_MAX_ANO_SIZE,
            Account.Keys.IC_MARGIN: ROOT_IC_MARGIN,
        })
        if am.add_account(account):
            logger.info(
                f"Root Account created:"
                f"\tID: {account.id}"
            )
            return account
        else:
            return None

    @staticmethod
    def create_invitation_code(a_id: AnyStr) -> Optional[InvitationCode]:
        ic = am.create_ic(a_id)
        if ic:
            logger.info(
                f"InvitationCode Created"
                f"\tAccount: {ic.aid}"
                f"\tInvitationCode: {ic.id}"
            )
        return ic

    @staticmethod
    def create_ano_code(a_id: AnyStr) -> Optional[AnoCode]:
        ac = am.create_ac(a_id)
        if ac:
            logger.info(
                f"AnoCode Created:"
                f"\tAccount: {ac.owner}"
                f"\tAnoCode: {ac.id}"
            )
        return ac

    @staticmethod
    def post_page(
            ac_id: AnyStr,
            content: AnyStr,
            group_name: AnyStr = gm.DEFAULT_ALL
    ) -> Optional[Page]:
        if not acm.check_ac(ac_id):
            return None
        page = pm.create_page(ac_id, content)
        if page:
            if gm.post_page_into_group(page.id, group_name):
                logger.info(
                    f"Page Created:"
                    f"\tAnoCode: {page.owner_ac}"
                    f"\tGroup: {group_name}"
                    f"\tPage: {page.id}"
                    f"\tContent: {content}"
                )
                return page
        return None

    @staticmethod
    def append_page(
            page_id: AnyStr,
            ac_id: AnyStr,
            content: AnyStr,
    ) -> Optional[Page]:
        page = pm.append_content(page_id, ac_id, content)
        if page:
            logger.info(
                f"Page Appended:"
                f"\tPage: {page.id}"
                f"\tAnoCode: {ac_id}"
                f"\tContent: {content}"
            )
        return page

    @staticmethod
    def get_all_root_account() -> List[Account]:
        return am.get_all_root_accounts()

    def get_admin_account(self) -> Optional[Account]:
        admin = am.get_first_root_account()
        if not admin:
            admin = self.create_root_account()
        return admin

    @staticmethod
    def get_all_group() -> List[Group]:
        return gm.get_all_group()

    @staticmethod
    def get_no_not_hidden() -> List[Group]:
        return gm.get_no_not_hidden()

    @staticmethod
    def get_account_by_token(token_id: AnyStr) -> Optional[Account]:
        a_id = tm.get_owner_id_by_token_id(token_id)
        if a_id:
            return am.get_account(a_id)
        return None

    @staticmethod
    def get_page_with_floors(
            page_id: AnyStr,
            page_size: int = 50,
            page_index: int = 1,
    ) -> Optional[dict]:
        page = pm.get_page(page_id)
        if not page:
            return None
        if page.hide:
            return None

        page_data = page.to_display_dict()
        if not page_data:
            return None
        page_data["floors_count"] = len(page_data.pop(Page.Keys.FLOOR_ID_LIST, []))

        floors = pm.get_floors(page_id, page_size, page_index)
        page_data["floors"] = [
            floor.to_display_dict()
            for floor
            in floors
            if not floor.hide
        ]
        return page_data

    @staticmethod
    def get_group_with_pages(
            group_name: AnyStr,
            page_size: int = 50,
            page_index: int = 1,
    ) -> Optional[dict]:
        group = gm.get_group_by_name(group_name)
        if not group:
            return None
        group_data = group.to_display_dict()
        if not group_data:
            return None
        group_data["pages_count"] = len(group_data.pop(Group.Keys.PAGE_ID_LIST, []))
        group_data["pages"] = gm.get_pages(group_name, page_size, page_index)
        return group_data

    @staticmethod
    def show():
        icm.show()
        print("---------")
        am.show()
        print("---------")
        acm.show()
        print("---------")
        gm.show()
        print("---------")
        pm.show()
        print("---------")
        tm.show()
        print("---------")
        fm.show()
