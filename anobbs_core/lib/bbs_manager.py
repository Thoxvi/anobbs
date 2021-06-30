__all__ = [
    "BbsManager",
    "bbs_manager",
]

import logging
import time
from typing import List, Optional, AnyStr

from anobbs_core.bean import Account, InvitationCode, AnoCode, Page, Group, Token, Floor
from anobbs_core.db_connector import (
    account_db_connector,
    ano_code_db_connector,
    floor_db_connector,
    group_db_connector,
    invitation_code_db_connector,
    page_db_connector,
    token_db_connector,
    config_db_connector,
)
from anobbs_core.utils.id_utils import get_uuid

ROOT_MAX_ANO_SIZE = 2 ** 10
ROOT_IC_MARGIN = 2 ** 10
MIN_CREATE_IC_TIME = 6 * 60 * 60

logger = logging.getLogger("AnoBBS")


class BbsManager:
    def __init__(self):
        # 1. Create admin
        admin = self.get_admin_account()
        if not admin:
            logger.error("Create admin error")
        else:
            logger.warning(f"-------------------")
            logger.warning(f"AnoBBS Manager inited")
            logger.warning(f"\tAdmin ID: {admin.id}")
            logger.warning(f"-------------------")

    @staticmethod
    def __check_token_is_admin(token_id: AnyStr) -> bool:
        account_id = BbsManager.get_account_id_by_token(token_id)
        admin = BbsManager.get_admin_account()
        return admin and account_id and admin.id == account_id

    @staticmethod
    def __check_ano_code_use_token(ano_code_id: AnyStr, token_id: AnyStr) -> bool:
        account = BbsManager.get_account_by_token(token_id)
        return account and ano_code_id in account.ac_id_list

    @staticmethod
    def login(account_id: AnyStr) -> Optional[Token]:
        return account_db_connector.login(account_id)

    @staticmethod
    def create_account_by_ic(invitation_code_id: AnyStr) -> Optional[Account]:
        if invitation_code_db_connector.is_ic_used(invitation_code_id):
            return None

        bid = get_uuid()
        if not invitation_code_db_connector.use_ic(invitation_code_id, bid):
            return None

        account = Account(**{
            Account.Keys.ID: bid,
            Account.Keys.INVITER_ID: invitation_code_db_connector.get_ic(invitation_code_id).aid,
        })
        if account_db_connector.add_account(account):
            logger.info(
                f"InvitationCode used:"
                f"\tIC: {invitation_code_id}"
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
        if account_db_connector.add_account(account):
            logger.info(
                f"Root Account created:"
                f"\tID: {account.id}"
            )
            return account
        else:
            return None

    @staticmethod
    def create_invitation_code_by_token(token_id: AnyStr) -> Optional[InvitationCode]:
        account_id = BbsManager.get_account_id_by_token(token_id)
        if account_id:
            return BbsManager.create_invitation_code_by_account(account_id)
        return None

    @staticmethod
    def create_invitation_code_by_account(account_id: AnyStr) -> Optional[InvitationCode]:
        account = account_db_connector.get_account(account_id)
        if not account.is_root and time.time() - account.create_date < MIN_CREATE_IC_TIME:
            return None
        ic = account_db_connector.create_ic(account_id)
        if ic:
            logger.info(
                f"InvitationCode Created"
                f"\tAccount: {ic.aid}"
                f"\tInvitationCode: {ic.id}"
            )
        return ic

    @staticmethod
    def create_ano_code_by_token(token_id: AnyStr) -> Optional[AnoCode]:
        account_id = BbsManager.get_account_id_by_token(token_id)
        if account_id:
            return BbsManager.create_ano_code_by_account(account_id)
        return None

    @staticmethod
    def create_ano_code_by_account(account_id: AnyStr) -> Optional[AnoCode]:
        ac = account_db_connector.create_ac(account_id)
        if ac:
            logger.info(
                f"AnoCode Created:"
                f"\tAccount: {ac.owner}"
                f"\tAnoCode: {ac.id}"
            )
        return ac

    @staticmethod
    def post_page(
            token_id: AnyStr,
            ac_id: AnyStr,
            content: AnyStr,
            group_name: AnyStr = group_db_connector.DEFAULT_ALL
    ) -> Optional[Page]:
        if not BbsManager.__check_ano_code_use_token(ac_id, token_id):
            return None
        if not (group_db_connector.check_exists_by_name(group_name) or BbsManager.__check_token_is_admin(token_id)):
            return None
        page = page_db_connector.create_page(ac_id, content)
        if page:
            if group_db_connector.post_page_into_group(page.id, group_name):
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
            token_id: AnyStr,
            ac_id: AnyStr,
            content: AnyStr,
    ) -> Optional[Page]:
        if not BbsManager.__check_ano_code_use_token(ac_id, token_id):
            return None
        page = page_db_connector.append_content(page_id, ac_id, content)
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
        return account_db_connector.get_all_root_accounts()

    @staticmethod
    def get_admin_account() -> Optional[Account]:
        admin = account_db_connector.get_first_root_account()
        if not admin:
            admin = BbsManager.create_root_account()
        return admin

    @staticmethod
    def get_all_group() -> List[Group]:
        return group_db_connector.get_all_group()

    @staticmethod
    def get_not_hidden_group() -> List[Group]:
        return group_db_connector.get_not_hidden_group()

    @staticmethod
    def get_account_id_by_token(token_id: AnyStr) -> Optional[AnyStr]:
        return token_db_connector.get_account_id_by_token_id(token_id)

    @staticmethod
    def get_floor(floor_id: AnyStr) -> Optional[Floor]:
        return floor_db_connector.get_floor(floor_id)

    @staticmethod
    def get_account_by_token(token_id: AnyStr) -> Optional[Account]:
        a_id = token_db_connector.get_account_id_by_token_id(token_id)
        if a_id:
            return account_db_connector.get_account(a_id)
        return None

    @staticmethod
    def get_page_with_floors(
            page_id: AnyStr,
            page_size: int = 50,
            page_index: int = 1,
    ) -> Optional[dict]:
        page = page_db_connector.get_page(page_id)
        if not page:
            return None
        if page.hide:
            return None

        page_data = page.to_display_dict()
        if not page_data:
            return None
        page_data["floors_count"] = len(page_data.pop(Page.Keys.FLOOR_ID_LIST, []))

        floors = page_db_connector.get_floors(page_id, page_size, page_index)
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
        group = group_db_connector.get_group_by_name(group_name)
        if not group:
            return None
        group_data = group.to_display_dict()
        if not group_data:
            return None
        group_data["pages_count"] = len(group_data.pop(Group.Keys.PAGE_ID_LIST, []))
        group_data["pages"] = group_db_connector.get_pages(group_name, page_size, page_index)
        return group_data

    @staticmethod
    def get_display_account_by_account(account_id: AnyStr) -> Optional[dict]:
        return account_db_connector.get_display_dict(account_id)

    @staticmethod
    def get_display_account_by_token(token_id: AnyStr) -> Optional[dict]:
        account_id = BbsManager.get_account_id_by_token(token_id)
        if account_id:
            return account_db_connector.get_display_dict(account_id)
        return None

    @staticmethod
    def get_account_tree_by_token(token_id: AnyStr) -> Optional[AnyStr]:
        if BbsManager.__check_token_is_admin(token_id):
            return account_db_connector.get_account_tree()
        return None

    @staticmethod
    def block_ano_code_by_floor_no(token_id: AnyStr, floor_no: AnyStr) -> Optional[AnyStr]:
        if not BbsManager.__check_token_is_admin(token_id):
            return None
        floor = floor_db_connector.query_one({Floor.Keys.NO: floor_no})
        if not floor:
            return None
        floor = Floor(**floor)
        if ano_code_db_connector.block_ac(floor.owner_ac):
            return floor.owner_ac
        else:
            return None

    @staticmethod
    def block_ano_code(token_id: AnyStr, ano_code: AnyStr) -> bool:
        if not BbsManager.__check_token_is_admin(token_id):
            return False
        return ano_code_db_connector.block_ac(ano_code.owner_ac)

    @staticmethod
    def show():
        invitation_code_db_connector.show()
        print("---------")
        account_db_connector.show()
        print("---------")
        ano_code_db_connector.show()
        print("---------")
        group_db_connector.show()
        print("---------")
        page_db_connector.show()
        print("---------")
        token_db_connector.show()
        print("---------")
        floor_db_connector.show()
        print("---------")
        config_db_connector.show()


bbs_manager = BbsManager()
