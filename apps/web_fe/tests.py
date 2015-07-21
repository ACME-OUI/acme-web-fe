from django.test import TestCase
from django.test.client import Client
import json
from django.contrib.auth.models import User
from web_fe.views import *


def userSetup(current_test):
    # First create a new user
    current_test.test_user = User.objects.create_user(
        'testuser', 'test@test.test', 'testpass')
    # Now login as that user
    current_test.client = Client()
    current_test.client.login(username='testuser', password='testpass')


class VeloServiceTest(TestCase):

    def setUp(self):
        userSetup(self)
        credentials = {}
        credentials['velo'] = {}
        credentials['velo']['username'] = 'acmetest'
        credentials['velo']['password'] = 'acmetest'

        data = json.dumps(credentials)
        response = self.client.post(
            '/acme/add_credentials/', content_type='application/json', data=data)

    def tearDown(self):
        User.objects.filter(username='testuser').delete()

    def test_get_folder(self):

        # Check first that a valid response returns correctly
        data = json.dumps({
            'file': '/User Documents/acmetest/'
        })
        response = self.client.post(
            '/acme/get_folder/', content_type='application/json', data=data)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(
            json.loads(data)['file'] in json.loads(response.content))

        # Check that a request for an invalid user fails
        data = json.dumps({
            'file': '/User Documents/SOME_OTHER_USER/'
        })
        try:
            response = self.client.post(
                '/acme/get_folder/', content_type='application/json', data=data)
            self.assertEquals(response.status_code, 200)
            self.assertTrue(
                'resource  /User Documents/SOME_OTHER_USER/ does not exist' in json.loads(response.content))
        except:
            self.assertTrue(False)

    def test_get_valid_file(self):

        data = json.dumps({
            'text': 'This is text for the save_file test',
            'filename': 'testSaveFile.txt'
        })
        response = self.client.post(
            '/acme/velo_save_file/', content_type='application/json', data=data)

        data = json.dumps({
            'filename': 'testSaveFile.txt',
            'path': '/User Documents/acmetest'
        })
        response = self.client.post(
            '/acme/get_file/', content_type='application/json', data=data)
        self.assertEquals(response.status_code, 200)

    def test_get_bogus_file(self):

        data = json.dumps({
            'filename': 'THIS_FILE_DOES_NOT_EXIST',
            'path': '/User Documents/acmetest'
        })
        response = self.client.post(
            '/acme/get_file/', content_type='application/json', data=data)
        self.assertEquals(response.status_code, 500)

    def test_save_file(self):

        data = json.dumps({
            'text': 'This is text for the save_file test',
            'filename': 'testSaveFile.txt'
        })
        response = self.client.post(
            '/acme/velo_save_file/', content_type='application/json', data=data)
        self.assertEquals(response.status_code, 200)

    def test_create_folder(self):

        import random
        foldername = 'create_new_folder_test_' + str(random.getrandbits(32))
        data = json.dumps({
            'foldername': foldername
        })
        response = self.client.post(
            '/acme/velo_new_folder/', content_type='application/json', data=data)
        self.assertEquals(response.status_code, 200)
        response = self.client.post(
            '/acme/delete/', content_type='application/json', data=data)

    def test_delete_file(self):

        data = json.dumps({
            'text': 'This is text for the save_file test',
            'filename': 'testSaveFile.txt'
        })
        response = self.client.post(
            '/acme/velo_save_file/', content_type='application/json', data=data)
        response = self.client.post(
            '/acme/velo_delete/', content_type='application/json', data=json.dumps({'name': '/User Documents/acmetest/testSaveFile.txt'}))
        data = json.dumps({
            'filename': 'testSaveFile.txt',
            'path': '/User Documents/acmetest'
        })
        response = self.client.post(
            '/acme/get_file/', content_type='application/json', data=data)
        self.assertEquals(response.status_code, 500)


class ServiceCredentialTest(TestCase):

    def setUp(self):
        userSetup(self)

    def tearDown(self):
        User.objects.filter(username='testuser').delete()

    def test_save_credentials(self):
        credentials = {}
        credentials['esgf'] = {}
        credentials['esgf']['username'] = 'testuser'
        credentials['esgf']['password'] = 'testpass'
        try:
            data = json.dumps(credentials)
        except:
            self.assertTrue(False)
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

