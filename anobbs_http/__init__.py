__all__ = [
    "create_app",
]

import logging

from .api import *
from .app import app

logger = logging.getLogger(__name__)


class HttpLoggerFilter(logging.Filter):
    def filter(self, record) -> bool:
        if record.msg.lower().find(r"/robot_status") != -1:
            return False
        if record.msg.lower().find(r"/robot_info_list") != -1:
            return False
        if record.msg.lower().find(r"/socket.io/") != -1:
            return False
        if record.msg.lower().find(r"Closing connection.") != -1:
            return False
        return True


def init_logger():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s: %(message)s')
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.addFilter(HttpLoggerFilter())
    for logger_name in []:
        shutup_logger = logging.getLogger(logger_name)
        shutup_logger.setLevel(logging.WARNING)
    logger.info("Init logging success")


def create_app(config=None):
    init_logger()
    if config is None:
        config = {}
    app.config.update(config)
    return app
