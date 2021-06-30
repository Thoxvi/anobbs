__all__ = [
    "CreateInvitationCode"
]

from flask import request

from anobbs_core.lib import bbs_manager
from anobbs_http.base import (
    BaseResource,
    json_type_checker,
)


class CreateInvitationCode(BaseResource):
    @json_type_checker({
        "token": ""
    })
    def post(self):
        ic = bbs_manager.create_invitation_code_by_token(request.json["token"])
        if ic:
            return self.return_ok(ic.id)
        else:
            return self.return_error("Create invitation code failed")
