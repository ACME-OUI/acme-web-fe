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

    def dispatch_request(self, request):
        data = json.loads(request.get_data())
        if data['command'] != 'init':
            v_str = self.redis.get(data['velo_user'])
            v = pickle.loads(v_str)
            return Response(self.commands[data['command']](data, v))
        else:
            return Response(self.commands[data['command']](data))

    def init_velo(self, data):
        v = VeloAPI.Velo()
        v.start_jvm()
        reply_string = v.init_velo(data['velo_user'], data['velo_pass'])
        v_str = pickle.dumps(v)
        self.redis.set(data['velo_user'], v_str)
        return reply_string

    def get_folder(self, data, velo):
        return velo.get_resources(data['folder'])

    def create_folder(self, data, velo):
        return velo.create_folder(data['foldername'])

    def save_file(self, data, velo):
        return velo.upload_file(data['remote_path'], data['local_path'], data['filename'])

    def get_file(self, data, velo):
        if velo.download_file(data['remote_path'], data['local_path'] == 0):
            return open(os.path.join(data['local_path'], data['filename'])).read()
        else:
            return 'Failed to download file'

    def delete(self, data, velo):
        return velo.delete_resource(data['resource'])

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def __init__(self, config):
        self.redis = redis.Redis(config['redis_host'], config['redis_port'])
        self.commands = {
            'init': self.init_velo,
            'get_folder': self.get_folder,
            'create_folder': self.create_folder,
            'save_file': self.save_file,
            'get_file': self.get_file,
            'delete': self.delete
        }


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
