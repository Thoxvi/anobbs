__all__ = [
    "QueryPageWithFloors"
]

from flask import request

from anobbs_core.lib import bbs_manager
from anobbs_http.base import (
    BaseResource,
    json_type_checker
)


class QueryPageWithFloors(BaseResource):
    @json_type_checker({
        "page_id": "",
        # "page_size": 50,
        # "page_index": 1,
    })
    def post(self):
        page_id = request.json["page_id"]

        page_size = request.json.get("page_size", 50)
        page_index = request.json.get("page_index", 1)

        group_data = bbs_manager.get_page_with_floors(
            page_id,
            page_size,
            page_index,
        )

        if group_data is not None:
            return self.return_ok(group_data)
        else:
            return self.return_error(f"Page not found: {page_id}")
