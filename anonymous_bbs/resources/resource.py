__all__ = [
    "get_env",
    "MongoConstant",
]

import logging
import os

from anonymous_bbs.utils.type_utils import EnumType

logger = logging.getLogger(__name__)


class MongoConstant(EnumType):
    MONGO_DB_NAME = "MONGO_DB_NAME"
    MONGO_INITDB_ROOT_USERNAME = "MONGO_INITDB_ROOT_USERNAME"
    MONGO_INITDB_ROOT_PASSWORD = "MONGO_INITDB_ROOT_PASSWORD"


class ResourceConstant(object):
    ENV_DEFAULT_VALUE_DICT = {
        MongoConstant.MONGO_DB_NAME: "localhost",
        MongoConstant.MONGO_INITDB_ROOT_USERNAME: "",
        MongoConstant.MONGO_INITDB_ROOT_PASSWORD: "",
    }


def get_env(env_name: str, default=None) -> str:
    if default is None:
        default = ResourceConstant.ENV_DEFAULT_VALUE_DICT.get(env_name, "")
    logger.info("The {env} is {value}".format(env=env_name, value=os.getenv(env_name, default)))
    return os.getenv(env_name, default)
