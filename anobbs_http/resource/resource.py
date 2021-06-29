__all__ = [
    "get_env",
    "FlaskAppResource",
]

import logging
import os

from anobbs_core.utils.type_utils import EnumType

logger = logging.getLogger(__name__)


class FlaskAppResource(EnumType):
    SECRET_KEY = "SECRET_KEY"


class ResourceConstant(object):
    ENV_DEFAULT_VALUE_DICT = {
        FlaskAppResource.SECRET_KEY: "HIdzXdB8Gs4uFZZlbqYoQuig7ILLI9hr"
    }


def get_env(env_name: str, default=None) -> str:
    if default is None:
        default = ResourceConstant.ENV_DEFAULT_VALUE_DICT.get(env_name, "")
    logger.info("The {env} is {value}".format(env=env_name, value=os.getenv(env_name, default)))
    return os.getenv(env_name, default)
