__all__ = [
    "BaseError"
]

import logging

logger = logging.getLogger(__name__)


class BaseError(Exception):
    @classmethod
    def raise_error(cls, msg: str) -> None:
        logger.error(msg)
        raise cls(msg)
