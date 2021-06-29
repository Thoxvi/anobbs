__all__ = [
    "ConfigDbConnector",
    "config_db_connector",
]

from typing import AnyStr, Optional

from anobbs_core.base import BaseDbConnect, get_mongo_db_uri
from anobbs_core.utils.type_utils import EnumType


class ConfigDbConnector(BaseDbConnect):
    __TABLE_NAME = "config"
    __ID_KEY = "key"

    class Keys(EnumType):
        MAX_FLOOR_NUMBER = "max_floor_number"

    def __set(self, key: AnyStr, value) -> bool:
        return self._update({self._id_key: key, "value": value})

    def __get(self, key: AnyStr, default=None):
        data = self._query_one({self._id_key: key})
        if data:
            return data.get("value", default)
        else:
            return default

    def __init__(self, uri: AnyStr, id_key=__ID_KEY):
        super().__init__(uri, self.__TABLE_NAME, id_key)

    def get_new_floor_number(self) -> Optional[AnyStr]:
        def get_long_number(num: int, length: int = 10) -> AnyStr:
            num_str = str(num)
            return "0" * max(0, length - len(num_str)) + num_str

        no = self.__get(self.Keys.MAX_FLOOR_NUMBER, 0)
        if self.__set(self.Keys.MAX_FLOOR_NUMBER, no + 1):
            return get_long_number(no)
        return None

    def show(self):
        print(f"Config:")
        print("\n".join([
            f"\t{config.get(self._id_key)}: {config.get('value')}"
            for config
            in self._query()
        ]))


config_db_connector = ConfigDbConnector(get_mongo_db_uri())
