__all__ = [
    "make_data",
    "make_ok",
    "make_error",
]


def make_ok(data=None, msg="ok"):
    return make_data(
        code=0,
        msg=msg,
        data=data
    )


def make_error(msg):
    return make_data(
        code=1,
        msg=msg,
    )


def make_data(code=0,
              msg="",
              data=None):
    ret_data = {
        "code": code,
        "msg": msg,
    }
    if data is not None:
        ret_data["data"] = data
    return ret_data
