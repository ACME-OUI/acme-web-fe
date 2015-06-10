from django.utils import unittest
from django.test.client import Client
import json


class credentialTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def save_credentials(self):
        client.login(username='testuser', password='testpass')

        new_credential = {
            'esgf': {
                'username': 'testuser',
                'password': 'testpass'
            }
        }

        response = client.post('add_credentials/')
