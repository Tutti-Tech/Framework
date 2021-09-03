import typing
from jinja2 import Environment, FileSystemLoader

from framework.request import Request
from framework.response import html


class Templating():
    
    def __init__(self, directory: str = 'templates', request: Request = None) -> None:
        self.env = self._create_env(directory)
        if request:
            self.env = self._create_request_env(request)

    def _create_env(self, directory: str):
        return Environment(loader=FileSystemLoader(directory), autoescape=True)
    
    def _create_request_env(self, request: Request):
        self.env.globals["base_url"] = request.base_url
        self.env.globals["app_url"] = request.app_url
        app_name = request.app_url.replace(str(request.base_url), '').rstrip('/')
        self.env.globals["app_name"] = app_name
        self.env.globals["static_url"] = request.url_for(app_name + '/static', path='/')
        self.env.globals["url_for"] = request.url_for
        return self.env
    
    def __call__(self, template_name: str, context: dict) -> None:
        template = self.env.get_template(template_name)
        content = template.render(context)
        # TODO hook here to generate static html page
        return html(content)
