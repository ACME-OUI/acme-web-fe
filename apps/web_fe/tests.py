from django.utils import unittest
from django.test.client import Client
import json
from django.contrib.auth.models import User


def userSetup(self):
    # First create a new user
    self.test_user = User.objects.create_user(
        'testuser', 'test@test.test', 'testpass')
    # Now login as that user
    self.client = Client()
    self.client.login(username='testuser', password='testpass')


class CredentialTest(unittest.TestCase):

    def setUp(self):
        userSetup(self)

    def tearDown(self):
        User.objects.filter(username='testuser').delete()

    def test_save_credentials(self):
        credentials = {}
        credentials['esgf'] = {}
        credentials['esgf']['username'] = 'testuser'
        credentials['esgf']['password'] = 'testpass'

        data = json.dumps(credentials)
        response = self.client.post(
            '/acme/add_credentials/', content_type='application/json', data=data)

        # Check the page came back normally
        self.assertEquals(response.status_code, 200)

        # Check the credential actually got saved
        self.assertEquals(response.context['added'], 'true')

    def test_empty_credentials(self):
        response = self.client.post(
            '/acme/add_credentials/', content_type='application/json', data={})

        # Check the page came back normally
        self.assertEquals(response.status_code, 200)

        # Check that nothing was added
        self.assertEquals(response.context['added'], 'false')


class NodeInfoTest(unittest.TestCase):

    def setUp(self):
        userSetup(self)

    def tearDown(self):
        User.objects.filter(username='testuser').delete()

    def test_node_info(self):

        node = 'esgdata'
        response = self.client.post(
            '/acme/node_info/', content_type='application/json', data=json.dumps({'node': node}))

        # Check that the server responeded with success
        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content)
        print content['ip']
        # Check that the node info is there
        self.assertEquals(content['ip'], '140.208.31.117')


class GridTest(unittest.TestCase):

    def setUp(self):
        userSetup(self)

    def tearDown(self):
        User.objects.filter(username='testuser').delete()

    def test_load_grid(self):
        response = self.client.get('/acme/grid/')

        # Check that the page is returning normally
        self.assertEquals(response.status_code, 200)

        # Check we are getting back more then one node
        self.assertTrue(len(response.context['nodes']) > 1)


class LayoutTest(unittest.TestCase):

    def setUp(self):
        userSetup(self)

    def tearDown(self):
        User.objects.filter(username='testuser').delete()

    def test_save_and_load_layout(self):

        tiles = [{"y": 0.016666666666666666, "x": 0.1, "sizex": 1, "tileName": "provenance", "sizey": 0.5},
                 {"y": 0.5166666666666667, "x": 0.1, "sizex": 0.5,
                     "tileName": "status", "sizey": 0.5},
                 {"y": 0.5166666666666667, "x": 0.6, "sizex": 0.5, "tileName": "science", "sizey": 0.5}]

        tiles = json.dumps(tiles)
        layout = {
            'name': 'testlayout',
            'layout': tiles,
            'default_layout': 'False',
            'mode': 'night',
            'style': 'balanced'
        }

        # Check that we're able to save the layout
        response = self.client.post(
            '/acme/save_layout/', content_type='application/json', data=json.dumps(layout))
        self.assertEquals(response.status_code, 200)

        # Check if when we ask for it, the same layout comes back
        response = self.client.post(
            '/acme/load_layout/', content_type='application/json', data=json.dumps({'layout_name': 'testlayout'}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content)['board_layout'], tiles)

    def test_bogus_layout_request(self):

        response = self.client.post(
            '/acme/load_layout/', content_type='application/json', data=json.dumps({'layout_name': 'THIS_LAYOUT_DOESNT_EXIST'}))

        self.assertEquals(response.status_code, 500)
        self.assertEquals(len(response.content), 0)
