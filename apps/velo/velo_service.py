import os
import redis
import urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from werkzeug.formparser import parse_form_data
from jinja2 import Environment, FileSystemLoader

import VeloAPI
import pickle
import json


class VeloService(object):

    def __init__(self, config):
        self.redis = redis.Redis(config['redis_host'], config['redis_port'])
        self.velo_instances = {}

    def dispatch_request(self, request):
        data = json.loads(request.get_data())
        # self.redis.set(data['user'], data['password'])
        reply_string = self.redis.get(data['user'])
        return Response(reply_string)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(redis_host='127.0.0.1', redis_port=6379, with_static=True):
    app = VeloService({
        'redis_host':       redis_host,
        'redis_port':       redis_port
    })
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static')
        })
    return app


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('127.0.0.1', 8080, app, use_debugger=True, use_reloader=True)


# print requests.post('http://localhost:8080', data=json.dumps({'user':'acmetest4', 'password':'acmetest4'})).content
