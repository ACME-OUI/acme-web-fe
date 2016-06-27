from django.test import LiveServerTestCase
import unittest
import json
import requests


class ESGFTestCase(LiveServerTestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.username = 'https://pcmdi.llnl.gov/esgf-idp/openid/acmetest'
        self.password = 'ACM#t3st'

    def test_logon(self):
        credential = json.dumps({
            'username': self.username,
            'password': self.password
        })
        response_code = requests.get(self.live_server_url, data=credential).status_code
        self.assertTrue( response_code == requests.codes.ok)
