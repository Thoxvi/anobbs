__all__ = [
    "get_env",
]

import logging
import os

logger = logging.getLogger(__name__)


class ResourceConstant(object):
    ENV_DEFAULT_VALUE_DICT = {}


def get_env(env_name: str, default=None) -> str:
    if default is None:
        default = ResourceConstant.ENV_DEFAULT_VALUE_DICT.get(env_name, "")
    logger.info("The {env} is {value}".format(env=env_name, value=os.getenv(env_name, default)))
    return os.getenv(env_name, default)
