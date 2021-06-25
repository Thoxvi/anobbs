__all__ = [
    "AccountManager",
]

from typing import Optional

from treelib import Tree

from anonymous_bbs.bean import Account


class AccountManager:
    def __init__(self):
        self.__account_id_tree = Tree()

    def add_account(self, account: Account) -> bool:
        # TODO save the new account to db, and add this account into tree
        pass

    def get_account(self, aid: str) -> Optional[Account]:
        if self.__account_id_tree.contains(aid):
            # TODO read account from db
            return None
        else:
            return None
