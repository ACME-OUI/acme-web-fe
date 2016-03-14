import unittest
import requests
import os
import json
from poller.models import UserRuns
import pdb

class Testresponses(unittest.TestCase):
    fixtures = ['initial.json']

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.url = 'http://127.0.0.1:8000/poller/'


    def test_get_next(self):
        payload = {'status': 'next'}
        r = requests.get(self.url , params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_get_all(self):
        payload = {'status': 'all'}
        r = requests.get(self.url , params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_get_new(self):
        payload = {'status': 'new'}
        r = requests.get(self.url, params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_get_in_progress(self):
        payload = {'status': 'in_progress'}
        r = requests.get(self.url, params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_get_complete(self):
        payload = {'status': 'complete'}
        r = requests.get(self.url, params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_get_failed(self):
        payload = {'status': 'failed'}
        r = requests.get(self.url, params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_get_csrf(self):
        r = requests.get(self.url)
        self.assertTrue(r.status_code == requests.codes.ok)
        csrf = r.cookies['csrftoken']

    def test_update_status(self):
        payload = {'status': 'next'}
        r = requests.get(self.url, params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)
        data = json.loads(r.content)
        payload = json.dumps({'id': data['id'], 'status': 'In_progress'})
        s = requests.Session()
        r1 = s.get(self.url)
        self.assertTrue(r1.status_code == requests.codes.ok)
        csrf_token = r1.cookies['csrftoken']
        headers = {'Content-type': 'application/json',  "X-CSRFToken":csrf_token, 'Referer': self.url}
        r2 = s.patch(self.url, data=payload, headers=headers)
        self.assertTrue(r2.status_code == requests.codes.ok)

    def test_queueing(self):
        # 
        # Test gets next run in line, updates its status, and gets the next run after that.
        # The result should be a different id from the database
        # 
        payload1 = {'status': 'next'}
        r = requests.get(self.url, params=payload1)
        self.assertTrue(r.status_code == requests.codes.ok)
        data = json.loads(r.content) # converts from JSON to python object
        if data == {}:
            return True # abort test if there are no 
        oldid = data['id']
        # finished getting first user run 1
        s = requests.Session()
        r1 = s.get(self.url)
        self.assertTrue(r1.status_code == requests.codes.ok)
        csrf_token = r1.cookies['csrftoken']
        # finished getting csrf token
        headers = {'Content-type': 'application/json',  "X-CSRFToken":csrf_token, 'Referer': self.url}
        payload2 = json.dumps({'id': data['id'], 'status': 'In_progress'}) # converts from python object to JSON string
        r2 = s.patch(self.url, data=payload2, headers=headers)
        self.assertTrue(r2.status_code == requests.codes.ok)
        # finished posting updated status for user run 1
        r3 = requests.get(self.url, params=payload1)
        if r3.content:
            data = json.loads(r3.content)
            self.assertTrue(oldid != data['id'])


os.system('clear')
