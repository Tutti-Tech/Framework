import sys
sys.path.append("..")

from framework.application import Application
from framework.response import text, html

app = Application()

@app.route('/')
def home(request):
    return text('Home Page')

@app.route('/hello/{username}')
def hello(request):
    return html('Hello, <strong>%s</strong>' % request.path_params['username'])