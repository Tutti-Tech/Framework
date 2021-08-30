import sys
sys.path.append("..")

from framework.application import Application
from framework.request import Request
from framework.response import text, html

app = Application()

@app.route('/')
def home(request):
    return text('Home Page')

@app.route('/hello/{username}')
def hello(request: Request):
    return html('Hello, <strong>%s</strong> <br> Your IP: %s ' % (request.path_params['username'], request.client.host))