__all__ = [
    "PageManager",
    "pm",
]

from typing import Optional, AnyStr

from anonymous_bbs.base import BaseDbConnect, get_mongo_db_uri
from anonymous_bbs.bean import Page
from .floor_manager import fm


class PageManager(BaseDbConnect):
    __TABLE_NAME = "page"

    def __init__(self, uri: AnyStr):
        super().__init__(uri, self.__TABLE_NAME)

    def create_page(
            self,
            ac_id: AnyStr,
            content: AnyStr,
    ) -> Optional[Page]:
        floor = fm.create_floor(ac_id, content)
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
            new_floor = fm.create_floor(ac_id, content)
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


pm = PageManager(get_mongo_db_uri())
