__all__ = [
    "AppendPage"
]

from flask import request

from anobbs_core.lib import bbs_manager
from anobbs_http.base import (
    BaseResource,
    json_type_checker,
)


class AppendPage(BaseResource):
    @json_type_checker({
        "page_id": "",
        "token": "",
        "ano_code": "",
        "content": "",
    })
    def post(self):
        params = {
            "page_id": request.json["page_id"],
            "token_id": request.json["token"],
            "ac_id": request.json["ano_code"],
            "content": request.json["content"][:1024],
        }
        page = bbs_manager.append_page(**params)
        if page:
            floor_id = page.floor_id_list[-1]
            floor = bbs_manager.get_floor(floor_id)
            return self.return_ok(floor.to_display_dict())
        else:
            return self.return_error("Append page failed")
