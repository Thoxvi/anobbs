__all__ = [
    "PageDbConnector",
    "page_db_connector",
]

from typing import Optional, AnyStr, List

from anobbs_core.base import BaseDbConnect, get_mongo_db_uri
from anobbs_core.bean import Page, Floor
from .floor import floor_db_connector


class PageDbConnector(BaseDbConnect):
    __TABLE_NAME = "page"

    def __init__(self, uri: AnyStr):
        super().__init__(uri, self.__TABLE_NAME)

    def get_page(self, pid: AnyStr) -> Optional[Page]:
        page = self._query_one({Page.Keys.ID: pid})
        if page:
            page = Page(**page)
        return page

    def get_floors(
            self, pid: AnyStr,
            page_size: int = 50,
            page_index: int = 1,
    ) -> List[Floor]:
        page = self.get_page(pid)
        if not page:
            return []

        if page_size <= 0 or page_index < 1:
            return []

        page_index -= 1
        floor_ids = page.floor_id_list[page_size * page_index:
                                       page_size * (page_index + 1)]

        return [
            Floor(**floor)
            for floor
            in floor_db_connector.query(
                {"$or": [
                    {
                        Floor.Keys.ID: fid,
                    }
                    for fid
                    in floor_ids
                ]},
                sort_key=Floor.Keys.CREATE_DATE,
                sort_rule=1,
            )
        ] if floor_ids else []

    def create_page(
            self,
            ac_id: AnyStr,
            content: AnyStr,
    ) -> Optional[Page]:
        floor = floor_db_connector.create_floor(ac_id, content)
        if floor:
            page = Page(**{
                Page.Keys.OWNER_AC: ac_id,
                Page.Keys.FIRST_FLOOR_ID: floor.id,
            })
            if self._update(page.to_dict()):
                return page
        return None

    def append_content(
            self,
            pid: AnyStr,
            ac_id: AnyStr,
            content: AnyStr,
    ) -> Optional[Page]:
        page = self.query_one({Page.Keys.ID: pid})
        if page:
            page = Page(**page)
            new_floor = floor_db_connector.create_floor(ac_id, content)
            if new_floor:
                page.add_floor(new_floor.id)
                if self._update(page.to_dict()):
                    return page

        return None

    def show(self):
        print(f"Page Info:")
        print(f"\tNumber of all Page:\t{self._count()}")
        print(f"\tNumber of not hidden Page:\t{self._count({Page.Keys.HIDE: False})}")
        print(f"\tNumber of hide Page:\t{self._count({Page.Keys.HIDE: True})}")


page_db_connector = PageDbConnector(get_mongo_db_uri())
