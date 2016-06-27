from django.test import LiveServerTestCase
import unittest
import json
import requests
from constants import NODE_HOSTNAMES

class ESGFTestLogon(LiveServerTestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.username = 'https://pcmdi.llnl.gov/esgf-idp/openid/acmetest'
        self.password = 'ACM#t3st'

    def test_logon_success(self):
        credential = json.dumps({
            'username': self.username,
            'password': self.password
        })
        response_code = requests.get(self.live_server_url + '/acme/esgf/logon/', data=credential).status_code
        self.assertTrue( response_code == requests.codes.ok)

    def test_logon_fail(self):
        credential = json.dumps({
            'username': 'abra',
            'password': 'cadabra'
        })
        response_code = requests.get(self.live_server_url + '/acme/esgf/logon/', data=credential).status_code
        self.assertFalse( response_code == requests.codes.ok)

class ESGFTestLoadFacet(LiveServerTestCase):

    def test_load_facet(self):
        nodes = json.dumps({
            'nodes': NODE_HOSTNAMES
        })
        response = requests.get(self.live_server_url + '/acme/esgf/load_facets/', data=nodes)
        self.assertTrue( response.status_code == requests.codes.ok )

class ESGFTestNodeSearch(LiveServerTestCase):

    def test_node_search(self):
        request = json.dumps({
            'nodes': NODE_HOSTNAMES,
            'terms': {
                'project': 'ACME',
                'Versionnum': 'v0_3'
            }
        })
        response = requests.get(self.live_server_url + '/acme/esgf/node_search/', data=request)
        print response.content
        self.assertTrue( response.status_code == requests.codes.ok )
