__all__ = [
    "app"
]

from flask import Flask
from flask_cors import CORS

from anobbs_http.resource import (
    get_env as gv,
    FlaskAppResource,
)

app = Flask("anobbs_http")
app.secret_key = gv(FlaskAppResource.SECRET_KEY)
app.config.update({
    # "SESSION_COOKIE_SECURE": True,
    "SESSION_COOKIE_HTTPONLY": False,
    "SESSION_COOKIE_SAMESITE": "Lax",
})
CORS(app, supports_credentials=True)
