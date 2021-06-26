__all__ = [
    "GroupManager",
    "gm",
]

from typing import Optional, AnyStr

from anonymous_bbs.base import BaseDbConnect, get_mongo_db_uri
from anonymous_bbs.bean import Group


class GroupManager(BaseDbConnect):
    __TABLE_NAME = "group"
    DEFAULT_ALL = "all"

    def __init__(self, uri: AnyStr):
        super().__init__(uri, self.__TABLE_NAME)

        if self._count({Group.Keys.NAME: self.DEFAULT_ALL}) == 0:
            self.create_new_group(self.DEFAULT_ALL)

    def create_new_group(self, name: AnyStr, gid: Optional[AnyStr] = None) -> Optional[Group]:
        group = self._query_one({Group.Keys.NAME: name})
        if group:
            return Group(**group)

        group_data = {
            Group.Keys.NAME: name
        }
        if gid:
            group_data[Group.Keys.ID] = gid
        group = Group(**group_data)
        if self._update(group.to_dict()):
            return group
        else:
            return None

    def post_page_into_group(self, page_id: AnyStr, name: AnyStr = DEFAULT_ALL) -> bool:
        group = self.create_new_group(name)
        if not group:
            return False
        group.add_page(page_id)
        return self._update(group.to_dict())

    def show(self):
        print(f"Group Info:")
        print(f"\tAll Group number:\t{self._count()}")
        print(f"Groups:")
        print("\n".join([
            f"\t{group.get(Group.Keys.NAME)}"
            for group
            in self._query()
        ]))


gm = GroupManager(get_mongo_db_uri())
