import unittest
import requests
import os
import json

class Testresponses(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.url = 'http://127.0.0.1:8000/poller/'

    def test_get_all(self):
        payload = {'status': 'all'}
        r = requests.get(self.url , params=payload)
        self.assertEqual(str(r), '<Response [200]>')

    def test_get_new(self):
        payload = {'status': 'new'}
        r = requests.get(self.url, params=payload)
        self.assertEqual(str(r), '<Response [200]>')

    def test_get_in_progress(self):
        payload = {'status': 'in_progress'}
        r = requests.get(self.url, params=payload)
        self.assertEqual(str(r), '<Response [200]>')

    def test_get_complete(self):
        payload = {'status': 'complete'}
        r = requests.get(self.url, params=payload)
        self.assertEqual(str(r), '<Response [200]>')

    def test_get_failed(self):
        payload = {'status': 'failed'}
        r = requests.get(self.url, params=payload)
        self.assertEqual(str(r), '<Response [200]>')

    def test_get_csrf(self):
        r = requests.get(self.url)
        self.assertEqual(str(r), '<Response [200]>')
        csrf = r.cookies['csrftoken']
    def test_update_status(self):
        payload = json.dumps({'id': 1, 'status': 'In_progress'})
        s = requests.Session()
        r1 = s.get(self.url)
        self.assertEqual(str(r1), '<Response [200]>')
        csrf_token = r1.cookies['csrftoken']
        headers = {'Content-type': 'application/json',  "X-CSRFToken":csrf_token, 'Referer': self.url}
        r2 = s.post(self.url, data=payload, headers=headers)
        self.assertEqual(str(r2), '<Response [200]>')

os.system('clear')
suite = unittest.TestLoader().loadTestsFromTestCase(Testresponses)
unittest.TextTestRunner(verbosity=1).run(suite)
