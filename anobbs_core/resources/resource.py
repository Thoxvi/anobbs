__all__ = [
    "get_env",
    "MongoResource",
]

import logging
import os

from anobbs_core.utils.type_utils import EnumType

logger = logging.getLogger(__name__)


class MongoResource(EnumType):
    MONGO_DB_NAME = "MONGO_DB_NAME"
    MONGO_INITDB_ROOT_USERNAME = "MONGO_INITDB_ROOT_USERNAME"
    MONGO_INITDB_ROOT_PASSWORD = "MONGO_INITDB_ROOT_PASSWORD"


class ResourceConstant(object):
    ENV_DEFAULT_VALUE_DICT = {
        MongoResource.MONGO_DB_NAME: "localhost",
        MongoResource.MONGO_INITDB_ROOT_USERNAME: "",
        MongoResource.MONGO_INITDB_ROOT_PASSWORD: "",
    }


def get_env(env_name: str, default=None) -> str:
    if default is None:
        default = ResourceConstant.ENV_DEFAULT_VALUE_DICT.get(env_name, "")
    logger.info("The {env} is {value}".format(env=env_name, value=os.getenv(env_name, default)))
    return os.getenv(env_name, default)
