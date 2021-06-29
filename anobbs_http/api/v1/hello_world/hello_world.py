__all__ = [
    "HelloWorld"
]

from anobbs_http.base import (
    BaseResource,
)


class HelloWorld(BaseResource):
    def get(self):
        return self.return_ok("Hello world!")
