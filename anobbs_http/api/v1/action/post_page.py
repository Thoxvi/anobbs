__all__ = [
    "PostPage"
]

from flask import request

from anobbs_core.lib import bbs_manager
from anobbs_http.base import (
    BaseResource,
    json_type_checker,
)


class PostPage(BaseResource):
    @json_type_checker({
        "token": "",
        "ano_code": "",
        "content": "",
        # "group_name": "",
    })
    def post(self):
        params = {
            "token_id": request.json["token"],
            "ac_id": request.json["ano_code"],
            "content": request.json["content"][:1024],
        }
        group_name = request.json.get("group_name")
        if group_name:
            params["group_name"] = group_name

        page = bbs_manager.post_page(**params)
        if page:
            return self.return_ok(page.id)
        else:
            return self.return_error("Post page failed")
