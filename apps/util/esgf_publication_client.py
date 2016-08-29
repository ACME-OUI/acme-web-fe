"""
REST client for ESGF Publication Service

"""

import yaml
import json
import urllib
import httplib2


class IngestionClient(object):

    def __init__(self, config=None, config_file=None):
        """Athenticate to the Ingestion Service and establish an HTTPS session

        Parameters:

        @param config_file: A path to a YAML file with three parameters
                            server: <hostname>[:<port>]/ingestion
                            openid: <ESGF OpenID>
                            password: <ESGF password>
                            If config_file is not specified, the function reads config.

        @param config: A dictionary with three parameters:
                       {
                           'server': '<hostname>[:<port>]/ingestion',
                           'openid': '<openid>',
                           'password': '<password>'
                       }
        """

        if config_file is not None:
            with open(config_file, 'r') as cfg:
                self.config = yaml.load(cfg.read())
        elif config is not None:
            self.config = config
        else:
            raise ValueError('No configuration was specified')
        self.session_cookies = {}
        self.server = self.config['server']
        openid = self.config['openid']
        password = self.config['password']
        response, content = self._openid_password_login(openid, password)
        if response['status'] != '200':
            raise Exception(content['message'])

    def submit(self, params=None):
        path = '/workflow/create'
        return self._rest_request(path, http_method='POST', params=params)

    def scan(self, submission_id, params=None):
        path = '/workflow/%s/scan' % submission_id
        return self._rest_request(path, http_method='POST', params=params)

    def publish(self, submission_id, params=None):
        path = '/workflow/%s/publish' % submission_id
        return self._rest_request(path, http_method='POST', params=params)

    def get_status(self, submission_id):
        path = '/workflow/%s/status' % submission_id
        return self._rest_request(path)

    # Private functions
    def _openid_password_login(self, openid, password):
        path = '/auth'
        params = {'openid': openid, 'password': password}
        response, content = self._rest_request(path, http_method='POST', params=params)
        return response, content

    def _rest_request(self, path, http_method='GET',
                      content_type='application/json',
                      accept='application/json',
                      params=None,
                      use_session_cookies=True):

        http = httplib2.Http(disable_ssl_certificate_validation=True, timeout=10)

        url = 'https://' + self.server + path
        headers = {}
        headers['Content-Type'] = content_type
        headers['Accept'] = accept
        if use_session_cookies:
            if self.session_cookies:
                headers['Cookie'] = self.session_cookies
        if params:
            if content_type == 'application/x-www-form-urlencoded':
                body = urllib.urlencode(params)
            else:
                body = json.dumps(params)
        else:
            body = None
        response, content = http.request(url, http_method, headers=headers, body=body)
        if 'set-cookie' in response:
            self.session_cookies = response['set-cookie']
        if 'content-type' in response and 'application/json' in response['content-type'] and content != '':
            return response, json.loads(content)
        else:
            return response, {}
