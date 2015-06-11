from django.utils import unittest
from django.test.client import Client
import json
from django.contrib.auth.models import User


class CredentialTest(unittest.TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            'testuser', 'test@test.test', 'testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def tearDown(self):
        User.objects.filter(username='testuser').delete()

    def test_save_credentials(self):
        credentials = {}
        credentials['esgf'] = {}
        credentials['esgf']['username'] = 'testuser'
        credentials['esgf']['password'] = 'testpass'

        data = json.dumps(credentials)
        response = self.client.post('/acme/add_credentials/', content_type='application/json', data=data)
        self.assertEquals(response.status_code, 200)


class GridTest(unittest.TestCase):

    def setUp(self):
        # First create a new user
        self.test_user = User.objects.create_user(
            'testuser', 'test@test.test', 'testpass')
        # Now login as that user
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def tearDown(self):
        User.objects.filter(username='testuser').delete()

    def test_load_grid(self):
        response = self.client.get('/acme/grid/')
        print response.status_code
        self.assertEquals(response.status_code, 200)
