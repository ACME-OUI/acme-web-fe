from django.test import LiveServerTestCase
import json
import requests
from constants import NODE_HOSTNAMES
import inspect
from util.utilities import print_message
from django.contrib.auth.models import User
from web_fe.models import Notification
from django.test import Client


class TestUploadToViewer(LiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')
        self.note = Notification(user='test')
        self.note.save()
        self.upload_viewer_user = 'baldwin2'
        self.upload_password = 'qwertyuiop'
        self.server_url = 'https://acme-ea.ornl.gov/'
        self.upload_endpoint = '/esgf/upload_to_viewer/'

    def test_upload_to_viewer(self):
        request = json.dumps({
            'run_name': 'test_run',
            'username': self.upload_viewer_user,
            'password': self.upload_password,
            'server': self.server_url
        })
        r = self.c.post(self.upload_endpoint, data=request, content_type='application/json')
        self.assertTrue(r.status_code == 200)
        self.assertTrue('dataset_id' in r.content)


class TestPublishConfig(LiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.note = Notification(user='test')
        self.note.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')
        self.params = json.dumps({
            'config_name': 'test_data',
            'path': '/path/to/data/',
            'metadata': {
                'name': 'test publication',
                'firstname': 'Tester',
                'lastname': 'McTest',
                'datanode': 'node',
                'organization': 'test org',
                'description':'a test publish config',
            },
            'server': 'some.server.somewhere.gov',
            'esgf_user': 'Tester',
            'esgf_password': 'McTesterson',
            'facets': {
                'project': 'ACME',
                'data_type': 'h0',
                'experiment': 'b1850c5_m1a',
                'versionnum': 'v0_1',
                'realm': 'atm',
                'regrinding': 'ne30_g16',
                'range': 'all',
            }
        })

    def test_publish_from_config(self):
        publish_url = self.live_server_url + '/esgf/publish/'
        save_url = self.live_server_url + '/esgf/save_publish_config/'
        r = self.c.post(save_url, data=self.params, content_type='application/json')
        self.assertTrue(r.status_code == 200)
        config = json.dumps({
            'config_name': 'test_data',
            'path': '/path/to/data/hhh',
            'metadata': {
                'name': 'name',
                'value': 'test dataset'
            },
            'server': 'some.server.somewhere.gov',
            'esgf_user': 'Tester',
            'esgf_password': 'McTesterson',
        })
        r = self.c.post(publish_url, config, content_type='application/json')
        self.assertTrue(r.status_code == 200)

    def test_publish_no_config(self):
        publish_url = self.live_server_url + '/esgf/publish/'
        params = json.loads(self.params)
        del params['config_name']
        params = json.dumps(params)
        r = self.c.post(publish_url, params, content_type='application/json')
        self.assertTrue(r.status_code == 200)

    def test_get_config(self):
        save_url = self.live_server_url + '/esgf/save_publish_config/'
        get_url = self.live_server_url + '/esgf/get_publish_config/'

        r = self.c.post(save_url, data=self.params, content_type='application/json')
        self.assertTrue(r.status_code == 200)
        r = self.c.get(get_url, {'config_name': 'test_data'})
        content = json.loads(r.content)
        print_message(content)
        self.assertTrue(r.status_code == 200)
        self.assertTrue('test_data' in content.get('config_name'))

    def test_get_config_list(self):
        save_url = self.live_server_url + '/esgf/save_publish_config/'
        get_url = self.live_server_url + '/esgf/get_publish_config_list/'

        r = self.c.post(save_url, data=self.params, content_type='application/json')
        self.assertTrue(r.status_code == 200)
        r = self.c.post(get_url)
        print_message(r.content)
        self.assertTrue(r.status_code == 200)
        self.assertTrue('test_data' in json.loads(r.content))

    def test_save_valid_config(self):
        url = self.live_server_url + '/esgf/save_publish_config/'

        r = self.c.post(url, data=self.params, content_type='application/json')
        self.assertTrue(r.status_code == 200)

    def test_save_invalid_config(self):
        url = self.live_server_url + '/esgf/save_publish_config/'
        params = json.dumps({
            'not a valid key': 'some value',
            'facets': {
                'project': 'ACME',
                'data_type': 'h0',
                'experiment': 'b1850c5_m1a',
                'versionnum': 'v0_1',
                'realm': 'atm',
                'regrinding': 'ne30_g16',
                'range': 'all',
            }
        })
        r = self.c.post(url, data=params, content_type='application/json')
        self.assertTrue(r.status_code == 400)

    def test_save_same_config_twice(self):
        url = self.live_server_url + '/esgf/save_publish_config/'

        r = self.c.post(url, data=self.params, content_type='application/json')
        self.assertTrue(r.status_code == 200)
        r = self.c.post(url, data=self.params, content_type='application/json')
        self.assertTrue(r.status_code == 500)


class TestLogon(LiveServerTestCase):

    def setUp(self):
        self.username = 'https://pcmdi.llnl.gov/esgf-idp/openid/acmetest'
        self.password = 'ACM#t3st'
        self.note = Notification(user='test')
        self.note.save()

    def test_logon_success(self):
        print "\n---->[+] Starting " + inspect.stack()[0][3]
        credential = {
            'username': self.username,
            'password': self.password
        }
        response_code = requests.get(self.live_server_url + '/esgf/logon/', params=credential).status_code
        message = 'Status code: {}'.format(response_code)
        print_message(message, 'error')
        self.assertTrue(response_code == 200)

    def test_logon_fail(self):
        print "\n---->[+] Starting " + inspect.stack()[0][3]
        credential = {
            'username': 'http://abra',
            'password': 'cadabra'
        }
        response_code = requests.get(self.live_server_url + '/esgf/logon/', params=credential).status_code
        self.assertFalse( response_code == 200)

    def test_logon_fail_no_user(self):
        print "\n---->[+] Starting " + inspect.stack()[0][3]
        print "--------------------------------------------"
        credential = {
            'asdf': 'http://abra',
            'fdsa': 'cadabra'
        }
        response_code = requests.get(self.live_server_url + '/esgf/logon/', params=credential).status_code
        self.assertTrue( response_code == 403)

    def test_logon_fail_no_pass(self):
        print "\n---->[+] Starting " + inspect.stack()[0][3]
        print "--------------------------------------------"
        credential = {
            'username': 'http://abra',
            'fdsa': 'cadabra'
        }
        response_code = requests.get(self.live_server_url + '/esgf/logon/', params=credential).status_code
        self.assertTrue( response_code == 403)


class TestLoadFacet(LiveServerTestCase):

    def test_load_facet_success(self):
        print "\n---->[+] Starting " + inspect.stack()[0][3]
        data = json.dumps(NODE_HOSTNAMES[0:1])
        response = requests.get(self.live_server_url + '/esgf/load_facets/', params={'nodes': data})
        self.assertTrue( response.status_code == 200 )

    def test_load_facet_failure(self):
        print "\n---->[+] Starting " + inspect.stack()[0][3]
        print "____ this should print a stack trace ________"
        print "--------------------------------------------"
        data = json.dumps(['this', 'is', 'not', 'a', 'hostname'])
        response = requests.get(self.live_server_url + '/esgf/load_facets/', params={'nodes': data})
        self.assertFalse( response.status_code == 200 )


class TestNodeSearch(LiveServerTestCase):

    def setUp(self):
        self.valid_nodes = NODE_HOSTNAMES[0:1]
        self.note = Notification(user='test')
        self.note.save()
        self.invalid_nodes = ['not.a.node.gov', 'also.not.a.node.gov']
        self.valid_terms = {'project': 'ACME'}
        self.invalid_terms = {'not_a_valid': 'search_term'}

    def test_node_search_success(self):
        print "\n---->[+] Starting " + inspect.stack()[0][3]
        params = {
            'searchString': json.dumps(self.valid_terms),
            'nodes': json.dumps(self.valid_nodes)
        }
        response = requests.get(self.live_server_url + '/esgf/node_search/', params=params)
        self.assertTrue( response.status_code == 200 )
        self.assertTrue( len(response.content) > 100 )

    # def test_node_search_no_node(self):
    #     print "\n---->[+] Starting " + inspect.stack()[0][3]
    #     params = {
    #         'searchString': json.dumps(self.valid_terms),
    #         'asdf': json.dumps(self.valid_nodes)
    #     }
    #     response = requests.get(self.live_server_url + '/esgf/node_search/', params=params)
    #     self.assertTrue( response.status_code == 400 )
    #     self.assertTrue( len(response.content) < 100 )

    def test_node_search_bad_node(self):
        print "\n---->[+] Starting " + inspect.stack()[0][3]
        print "____ this should print a stack trace ________"
        print "--------------------------------------------"
        request = json.dumps({
            'nodes': self.invalid_nodes,
            'terms': self.valid_terms
        })
        response = requests.get(self.live_server_url + '/esgf/node_search/', params={'searchString':request})
        self.assertFalse( response.status_code == 200 )
        self.assertFalse( len(response.content) > 100 )

    def test_node_search_bad_term(self):
        print "\n---->[+] Starting " + inspect.stack()[0][3]
        print "____ this should print a stack trace ________"
        print "--------------------------------------------"
        request = json.dumps({
            'nodes': self.valid_nodes,
            'terms': self.invalid_terms
        })
        response = requests.get(self.live_server_url + '/esgf/node_search/', params={'searchString':request})
        self.assertFalse( response.status_code == 200 )
        self.assertFalse( len(response.content) > 100 )


class TestNodeList(LiveServerTestCase):

    def test_get_node_list(self):
        print "\n---->[+] Starting " + inspect.stack()[0][3]
        response = requests.get(self.live_server_url + '/esgf/node_list')
        self.assertTrue( response.status_code == 200 )
        self.assertTrue( 'pcmdi.llnl.gov' in json.loads(response.content) )

#
# These URLs are old and dont work anymore
#
# class TestDownload(LiveServerTestCase):
#
#     def setUp(self):
#         self.auth_url = 'http://aims3.llnl.gov/thredds/fileServer/cmip5_css01_data/cmip5/output1/LASG-CESS/FGOALS-g2/midHolocene/day/seaIce/day/r1i1p1/v1/usi/usi_day_FGOALS-g2_midHolocene_r1i1p1_05320101-05321231.nc'
#         self.unauth_url = 'http://airsl2.gesdisc.eosdis.nasa.gov/thredds/fileServer/cmac/taNobs_AIRS_L3_RetStd-v6_201502.nc'
#         self.bad_url = 'http://not.a.site.llnl.gov/not_a_file.nc'
#
#     def test_download_unauth(self):
#         print "\n---->[+] Starting " + inspect.stack()[0][3]
#         response = requests.get(self.live_server_url + '/esgf/download', params={'url': self.unauth_url})
#         self.assertTrue( response.status_code == 200 )
#
#     def test_download_bad_url(self):
#         print "\n---->[+] Starting " + inspect.stack()[0][3]
#         response = requests.get(self.live_server_url + '/esgf/download', params={'url': self.bad_url})
#         print_message(response.status_code)
#         self.assertTrue( response.status_code == 400 )

    # TODO: make this work
    # def test_download_auth(self):
    #     print "\n---->[+] Starting " + inspect.stack()[0][3]
    #     response = requests.get(self.live_server_url + '/esgf/download', params={'url': self.auth_url})
    #     self.assertTrue( response.status_code == 200 )
