from starlette.requests import Request
from starlette.datastructures import URL

class Request(Request):
    @property
    def app_url(self):
        if not hasattr(self, "_app_url"):
            app_url_scope = dict(self.scope)
            app_url_scope["path"] = "/"
            app_url_scope["query_string"] = b""
            self._app_url = URL(scope=app_url_scope)
        return self._app_url._url
