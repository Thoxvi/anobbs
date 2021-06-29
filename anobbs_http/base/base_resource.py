__all__ = [
    "BaseResource",
    "json_type_checker",
    "get_param_checker",
]

import binascii
import logging
import re
from functools import wraps

from flask import request
from flask_restful import Resource

from anobbs_http.utils.format_return_data import make_data
from anobbs_http.utils.type_utils import TypeChecker

logger = logging.getLogger(__name__)


def hump2underline(hunp_str: str) -> str:
    p = re.compile(r'([a-z]|\d)([A-Z])')
    sub = re.sub(p, r'\1_\2', hunp_str).lower()
    return sub


def json_exception_handler(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except TypeError as err:
            return self.return_error(str(err))
        except (KeyError, SyntaxError):
            return self.return_error("JSON format error")
        except binascii.Error:
            return self.return_error("Base64 error")

    return wrapper


@json_exception_handler
def json_type_checker(json_template):
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(self, *args, **kwargs):
            try:
                TypeChecker(json_template).check(request.json)
                return func(self, *args, **kwargs)
            except RuntimeError as err:
                return self.return_error(str(err))

        return inner_wrapper

    return wrapper


def get_param_checker(params_filed):
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(self, *args, **kwargs):
            try:
                for k in params_filed.keys():
                    params_filed[k] = "str"
                TypeChecker(params_filed).check(request.args)
                return func(self, *args, **kwargs)
            except RuntimeError as err:
                return self.return_error(str(err))

        return inner_wrapper

    return wrapper


class BaseResource(Resource):
    SESSION_TOKEN = "token"

    @classmethod
    def get_url(cls):
        return f"/{hump2underline(cls.__name__)}"

    @classmethod
    def get_register_addr(cls):
        return {
            cls.get_url(): ["GET", "POST", "PUT", "DELETE"]
        }

    @staticmethod
    def return_undone(data=None, header=None):
        logger.warning(f"This API is not yet complete: {request.path}")
        return BaseResource.return_data(code=2,
                                        msg="undone: This API is not yet complete",
                                        data=data,
                                        header=header)

    @staticmethod
    def return_ok(data=None, header=None, msg="ok"):
        return BaseResource.return_data(code=0,
                                        msg=msg,
                                        data=data,
                                        header=header)

    @staticmethod
    def return_error(msg, header=None):
        return BaseResource.return_data(code=1,
                                        msg=msg,
                                        header=header)

    @staticmethod
    def return_data(code=1,
                    msg="",
                    data=None,
                    header=None):
        ret_header = header or {}
        # return ret_data, ret_code, ret_header
        return make_data(
            code,
            msg,
            data
        ), 200, ret_header
