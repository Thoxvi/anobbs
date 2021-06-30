__all__ = [
    "BlockAnoCodeByFloorNo"
]

from flask import request

from anobbs_core.lib import bbs_manager
from anobbs_http.base import (
    BaseResource,
    json_type_checker,
)


class BlockAnoCodeByFloorNo(BaseResource):
    @json_type_checker({
        "token": "",
        "floor_no": "",
    })
    def post(self):
        ac = bbs_manager.block_ano_code_by_floor_no(request.json["token"], request.json["floor_no"])
        if ac:
            return self.return_ok(ac)
        else:
            return self.return_error("Block Anocode failed")
