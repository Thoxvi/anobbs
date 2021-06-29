__all__ = [
    "get_uuid",
]

from random import randint

from .string_utils import get_random_string


def get_uuid() -> str:
    return str(get_random_string(randint(32, 64)))
