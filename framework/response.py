import typing
import json
from urllib.parse import quote
from starlette.responses import Response, HTMLResponse, PlainTextResponse, JSONResponse, RedirectResponse, StreamingResponse, FileResponse
from starlette.background import BackgroundTask
from starlette.datastructures import URL


class HTML(Response):
    media_type = "text/html"


class Text(Response):
    media_type = "text/plain"


class JSON(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")


class Redirect(Response):
    def __init__(
        self,
        url: typing.Union[str, URL],
        status_code: int = 307,
        headers: dict = None,
        background: BackgroundTask = None,
    ) -> None:
        super().__init__(
            content=b"", status_code=status_code, headers=headers, background=background
        )
        self.headers["location"] = quote(str(url), safe=":/%#?=@[]!$&'()*+,;")
