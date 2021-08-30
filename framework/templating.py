from jinja2 import Environment, FileSystemLoader
from framework.response import html


class Templating():
    
    def __init__(self, directory: str = 'templates') -> None:
        self.env = self._create_env(directory)

    def _create_env(self, directory: str):
        return Environment(loader=FileSystemLoader(directory), autoescape=True)
    
    def __call__(self, template_name: str, context: dict) -> None:
        template = self.env.get_template(template_name)
        content = template.render(context)
        return html(content)
