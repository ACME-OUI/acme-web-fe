import unittest
import requests
import os
import json
from poller.models import UserRuns
from django.test import LiveServerTestCase
import pdb


class Testresponses(LiveServerTestCase):
    fixtures = ['testdata.json']

    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_get_next(self):
        payload = {'request': 'next'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)
# --------------------------------------------------------------------------------
# Tests when request is 'all'
    def test_get_all_no_user(self):
        payload = {'request': 'all'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_get_all_with_user(self):
        payload = {'request': 'all', 'user': 'acmetest'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)
        for record in json.loads(r.content):
            self.assertTrue(record['user'] == 'acmetest')

    def test_post_all_with_user(self):
        payload = {'request': 'all', 'user': 'acmetest', 'status': 'complete'}
        r = requests.post(self.live_server_url + '/poller/update/', data=payload)
        self.assertTrue(r.status_code == requests.codes.ok)
        payload = {'request': 'all', 'user': 'acmetest'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        for job in r.json():
            self.assertEquals(job['status'], 'complete')
        payload = {'request': 'all', 'user': 'acme'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        for job in r.json():
            self.assertNotEquals(job['status'], 'complete')

# --------------------------------------------------------------------------------
# Tests when request is 'new'
    def test_get_new_no_user(self):
        payload = {'request': 'new'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_get_new_with_user(self):
        payload = {'request': 'new', 'user': 'acmetest'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)
        for record in json.loads(r.content):
            self.assertTrue(record['user'] == 'acmetest')

    def test_post_new(self):
        payload = {'request': 'new', 'user': 'test', 'config_options': json.dumps({'testdata': 'hello'})}
        r = requests.post(self.live_server_url + '/poller/update/', data=payload)
        self.assertTrue(r.status_code == requests.codes.ok)
        payload = {'request': 'all', 'user': 'test'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)
        for job in r.json():
            self.assertEquals(job['status'], 'new')
# --------------------------------------------------------------------------------
# Tests when request is 'in_progress'
    def test_get_in_progress(self):
        payload = {'request': 'in_progress'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_postin_progress(self):
        payload = {'request': 'in_progress', 'user': 'test'}
        r = requests.post(self.live_server_url + '/poller/update/', data=payload)
        self.assertTrue(r.status_code == requests.codes.ok)
        payload = {'request': 'all', 'user': 'acmetest'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        for job in r.json():
            self.assertEquals(job['status'], 'complete')
        payload = {'request': 'all', 'user': 'acme'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        for job in r.json():
            self.assertNotEquals(job['status'], 'complete')
# --------------------------------------------------------------------------------
    def test_get_complete(self):
        payload = {'request': 'complete'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_get_failed(self):
        payload = {'request': 'failed'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)


    def test_queueing(self):
        #
        # Test gets next run from queue, updates its status, and gets the next run after that.
        # The result should be a different id from the database
        #
        payload1 = {'request': 'next'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload1)
        self.assertTrue(r.status_code == requests.codes.ok)
        # pdb.set_trace()
        data = json.loads(r.content)  # converts from JSON to python object
        if data == {}:
            self.assertTrue(False)  # abort test if there are no items in queue
        oldid = data['id']
        # finished getting first user run 1
        s = requests.Session()
        r1 = s.get(self.live_server_url + '/poller/update/')
        self.assertTrue(r1.status_code == requests.codes.ok)
        csrf_token = r1.cookies['csrftoken']
        # finished getting csrf token
        headers = {
            'Content-type': 'application/json',
            "X-CSRFToken": csrf_token,
            'Referer': self.live_server_url + '/poller/update/'
        }
        # converts from python object to JSON string
        payload2 = json.dumps({'id': data['id'], 'status': 'in_progress'})
        r2 = s.patch(self.live_server_url + '/poller/update/', data=payload2, headers=headers)
        self.assertTrue(r2.status_code == requests.codes.ok)
        # finished posting updated status for user run 1
        r3 = requests.get(self.live_server_url + '/poller/update/', params=payload1)
        if r3.content:
            data = json.loads(r3.content)
            self.assertTrue(oldid != data['id'])

    def test_next_repeat(self):
        payload = {'request': 'next'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        datanew = json.loads(r.content)
        dataold = ''
        for i in range(20):
            dataold = datanew
            r = requests.get(self.live_server_url + '/poller/update/', params=payload)
            datanew = json.loads(r.content)
            self.assertTrue(dataold['id'] == datanew['id'])

    def test_bad_status(self):
        payload = {'request': 'next'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)
        data = json.loads(r.content)
        payload = json.dumps({'id': data['id'], 'status': 'bad_status'})
        s = requests.Session()
        r1 = s.get(self.live_server_url + '/poller/update/')
        self.assertTrue(r1.status_code == requests.codes.ok)
        csrf_token = r1.cookies['csrftoken']
        headers = {
            'Content-type': 'application/json',
            "X-CSRFToken": csrf_token,
            'Referer': self.live_server_url + '/poller/update/'
        }
        r2 = s.patch(self.live_server_url + '/poller/update/', data=payload, headers=headers)
        self.assertTrue(r2.status_code == 400)


# os.system('clear')
