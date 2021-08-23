import typing
import importlib
import os

from framework.registry import registry
from framework.config import Config
from framework.logging import logger

from starlette.datastructures import State, URLPath
from starlette.exceptions import ExceptionMiddleware
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.routing import BaseRoute, Router, Mount
from starlette.types import ASGIApp, Receive, Scope, Send


class Application():
    """
    Creates an application instance.
    """

    _instance = None

    def __new__(cls, debug: bool = False,
        routes: typing.Sequence[BaseRoute] = None,
        middleware: typing.Sequence[Middleware] = None,
        exception_handlers: typing.Dict[
            typing.Union[int, typing.Type[Exception]], typing.Callable
        ] = None,
        on_startup: typing.Sequence[typing.Callable] = None,
        on_shutdown: typing.Sequence[typing.Callable] = None,
        lifespan: typing.Callable[["Starlette"], typing.AsyncContextManager] = None,
        config: Config = None,):
        if not cls._instance:
            cls._instance = super(Application, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        debug: bool = False,
        routes: typing.Sequence[BaseRoute] = None,
        middleware: typing.Sequence[Middleware] = None,
        exception_handlers: typing.Dict[
            typing.Union[int, typing.Type[Exception]], typing.Callable
        ] = None,
        on_startup: typing.Sequence[typing.Callable] = None,
        on_shutdown: typing.Sequence[typing.Callable] = None,
        lifespan: typing.Callable[["Starlette"], typing.AsyncContextManager] = None,
        config: Config = None,
    ) -> None:
        
        # The lifespan context function is a newer style that replaces
        # on_startup / on_shutdown handlers. Use one or the other, not both.
        assert lifespan is None or (
            on_startup is None and on_shutdown is None
        ), "Use either 'lifespan' or 'on_startup'/'on_shutdown', not both."

        self._debug = debug
        self.state = State()
        
        #
        if config:
            self.config = config
            apps_path = config('APPS_PATH').split(';')
            routes = self.load_apps(apps_path)
        self.registry = registry

        self.router = Router(
            routes, on_startup=on_startup, on_shutdown=on_shutdown, lifespan=lifespan
        )
        self.exception_handlers = (
            {} if exception_handlers is None else dict(exception_handlers)
        )
        self.user_middleware = [] if middleware is None else list(middleware)
        self.middleware_stack = self.build_middleware_stack()
    
    #
    def load_apps(self, apps_path) -> typing.Sequence[BaseRoute]:
        routes = []
        for path in apps_path:
            if not path.endswith('/'): path += '/'
            if not os.path.isdir(path): continue
            app_list = os.listdir(path)
            for app_id in app_list:
                if not os.path.isfile(path + app_id + '/main.py'): continue
                try:
                    app_module = importlib.import_module(path[:-1] + '.' + app_id + '.main')
                    routes.append(Mount('/' + app_id, routes=app_module.app.routes))
                    logger.info("Module '" + path[:-1] + '.' + app_id + "' has been loaded.")
                except Exception as e:
                    logger.warn(e)
        return routes
    
    def config(self):
        return self.config

    def build_middleware_stack(self) -> ASGIApp:
        debug = self.debug
        error_handler = None
        exception_handlers = {}

        for key, value in self.exception_handlers.items():
            if key in (500, Exception):
                error_handler = value
            else:
                exception_handlers[key] = value

        middleware = (
            [Middleware(ServerErrorMiddleware, handler=error_handler, debug=debug)]
            + self.user_middleware
            + [
                Middleware(
                    ExceptionMiddleware, handlers=exception_handlers, debug=debug
                )
            ]
        )

        app = self.router
        for cls, options in reversed(middleware):
            app = cls(app=app, **options)
        return app

    @property
    def routes(self) -> typing.List[BaseRoute]:
        return self.router.routes

    @property
    def debug(self) -> bool:
        return self._debug

    @debug.setter
    def debug(self, value: bool) -> None:
        self._debug = value
        self.middleware_stack = self.build_middleware_stack()

    def url_path_for(self, name: str, **path_params: str) -> URLPath:
        return self.router.url_path_for(name, **path_params)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        scope["app"] = self
        await self.middleware_stack(scope, receive, send)

    # The following usages are now discouraged in favour of configuration
    #  during Starlette.__init__(...)
    def on_event(self, event_type: str) -> typing.Callable:
        return self.router.on_event(event_type)

    def mount(self, path: str, app: ASGIApp, name: str = None) -> None:
        self.router.mount(path, app=app, name=name)

    def host(self, host: str, app: ASGIApp, name: str = None) -> None:
        self.router.host(host, app=app, name=name)

    def add_middleware(self, middleware_class: type, **options: typing.Any) -> None:
        self.user_middleware.insert(0, Middleware(middleware_class, **options))
        self.middleware_stack = self.build_middleware_stack()

    def add_exception_handler(
        self,
        exc_class_or_status_code: typing.Union[int, typing.Type[Exception]],
        handler: typing.Callable,
    ) -> None:
        self.exception_handlers[exc_class_or_status_code] = handler
        self.middleware_stack = self.build_middleware_stack()

    def add_event_handler(self, event_type: str, func: typing.Callable) -> None:
        self.router.add_event_handler(event_type, func)

    def add_route(
        self,
        path: str,
        route: typing.Callable,
        methods: typing.List[str] = None,
        name: str = None,
        include_in_schema: bool = True,
    ) -> None:
        self.router.add_route(
            path, route, methods=methods, name=name, include_in_schema=include_in_schema
        )

    def add_websocket_route(
        self, path: str, route: typing.Callable, name: str = None
    ) -> None:
        self.router.add_websocket_route(path, route, name=name)

    def exception_handler(
        self, exc_class_or_status_code: typing.Union[int, typing.Type[Exception]]
    ) -> typing.Callable:
        def decorator(func: typing.Callable) -> typing.Callable:
            self.add_exception_handler(exc_class_or_status_code, func)
            return func

        return decorator

    def route(
        self,
        path: str,
        methods: typing.List[str] = None,
        name: str = None,
        include_in_schema: bool = True,
    ) -> typing.Callable:
        def decorator(func: typing.Callable) -> typing.Callable:
            self.router.add_route(
                path,
                func,
                methods=methods,
                name=name,
                include_in_schema=include_in_schema,
            )
            return func

        return decorator

    def websocket_route(self, path: str, name: str = None) -> typing.Callable:
        def decorator(func: typing.Callable) -> typing.Callable:
            self.router.add_websocket_route(path, func, name=name)
            return func

        return decorator

    def middleware(self, middleware_type: str) -> typing.Callable:
        assert (
            middleware_type == "http"
        ), 'Currently only middleware("http") is supported.'

        def decorator(func: typing.Callable) -> typing.Callable:
            self.add_middleware(BaseHTTPMiddleware, dispatch=func)
            return func

        return decorator

class App(Application):
    app_path = None
    def __init__(self, debug: bool, routes: typing.Sequence[BaseRoute], middleware: typing.Sequence[Middleware], exception_handlers: typing.Dict[typing.Union[int, typing.Type[Exception]], typing.Callable], on_startup: typing.Sequence[typing.Callable], on_shutdown: typing.Sequence[typing.Callable], lifespan: typing.Callable[["Starlette"], typing.AsyncContextManager], config: Config) -> None:
        super().__init__(debug=debug, routes=routes, middleware=middleware, exception_handlers=exception_handlers, on_startup=on_startup, on_shutdown=on_shutdown, lifespan=lifespan, config=config)
