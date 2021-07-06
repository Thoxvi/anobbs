__all__ = [
    "BaseDb",
    "BaseDbConnect",
    "DbError",
    "check_db_connect",
    "get_mongo_db_uri",
]

import copy
import hashlib
import logging
import time
from functools import wraps
from typing import List, Dict, AnyStr, Optional

import pymongo
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError, AutoReconnect

from anobbs_core.resources import (
    get_env as gv,
    MongoResource,
)
from .base_error import BaseError

logger = logging.getLogger(__name__)


class DbError(BaseError):
    pass


def get_mongo_db_uri():
    db = gv(MongoResource.MONGO_DB_NAME)
    mongo_username = gv(MongoResource.MONGO_INITDB_ROOT_USERNAME)
    mongo_passwd = gv(MongoResource.MONGO_INITDB_ROOT_PASSWORD)

    if not mongo_username and not mongo_passwd:
        mongo_uri = f'mongodb://{db}:27017/'
    else:
        mongo_uri = f'mongodb://{mongo_username}:{mongo_passwd}@{db}:27017/'
    return mongo_uri


def check_db_connect(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> func:
        while True:
            if not self.init_db_client():
                DbError.raise_error(f"Connect DB error")
                # logger.warning("Get DB error, may be the DB has not been started, will retry in 1s")
                # time.sleep(1)
            else:
                break
        try:
            return func(self, *args, **kwargs)
        except (PyMongoError, AutoReconnect) as err:
            DbError.raise_error(f"Other error: {err}")

    return wrapper


class BaseDb(object):
    __DB_DATABASE_NAME = "AnoBBS"
    __DB_PASSWORD_SALT = "V8OMDhoURNYHCiJZLE13DgQQesrLsuQ3"
    __INSTANCE = None
    __ID_KEY = "id"

    @staticmethod
    def __get_expand_keys(
            keys: dict = None,
            regex_keys: List[AnyStr] = None,
            range_keys: Dict[AnyStr, Dict[AnyStr, float]] = None,
    ):
        if keys is None:
            keys = {}
        keys = {k: v for k, v in keys.items() if k != ""}
        if regex_keys:
            for r_key in regex_keys:
                if r_key in keys:
                    keys[r_key] = {"$regex": keys[r_key]}
        if range_keys:
            for r_key in range_keys:
                range_value = range_keys[r_key]
                query_value = {
                    k: v
                    for k, v
                    in {
                        "$gt": range_value.get("min"),
                        "$lte": range_value.get("max"),
                    }.items()
                    if v
                }
                keys[r_key] = query_value
        return keys

    @check_db_connect
    def _get_collection(self):
        return self._db_client[self.__DB_DATABASE_NAME][self._table_name]

    def _sha256_and_add_salt_string(self, string: AnyStr) -> AnyStr:
        string_with_salt = string + self.__DB_PASSWORD_SALT
        sha256 = hashlib.sha256()
        sha256.update(string_with_salt.encode())
        return sha256.hexdigest()

    def _check_exists(self, data_id: AnyStr) -> bool:
        return BaseDb._get_collection(self).count_documents({self._id_key: data_id}) > 0

    def _insert(self, data: dict) -> bool:
        if data is None:
            return False
        return BaseDb._get_collection(self).insert_one(data).acknowledged

    def _update(self, data: dict) -> bool:
        try:
            data = copy.deepcopy(data)
            data_id = data[self._id_key]
            if BaseDb._get_collection(self).find({self._id_key: data_id}).count() > 0:
                BaseDb._get_collection(self).update_one({self._id_key: data_id}, {"$set": data})
            else:
                return self._insert(data)
            return True
        except KeyError:
            return False

    def _create_index(self, key: AnyStr, index_type: int) -> bool:
        if index_type not in [1, -1]:
            DbError.raise_error("Index type must be 1 or -1")
        return BaseDb._get_collection(self).create_index([(key, index_type)], background=True)

    def _drop_index(self, name: AnyStr) -> bool:
        return BaseDb._get_collection(self).drop_index(name)

    def _delete(self, data_id: AnyStr) -> bool:
        return BaseDb._get_collection(self).delete_one({self._id_key: data_id}).deleted_count == 1

    def _count(
            self,
            keys: dict = None,
            regex_keys: List[AnyStr] = None,
            range_keys: Dict[AnyStr, Dict[AnyStr, float]] = None,
    ) -> int:
        keys = self.__get_expand_keys(keys, regex_keys, range_keys)
        return BaseDb._get_collection(self).count(keys)

    def _update_many(self, objects: List[dict]) -> bool:
        if not isinstance(objects, list):
            return False
        if len(objects) == 0:
            return True
        operation_list = []

        for obj in objects:
            if not isinstance(obj, dict):
                continue
            oid = obj.get(self._id_key)
            if oid is None:
                continue
            operation_list.append(pymongo.UpdateOne({self._id_key: oid}, {"$set": obj}))

        return BaseDb._get_collection(self).bulk_write(operation_list).acknowledged

    def _query(
            self,
            keys: dict = None,
            select: Dict[AnyStr, bool] = None,
            sort_key: AnyStr = None,
            sort_rule: int = None,
            page_index: int = None,
            page_size: int = None,
    ) -> List[dict]:
        if keys is None:
            keys = {}
        keys = {k: v for k, v in keys.items() if k != ""}
        if select is None:
            select = {}
        select = {k: v for k, v in select.items() if k != ""}

        select["_id"] = False
        select = {k: (1 if v else 0) for k, v in select.items()}

        data = BaseDb._get_collection(self).find(keys, select)

        if sort_key:
            sort_rule = sort_rule or pymongo.DESCENDING
            data = data.sort(sort_key, sort_rule)
        if page_index and page_size is not None:
            data = data.skip((page_index - 1) * page_size).limit(page_size)

        return list(data)

    def _query_one(
            self,
            keys: dict = None,
            select: Dict[AnyStr, bool] = None
    ) -> Optional[dict]:
        data = self._query(keys, select)
        if len(data) > 0:
            return data[0]
        else:
            return None

    def _expand_query(
            self,
            keys: dict = None,
            regex_keys: List[AnyStr] = None,
            range_keys: Dict[AnyStr, Dict[AnyStr, float]] = None,
            **kwargs,
    ) -> List[dict]:
        keys = self.__get_expand_keys(keys, regex_keys, range_keys)
        return self._query(keys, **kwargs)

    def _remove_all(self) -> None:
        BaseDb._get_collection(self).drop()

    def __init__(
            self,
            uri: AnyStr,
            table_name: AnyStr,
            id_key: AnyStr = __ID_KEY,
    ):
        self._db_uri = uri
        self._db_client = None
        self._table_name = table_name
        self._id_key = id_key

    def init_db_client(self) -> bool:
        try:
            self._db_client = self._db_client or pymongo.MongoClient(self._db_uri, serverSelectionTimeoutMS=5)
            if self._db_client.server_info():
                return True
            else:
                self._db_client = None
        except (ServerSelectionTimeoutError, AutoReconnect) as err:
            logger.warning(err)
        return False


class BaseDbConnect(BaseDb):
    __DOC_NAME = "error"
    __ID_KEY = "id"

    def __init__(
            self,
            uri: AnyStr,
            doc_name: AnyStr = __DOC_NAME,
            id_key: AnyStr = __ID_KEY,
    ):
        super().__init__(uri, doc_name, id_key)

    def check_exists_by_id(self, data_id: AnyStr) -> bool:
        return self._check_exists(data_id)

    def insert(self, data) -> bool:
        return self._insert(data)

    def update(self, data) -> bool:
        return self._update(data)

    def delete(self, data_id: AnyStr) -> bool:
        return self._delete(data_id)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def update_many(self, objects: List[dict]) -> bool:
        return self._update_many(objects)

    def create_index(self, key, index_type):
        return self._create_index(key, index_type)

    def remove_all(self):
        return self._remove_all()

    def query(
            self,
            keys: dict = None,
            select: Dict[AnyStr, bool] = None,
            sort_key: AnyStr = None,
            sort_rule: int = None,
            page_index: int = None,
            page_size: int = None,
    ) -> List[dict]:
        return self._query(
            keys,
            select,
            sort_key,
            sort_rule,
            page_index,
            page_size,
        )

    def query_one(
            self,
            keys: dict = None,
            select: Dict[AnyStr, bool] = None
    ) -> Optional[dict]:
        return self._query_one(keys, select)

    def expand_query(
            self,
            keys: dict = None,
            regex_keys: List[AnyStr] = None,
            range_keys: Dict[AnyStr, Dict[AnyStr, float]] = None,
            **kwargs
    ) -> List[dict]:
        return self._expand_query(
            keys,
            regex_keys,
            range_keys,
            **kwargs,
        )
