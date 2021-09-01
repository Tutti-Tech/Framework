import typing
import inspect
import functools

from framework.request import Request

from starlette.concurrency import run_in_threadpool
from starlette.routing import BaseRoute, Router, Route, Mount
from starlette.types import ASGIApp, Receive, Scope, Send


class Route(Route):
    
    def __init__(self, path: str, endpoint: typing.Callable, *, methods: typing.List[str], name: str, include_in_schema: bool) -> None:
        super().__init__(path, endpoint, methods=methods, name=name, include_in_schema=include_in_schema)
        endpoint_handler = endpoint
        while isinstance(endpoint_handler, functools.partial):
            endpoint_handler = endpoint_handler.func
        if inspect.isfunction(endpoint_handler) or inspect.ismethod(endpoint_handler):
            # Endpoint is function or method. Treat it as `func(request) -> response`.
            self.app = request_response(endpoint)
            if methods is None:
                methods = ["GET"]
        else:
            # Endpoint is a class. Treat it as ASGI.
            self.app = endpoint


class BaseRoute(BaseRoute):
    pass


class Router(Router):
    pass


class Mount(Mount):
    pass


def request_response(func: typing.Callable) -> ASGIApp:
    """
    Takes a function or coroutine `func(request) -> response`,
    and returns an ASGI application.
    """
    is_coroutine = iscoroutinefunction_or_partial(func)

    async def app(scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope, receive=receive, send=send)
        if is_coroutine:
            response = await func(request)
        else:
            response = await run_in_threadpool(func, request)
        await response(scope, receive, send)

    return app

def iscoroutinefunction_or_partial(obj: typing.Any) -> bool:
    """
    Correctly determines if an object is a coroutine function,
    including those wrapped in functools.partial objects.
    """
    while isinstance(obj, functools.partial):
        obj = obj.func
    return inspect.iscoroutinefunction(obj)