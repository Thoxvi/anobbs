__all__ = [
    "QueryAccount"
]

from flask import request

from anobbs_core.lib import bbs_manager
from anobbs_http.base import (
    BaseResource,
    json_type_checker,
)


class QueryAccount(BaseResource):
    @json_type_checker({
        "token": ""
    })
    def post(self):
        token_id = request.json["token"]
        account_data = bbs_manager.get_display_account_by_token(token_id)
        if account_data is not None:
            return self.return_ok(account_data)
        else:
            return self.return_error("Token expired")
