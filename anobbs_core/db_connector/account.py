__all__ = [
    "AccountDbConnector",
    "account_db_connector",
]

from typing import AnyStr, List
from typing import Optional

from treelib import Tree

from anobbs_core.base import BaseDbConnect, get_mongo_db_uri
from anobbs_core.bean import Account, InvitationCode, AnoCode, Token
from anobbs_core.db_connector.ano_code import ano_code_db_connector
from anobbs_core.db_connector.invitation_code import invitation_code_db_connector
from anobbs_core.db_connector.token import token_db_connector


class AccountDbConnector(BaseDbConnect):
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
        data = self._query_one({self._id_key: a_id})
        return Account(**data) if data else None

    def get_all_root_accounts(self) -> List[Account]:
        return [
            Account(**data)
            for data
            in self._query({Account.Keys.IS_ROOT: True})
        ]

    def get_first_root_account(self) -> Optional[Account]:
        ac = self._query_one({Account.Keys.IS_ROOT: True})
        if ac:
            ac = Account(**ac)
        return ac

    def get_display_dict(self, a_id: AnyStr) -> Optional[dict]:
        account = self.get_account(a_id)
        if not account:
            return None
        data = account.to_display_dict()
        data["ac_list"] = [
            AnoCode(**ac_data).to_display_dict()
            for ac_data
            in ano_code_db_connector.query(
                {"$or": [
                    {AnoCode.Keys.ID: ac_id}
                    for ac_id
                    in data.pop(Account.Keys.AC_ID_LIST, [])
                ]
                },
                sort_key=AnoCode.Keys.CREATE_DATE,
                sort_rule=1,
            )
            if ac_data
        ]
        data["ic_list"] = [
            InvitationCode(**ic_data).to_display_dict()
            for ic_data
            in invitation_code_db_connector.query({InvitationCode.Keys.AID: a_id})
        ]
        return data

    def create_ic(self, a_id: AnyStr) -> Optional[InvitationCode]:
        account = self.get_account(a_id)
        if not account:
            return None

        ic = account.create_ic()
        if ic:
            self._update(account.to_dict())
            invitation_code_db_connector.add_ic(ic)
        return ic

    def create_ac(self, a_id: AnyStr) -> Optional[AnoCode]:
        account = self.get_account(a_id)
        if not account:
            return None

        ac = account.create_ac()
        if ac:
            self._update(account.to_dict())
            ano_code_db_connector.add_ac(ac)
        return ac

    def login(self, a_id: AnyStr) -> Optional[Token]:
        if self._count({Account.Keys.ID: a_id}) > 0:
            return token_db_connector.create_token(a_id)
        return None

    def show(self):
        print(f"Account Info:")
        print(f"\tNumber of all account:\t{self._count()}")
        print(f"\tNumber of root account:\t{self._count({Account.Keys.IS_ROOT: True})}")
        print(f"\tNumber of normal account:\t{self._count({Account.Keys.IS_ROOT: False})}")
        print(f"\tNumber of unblock account:\t{self._count({Account.Keys.IS_BLOCKED: False})}")
        print(f"\tNumber of block account:\t{self._count({Account.Keys.IS_BLOCKED: True})}")
        print()
        self.__make_account_tree().show()


account_db_connector = AccountDbConnector(get_mongo_db_uri())
