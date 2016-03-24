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
        # self.url = 'http://127.0.0.1:8000/poller/'

    def test_get_next(self):
        payload = {'status': 'next'}
        r = requests.get(self.live_server_url + '/poller/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_get_all(self):
        payload = {'status': 'all'}
        r = requests.get(self.live_server_url + '/poller/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_get_new(self):
        payload = {'status': 'new'}
        r = requests.get(self.live_server_url + '/poller/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_get_in_progress(self):
        payload = {'status': 'in_progress'}
        r = requests.get(self.live_server_url + '/poller/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_get_complete(self):
        payload = {'status': 'complete'}
        r = requests.get(self.live_server_url + '/poller/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_get_failed(self):
        payload = {'status': 'failed'}
        r = requests.get(self.live_server_url + '/poller/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_get_csrf(self):
        r = requests.get(self.live_server_url + '/poller/')
        self.assertTrue(r.status_code == requests.codes.ok)
        csrf = r.cookies['csrftoken']

    def test_update_status(self):
        payload = {'status': 'next'}
        r = requests.get(self.live_server_url + '/poller/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)
        data = json.loads(r.content)
        payload = json.dumps({'id': data['id'], 'status': 'in_progress'})
        s = requests.Session()
        r1 = s.get(self.live_server_url + '/poller/')
        self.assertTrue(r1.status_code == requests.codes.ok)
        csrf_token = r1.cookies['csrftoken']
        headers = {'Content-type': 'application/json',  "X-CSRFToken":csrf_token, 'Referer': self.live_server_url + '/poller/'}
        r2 = s.patch(self.live_server_url + '/poller/', data=payload, headers=headers)
        self.assertTrue(r2.status_code == requests.codes.ok)

    def test_queueing(self):
        # 
        # Test gets next run from queue, updates its status, and gets the next run after that.
        # The result should be a different id from the database
        # 
        payload1 = {'status': 'next'}
        r = requests.get(self.live_server_url + '/poller/', params=payload1)
        self.assertTrue(r.status_code == requests.codes.ok)
        #pdb.set_trace()
        data = json.loads(r.content) # converts from JSON to python object
        if data == {}:
            self.assertTrue(False) # abort test if there are no items in queue
        oldid = data['id']
        # finished getting first user run 1
        s = requests.Session()
        r1 = s.get(self.live_server_url + '/poller/')
        self.assertTrue(r1.status_code == requests.codes.ok)
        csrf_token = r1.cookies['csrftoken']
        # finished getting csrf token
        headers = {'Content-type': 'application/json',  "X-CSRFToken":csrf_token, 'Referer': self.live_server_url + '/poller/'}
        payload2 = json.dumps({'id': data['id'], 'status': 'in_progress'}) # converts from python object to JSON string
        r2 = s.patch(self.live_server_url + '/poller/', data=payload2, headers=headers)
        self.assertTrue(r2.status_code == requests.codes.ok)
        # finished posting updated status for user run 1
        r3 = requests.get(self.live_server_url + '/poller/', params=payload1)
        if r3.content:
            data = json.loads(r3.content)
            self.assertTrue(oldid != data['id'])

    def test_next_repeat(self):
        payload1 = {'status': 'next'}
        for i in range(20):
            r = requests.get(self.live_server_url + '/poller/', params=payload1)
            self.assertTrue(r.status_code == requests.codes.ok)

    def test_bad_status(self):
        payload = {'status': 'next'}
        r = requests.get(self.live_server_url + '/poller/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)
        data = json.loads(r.content)
        payload = json.dumps({'id': data['id'], 'status': 'bad_status'})
        s = requests.Session()
        r1 = s.get(self.live_server_url + '/poller/')
        self.assertTrue(r1.status_code == requests.codes.ok)
        csrf_token = r1.cookies['csrftoken']
        headers = {'Content-type': 'application/json',  "X-CSRFToken":csrf_token, 'Referer': self.live_server_url + '/poller/'}
        r2 = s.patch(self.live_server_url + '/poller/', data=payload, headers=headers)
        self.assertTrue(r2.status_code == 400)

            

os.system('clear')
