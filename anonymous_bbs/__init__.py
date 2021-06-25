__all__ = [
    "AppConstant"
]


class AppConstant(object):
    NAME = "Ano BBS"
    PACKAGE_NAME = NAME.lower().replace(" ", "_")
    UPPER_NAME = NAME.upper().replace(" ", "_")
    VERSION_TUPLE = (0, 0, 1)
    VERSION = '.'.join([str(i) for i in VERSION_TUPLE])
    AUTHOR_NAME = "Thoxvi"
    AUTHOR_EMAIL = "Thoxvi@Gmail.com"
    AUTHOR = "{AUTHOR_NAME} <{AUTHOR_EMAIL}>".format(AUTHOR_NAME=AUTHOR_NAME, AUTHOR_EMAIL=AUTHOR_EMAIL)
    DESC = "An anonymous bbs backend"
    URL = 'https://github.com/thoxvi/AnoBBS'
