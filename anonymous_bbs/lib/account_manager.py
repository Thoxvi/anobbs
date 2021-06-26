__all__ = [
    "AccountManager",
    "am",
]

from typing import AnyStr, List
from typing import Optional

from treelib import Tree

from anonymous_bbs.base import BaseDbConnect, get_mongo_db_uri
from anonymous_bbs.bean import Account, InvitationCode, AnoCode
from .ano_code_manager import acm
from .invitation_code_manager import icm


class AccountManager(BaseDbConnect):
    __TABLE_NAME = "account"

    def __make_account_tree(self) -> Tree:
        tree_root_id = "Account Tree"
        tree = Tree()
        tree.create_node(identifier=tree_root_id)
        for account in self._query(select={
            Account.Keys.ID: True,
            Account.Keys.INVITER_ID: True,
        }):
            tree.create_node(
                identifier=account.get(Account.Keys.ID),
                parent=account.get(Account.Keys.INVITER_ID) or tree_root_id,
            )
        return tree

    def __init__(self, uri: AnyStr):
        super().__init__(uri, self.__TABLE_NAME)

    def add_account(self, account: Account) -> bool:
        return self._update(account.to_dict())

    def get_account(self, a_id: AnyStr) -> Optional[Account]:
        data = self._query_one({self.ID_KEY: a_id})
        return Account.from_dict(data) if data else None

    def get_all_root_accounts(self) -> List[Account]:
        return [
            Account.from_dict(data)
            for data
            in self._query({Account.Keys.IS_ROOT: True})
        ]

    def create_ic(self, a_id: AnyStr) -> Optional[InvitationCode]:
        account = self.get_account(a_id)
        if not account:
            return None

        ic = account.create_ic()
        if ic:
            self._update(account.to_dict())
            icm.add_ic(ic)
        return ic

    def create_ac(self, a_id: AnyStr) -> Optional[AnoCode]:
        account = self.get_account(a_id)
        if not account:
            return None

        ac = account.create_ac()
        if ac:
            self._update(account.to_dict())
            acm.add_ac(ac)
        return ac

    def show(self):
        print(f"Account Info:")
        print(f"\tAll account number:\t{self._count()}")
        print(f"\tRoot account number:\t{self._count({Account.Keys.IS_ROOT: True})}")
        print(f"\tNormal account number:\t{self._count({Account.Keys.IS_ROOT: False})}")
        print(f"\tUnblock account number:\t{self._count({Account.Keys.IS_BLOCKED: False})}")
        print(f"\tblock account number:\t{self._count({Account.Keys.IS_BLOCKED: True})}")
        print()
        self.__make_account_tree().show()


am = AccountManager(get_mongo_db_uri())
