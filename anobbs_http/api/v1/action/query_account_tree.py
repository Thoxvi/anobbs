__all__ = [
    "QueryAccountTree"
]

from flask import request

from anobbs_core.lib import bbs_manager
from anobbs_http.base import (
    BaseResource,
    json_type_checker,
)


class QueryAccountTree(BaseResource):
    @json_type_checker({
        "token": "",
    })
    def post(self):
        tree = bbs_manager.get_account_tree_by_token(request.json["token"])
        if tree:
            return self.return_ok(tree)
        else:
            return self.return_error("Inadequate authority")
