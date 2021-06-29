__all__ = [
    "QueryGroupWithPages"
]

from flask import request

from anobbs_core.lib import bbs_manager
from anobbs_http.base import (
    BaseResource,
    json_type_checker
)


class QueryGroupWithPages(BaseResource):
    @json_type_checker({
        "group_name": "",
        # "page_size": 20,
        # "page_index": 1,
    })
    def post(self):
        group_name = request.json["group_name"]

        page_size = request.json.get("page_size", 20)
        page_index = request.json.get("page_index", 1)

        group_data = bbs_manager.get_group_with_pages(
            group_name,
            page_size,
            page_index,
        )

        if group_data is not None:
            return self.return_ok(group_data)
        else:
            return self.return_error(f"Group not found: {group_name}")
