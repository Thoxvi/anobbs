__all__ = [
    "Login"
]

from flask import request

from anobbs_core.lib import bbs_manager
from anobbs_http.base import (
    BaseResource,
    json_type_checker,
)


class Login(BaseResource):
    @json_type_checker({
        "account_id": ""
    })
    def post(self):
        token = bbs_manager.login(request.json["account_id"])
        if token:
            return self.return_ok(token.id)
        else:
            return self.return_error("Login failed")
