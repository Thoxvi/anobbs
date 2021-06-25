__all__ = [
    "get_uuid",
]

from .string_utils import get_random_string


def get_uuid() -> str:
    return str(get_random_string(128))
