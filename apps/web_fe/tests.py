from django.utils import unittest
from django.test.client import Client
import json


class CredentialTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        client.login(username='testuser', password='testpass')

    def save_credentials(self):

        new_credential = {
            'esgf': {
                'username': 'testuser',
                'password': 'testpass'
            }
        }

        response = client.post('add_credentials/', json.dumps(new_credential))
        self.assertEquals(response.status_code, 200)


class GridTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        client.login(username='testuser', password='testpass')

    def load_grid(self):
        response = client.get('grid/')
        self.assertEquals(response.status_code, 200)
