__all__ = [
    "TokenDbConnector",
    "token_db_connector",
]

import time
from typing import AnyStr, Optional

from anobbs_core.base import BaseDbConnect, get_mongo_db_uri
from anobbs_core.bean import Token

DEFAULT_EXPIRE_TIME = 60 * 60 * 48


class TokenDbConnector(BaseDbConnect):
    __TABLE_NAME = "token"

    def __init__(self, uri: AnyStr):
        super().__init__(uri, self.__TABLE_NAME)

    def create_token(self, a_id: AnyStr) -> Optional[Token]:
        old_token_list = []
        for old_token in self._query({Token.Keys.OWNED_ACCOUNT_ID: a_id}):
            old_token[Token.Keys.EXPIRE_DATE] = 0
            old_token[Token.Keys.IS_EXPIRED] = True
            old_token_list.append(old_token)
        self.update_many(old_token_list)

        token = Token(**{
            Token.Keys.OWNED_ACCOUNT_ID: a_id,
            Token.Keys.EXPIRE_DATE: time.time() + DEFAULT_EXPIRE_TIME,
        })
        if self._update(token.to_dict()):
            return token
        else:
            return None

    def get_account_id_by_token_id(self, tid: AnyStr) -> Optional[AnyStr]:
        token = self.query_one({Token.Keys.ID: tid})
        if token:
            token = Token(**token)
            if not token.is_expired:
                return token.owned_account_id
            else:
                self._update(token.to_dict())
                return None

    def show(self):
        print(f"Token Info:")
        print(f"\tNumber of all Token:\t{self._count()}")
        print(f"\tNumber of expired Token:\t{self._count({Token.Keys.IS_EXPIRED: True})}")
        print(f"\tNumber of unexpired Token:\t{self._count({Token.Keys.IS_EXPIRED: False})}")


token_db_connector = TokenDbConnector(get_mongo_db_uri())
