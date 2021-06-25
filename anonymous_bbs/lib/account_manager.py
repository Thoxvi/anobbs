__all__ = [
    "AccountManager",
]

from treelib import Tree

from anonymous_bbs.bean import Account


class AccountManager:
    def __init__(self):
        self.__account_id_tree = Tree()

    def add_account(self, account: Account) -> bool:
        # TODO save the new account to db, and add this account into tree
        pass
