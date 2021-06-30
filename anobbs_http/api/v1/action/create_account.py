__all__ = [
    "CreateAccount"
]

from flask import request

from anobbs_core.lib import bbs_manager
from anobbs_http.base import (
    BaseResource,
    json_type_checker,
)


class CreateAccount(BaseResource):
    @json_type_checker({
        "invitation_code": ""
    })
    def post(self):
        account = bbs_manager.create_account_by_ic(request.json["invitation_code"])
        if account:
            bbs_manager.create_ano_code_by_account(account.id)
            return self.return_ok(account.id)
        else:
            return self.return_error("Create account failed")
