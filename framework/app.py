import typing
from pathlib import Path
from framework.registry import registry
from starlette.routing import Route

class App():
    routes:typing.List[Route] = []

    def __init__(self, path) -> None:
        _path = Path(path)
        self.id = _path.parent.name
        self.path = str(_path.absolute().parent) + '/'
        self.registry = registry
        self.registry['apps'][self.id] = self
    
    def route(
        self,
        path: str,
        methods: typing.List[str] = None,
        name: str = None,
        include_in_schema: bool = True,
    ) -> typing.Callable:
        def decorator(func: typing.Callable) -> typing.Callable:
            self.routes.append(Route(path, endpoint=func, methods=methods, name=name, include_in_schema=include_in_schema))
            return func

        return decorator

    def get_attribute(self, name):
        for route in self.routes:
            if route.endpoint.__name__ == name:
                return route.endpoint
