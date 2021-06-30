__all__ = [
    "GroupDbConnector",
    "group_db_connector",
]

from typing import Optional, AnyStr, List

from anobbs_core.base import BaseDbConnect, get_mongo_db_uri
from anobbs_core.bean import Group, Page, Floor
from .floor import floor_db_connector
from .page import page_db_connector


class GroupDbConnector(BaseDbConnect):
    __TABLE_NAME = "group"
    DEFAULT_ALL = "all"

    def __init__(self, uri: AnyStr):
        super().__init__(uri, self.__TABLE_NAME)

        if self._count({Group.Keys.NAME: self.DEFAULT_ALL}) == 0:
            self.create_new_group(self.DEFAULT_ALL)

    def check_exists_by_name(self, name: AnyStr) -> bool:
        return self._count({Group.Keys.NAME: name}) > 0

    def get_group_by_id(self, gid: AnyStr) -> Optional[Group]:
        group = self._query_one({Group.Keys.ID: gid})
        if group:
            group = Group(**group)
        return group

    def get_group_by_name(self, name: AnyStr) -> Optional[Group]:
        group = self._query_one({Group.Keys.NAME: name})
        if group:
            group = Group(**group)
        return group

    def create_new_group(self, name: AnyStr) -> Optional[Group]:
        group = self._query_one({Group.Keys.NAME: name})
        if group:
            return Group(**group)

        group_data = {
            Group.Keys.NAME: name
        }

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

    def get_all_group(self) -> List[Group]:
        return [
            Group(**group_data)
            for group_data
            in self._query(Group.Keys.CREATE_DATE)
        ]

    def get_not_hidden_group(self) -> List[Group]:
        return [
            Group(**group_data)
            for group_data
            in self._query({Group.Keys.HIDE: False})
        ]

    def get_pages(
            self,
            group_name: AnyStr,
            page_size: int = 50,
            page_index: int = 1,
    ) -> List[dict]:
        group = self.get_group_by_name(group_name)
        if not group:
            return []
        if group.hide:
            return []

        if page_size <= 0 or page_index < 1:
            return []
        page_index -= 1
        page_ids = group.page_id_list[page_size * page_index:
                                      page_size * (page_index + 1)]

        page_list = [
            Page(**page_data)
            for page_data
            in page_db_connector.query(
                {"$or": [
                    {
                        Page.Keys.ID: pid,
                        Page.Keys.HIDE: False
                    }
                    for pid
                    in page_ids
                ]},
                sort_key=Page.Keys.CREATE_DATE,
                sort_rule=-1,
            )
        ] if page_ids else []
        first_floor_list = [
            Floor(**floor)
            for floor
            in floor_db_connector.query(
                {"$or": [
                    {
                        Floor.Keys.ID: page.first_floor_id,
                        Floor.Keys.HIDE: False
                    }
                    for page
                    in page_list
                ]}
            )
        ] if page_list else []

        pages = []
        for i in range(len(first_floor_list)):
            page = page_list[i].to_display_dict()
            page.pop(Page.Keys.FLOOR_ID_LIST, [])
            page.pop(Page.Keys.FIRST_FLOOR_ID, "")
            page["first_floor"] = first_floor_list[i].to_display_dict()
            pages.append(page)

        return pages

    def show(self):
        print(f"Group Info:")
        print(f"\tNumber of all Group:\t{self._count()}")
        print(f"Groups:")
        print("\n".join([
            f"\t{group.get(Group.Keys.NAME)}"
            for group
            in self._query()
        ]))


group_db_connector = GroupDbConnector(get_mongo_db_uri())
