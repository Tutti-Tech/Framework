import typing
from pathlib import Path

from framework.config import Config
from framework.registry import registry
from framework.routing import Route, Mount

from starlette.staticfiles import StaticFiles


class App():

    def __init__(self, path) -> None:
        _path = Path(path)
        self.id = _path.parent.name
        self.path = str(_path.absolute().parent) + '/'
        self.routes: typing.List[Route] = []
        self.routes.append(Mount('/static', app=StaticFiles(directory=self.path+'static', check_dir=False), name=self.id+'/static'))
        self.config = Config('.config')
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
            # The type of route may be Mount or Route 
            if 'endpoint' in route.__dict__ and route.endpoint.__name__ == name:
                return route.endpoint
