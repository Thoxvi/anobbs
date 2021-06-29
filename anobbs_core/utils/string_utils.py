__all__ = [
    "get_random_string",
]

import random
import string


def get_random_string(size=32, with_lower=True, with_number=True, with_upper=True, with_sign=False):
    chars = ""
    if with_lower:
        chars += string.ascii_lowercase
    if with_upper:
        chars += string.ascii_uppercase
    if with_number:
        chars += string.digits
    if with_sign:
        chars += string.punctuation

    return ''.join(random.choice(chars) for _ in range(size))
