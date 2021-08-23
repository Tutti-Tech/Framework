import sys
sys.path.append("..")

from framework.application import Application
from framework.response import Text

app = Application()

@app.route('/')
def home(request):
    response = Text('Home Page')
    return response

@app.route('/hello/{username}')
def hello(request):
    return Text('Hello, %s' % request.path_params['username'])