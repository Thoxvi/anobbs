__all__ = [
    "GroupList"
]

from anobbs_core.lib import bbs_manager
from anobbs_http.base import (
    BaseResource,
)


class GroupList(BaseResource):
    def get(self):
        return self.return_ok([
            group.name
            for group
            in bbs_manager.get_not_hidden_group()
        ])
