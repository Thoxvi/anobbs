__all__ = []

import logging
import pkgutil
import re
from string import ascii_uppercase

from flask import Blueprint
from flask_restful import Api

from anobbs_http.app import app
from anobbs_http.base.base_resource import BaseResource

logger = logging.getLogger(__name__)


def register_all_api_in_app():
    def add_resource(restful_api, resource_cls):
        register_addr_method_map = resource_cls.get_register_addr()

        for addr, methods in register_addr_method_map.items():
            endpoint = re.sub(r"[/:<>]", "_", addr).lower()
            methods = list(filter(lambda x: x.lower() in dir(resource_cls), methods))
            restful_api.add_resource(resource_cls, addr, methods=methods, endpoint=endpoint)
            logger.warning(
                f" * Register resource {resource_cls.__name__} {str(methods)}: {bp.url_prefix}{addr} endpoint={endpoint}"
            )

    for _, api_version, ispkg in pkgutil.iter_modules(__path__):
        if not ispkg:
            continue

        api = __import__(api_version, globals(), locals(), [], 1)

        bp = Blueprint(api_version, __name__, url_prefix=f"/api/{api_version}")
        restful = Api(bp)

        for cls_name in filter(lambda x: not x.startswith("__") and x[0] in ascii_uppercase, dir(api)):
            cls = getattr(api, cls_name)
            if not issubclass(cls, BaseResource):
                continue
            if cls == BaseResource:
                continue
            add_resource(restful, cls)

        app.register_blueprint(bp)


register_all_api_in_app()
