__all__ = [
    "EnumType"
]


class EnumType:
    @classmethod
    def get_list(cls):
        return [
            getattr(cls, attr)
            for attr
            in dir(cls)
            if not attr.startswith("__") and attr != "get_list"
        ]
