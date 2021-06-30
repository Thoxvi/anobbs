__all__ = [
    "CreateAnoCode"
]

from flask import request

from anobbs_core.lib import bbs_manager
from anobbs_http.base import (
    BaseResource,
    json_type_checker,
)


class CreateAnoCode(BaseResource):
    @json_type_checker({
        "token": ""
    })
    def post(self):
        ac = bbs_manager.create_ano_code_by_token(request.json["token"])
        if ac:
            return self.return_ok(ac.id)
        else:
            return self.return_error("Create anocode failed")