# Uncomment when ESGF comes back online
'''

class TestNodeInfo(TestCase):

    def setUp(self):
        userSetup(self)

    def tearDown(self):
        User.objects.filter(username='testuser').delete()

    def test_node_info(self):

        node = 'esgf-pcmdi-9'
        response = self.client.post(
            '/acme/node_info/', content_type='application/json', data=json.dumps({'node': node}))

        # Check that the server responeded with success
        self.assertEquals(response.status_code, 200)
        try:
            content = json.loads(response.content)
        except:
            self.assertTrue(False)
        print content['ip']
        # Check that the node info is there
        # This IP address is hard coded as the value for the ESG data node as
        # of 6/11/15
        self.assertEquals(content['ip'], '198.128.245.159')

    def test_bogus_node_name(self):

        node = 'BOGUS_NODE'
        response = self.client.post(
            '/acme/node_info/', content_type='application/json', data=json.dumps({'node': node}))

        # Check that the server responeded with success
        self.assertEquals(response.status_code, 501)

    def test_no_node(self):

        response = self.client.post(
            '/acme/node_info/', content_type='application/json', data=json.dumps({}))

        # Check that the server responeded with success
        self.assertEquals(response.status_code, 500)


class TestNodeSearch(TestCase):

    def setUp(self):
        userSetup(self)

    def tearDown(self):
        User.objects.filter(username='testuser').delete()

    def test_node_connection(self):
        request = {
            'node': 'http://pcmdi9.llnl.gov/esg-search/',
            'test_connection': 'true'
        }
        try:
            request = json.dumps(request)
        except:
            self.assertTrue(False)

        response = self.client.post(
            '/acme/node_search/', content_type='application/json', data=request)
        response_data = json.loads(response.content)

        self.assertEquals(response.status_code, 200)
        # hits as of 6/11/15
        self.assertTrue(response_data['institute']['LLNL'] >= 612)

    def test_node_search(self):

        request = {
            'node': 'http://pcmdi9.llnl.gov/esg-search/',
            'institute': 'LLNL'
        }
        request = json.dumps(request)
        response = self.client.post(
            '/acme/node_search/', content_type='application/json', data=request)
        try:
            response_data = json.loads(response.content)
        except:
            self.assertTrue(False)
        self.assertEquals(response.status_code, 200)
'''


class DashboardTest(TestCase):

    def setUp(self):
        userSetup(self)

    def tearDown(self):
        User.objects.filter(username='testuser').delete()

    def test_load_grid(self):
        response = self.client.get('/acme/dashboard/')

        # Check that the page is returning normally
        self.assertEquals(response.status_code, 200)

        # Check we are getting back more then one node
        # Uncomment this when ESGF comes back online
        # self.assertTrue(len(response.context['nodes']) > 1)


class LayoutTest(TestCase):

    def setUp(self):
        userSetup(self)

    def tearDown(self):
        User.objects.filter(username='testuser').delete()

    def test_save_and_load_layout(self):

        tiles = [{"y": 0.016666666666666666, "x": 0.1, "sizex": 1, "tileName": "provenance", "sizey": 0.5},
                 {"y": 0.5166666666666667, "x": 0.1, "sizex": 0.5,
                     "tileName": "status", "sizey": 0.5},
                 {"y": 0.5166666666666667, "x": 0.6, "sizex": 0.5, "tileName": "science", "sizey": 0.5}]
        try:
            tiles = json.dumps(tiles)
        except:
            self.assertTrue(False)
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

    def test_get_all_layouts(self):

        response = self.client.get('/acme/load_layout/')

        self.assertEquals(response.status_code, 200)
        self.assertTrue(len(response.content) > 0)


class UserLoginTest(TestCase):

    def setUp(self):
        userSetup(self)

    def tearDown(self):
        User.objects.filter(username='testuser').delete()

    def test_valid_user_login_success(self):
        user = {
            'username': 'testuser',
            'password': 'testpass'
        }
        response = self.client.post(
            '/acme/login/', {'username': user['username'], 'password': user['password']})

        self.assertEquals(response.status_code, 302)
        self.assertTrue(response.url.split('/').pop() != 'login')

    def test_valud_user_invalid_password_login_success(self):
        user = {
            'username': 'testuser',
            'password': 'NOT_A_GOOD_PASSWORD'
        }
        response = self.client.post(
            '/acme/login/', {'username': user['username'], 'password': user['password']})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url.split('/').pop(), 'login')

    def test_user_login_failure(self):
        user = {
            'username': 'NOT_A_USER',
            'password': 'NOT_A_PASSWORD'
        }
        response = self.client.post(
            '/acme/login/', {'username': user['username'], 'password': user['password']})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url.split('/').pop(), 'login')
