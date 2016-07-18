import unittest
import requests
import json
from django.test import LiveServerTestCase
from util.utilities import print_message


class TestResponses(LiveServerTestCase):
    fixtures = ['testdata.yaml']

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
        payload = json.dumps({'request': 'all', 'user': 'acmetest', 'status': 'complete'})
        r = requests.post(self.live_server_url + '/poller/update/', data=payload, headers={'content-type': 'application/json'})
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
        payload = json.dumps({'request': 'new', 'user': 'test', 'testdata': 'hello', 'model': 'CMIP5'})
        r = requests.post(self.live_server_url + '/poller/update/', data=payload, headers={'content-type': 'application/json'})
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

    def test_post_in_progress(self):
        payload = json.dumps({'request': 'in_progress', 'job_id': 1})
        r = requests.post(self.live_server_url + '/poller/update/', data=payload, headers={'content-type': 'application/json'})
        self.assertTrue(r.status_code == requests.codes.ok)
        payload = {'request': 'job', 'job_id': 1}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)
        data = json.loads(r.content)
        self.assertEquals(data['status'], 'in_progress')
# --------------------------------------------------------------------------------

# Tests when request is 'complete'

    def test_get_complete(self):
        payload = {'request': 'complete'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_post_comlete(self):
        payload = json.dumps({'request': 'complete', 'job_id': 1})
        r = requests.post(self.live_server_url + '/poller/update/', data=payload, headers={'content-type': 'application/json'})
        print_message(r.status_code)
        self.assertTrue(r.status_code == requests.codes.ok)
        payload = {'request': 'job', 'job_id': 1}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)
        data = json.loads(r.content)
        self.assertEquals(data['status'], 'complete')
# --------------------------------------------------------------------------------

# Tests when request is 'in_progress'

    def test_get_failed(self):
        payload = {'request': 'failed'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)

    def test_post_failed(self):
        payload = json.dumps({'request': 'failed', 'job_id': 1})
        r = requests.post(self.live_server_url + '/poller/update/', data=payload, headers={'content-type': 'application/json'})
        self.assertTrue(r.status_code == requests.codes.ok)
        payload = {'request': 'job', 'job_id': 1}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        self.assertTrue(r.status_code == requests.codes.ok)
        data = json.loads(r.content)
        self.assertEquals(data['status'], 'failed')
# --------------------------------------------------------------------------------

# Tests when request is 'delete'

    def test_delete(self):
        payload = json.dumps({'request': 'delete', 'job_id': 1})
        r = requests.post(self.live_server_url + '/poller/update/', data=payload, headers={'content-type': 'application/json'})
        self.assertTrue(r.status_code == 200)  # delete job successfully

# --------------------------------------------------------------------------------

# Testing behavior

    def test_queueing(self):
        #
        # Test gets next run from queue, updates its status, and gets the next run after that.
        # The result should be a different id from the database
        #
        payload1 = {'request': 'next'}
        r1 = requests.get(self.live_server_url + '/poller/update/', params=payload1)
        self.assertTrue(r1.status_code == requests.codes.ok)
        oldid = json.loads(r1.content)['job_id']
        # finished getting first user run
        payload2 = json.dumps({'request': 'complete', 'job_id': oldid})
        r2 = requests.post(self.live_server_url + '/poller/update/', data=payload2, headers={'content-type': 'application/json'})
        self.assertTrue(r2.status_code == requests.codes.ok)
        # finished updated the run's status
        r3 = requests.get(self.live_server_url + '/poller/update/', params=payload1)
        self.assertTrue(r3.status_code == requests.codes.ok)
        # r3 run should be a different id
        newid = json.loads(r3.content)['job_id']
        self.assertNotEqual(oldid, newid)

    def test_next_repeat(self):
        payload = {'request': 'next'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        datanew = json.loads(r.content)
        for i in range(20):
            dataold = datanew
            r = requests.get(self.live_server_url + '/poller/update/', params=payload)
            datanew = json.loads(r.content)
            self.assertTrue(dataold['job_id'] == datanew['job_id'])

    def test_get_bad_request(self):
        payload = {'request': 'bad_parameter', 'job_id': 1, 'status': 'complete'}
        r2 = requests.get(self.live_server_url + '/poller/update/', data=payload)
        self.assertTrue(r2.status_code == 400)

    def test_post_bad_request(self):
        payload = json.dumps({'request': 'bad_parameter', 'job_id': 1, 'status': 'complete'})
        r = requests.post(self.live_server_url + '/poller/update/', data=payload, headers={'content-type': 'application/json'})
        self.assertTrue(r.status_code == 400)

    def test_get_empty(self):
        payload = json.dumps({'request': 'all', 'status': 'complete'})
        r = requests.post(self.live_server_url + '/poller/update/', data=payload, headers={'content-type': 'application/json'})
        self.assertTrue(r.status_code == requests.codes.ok)
        payload = {'request': 'next'}
        r = requests.get(self.live_server_url + '/poller/update/', params=payload)
        data = json.loads(r.content)
        self.assertEquals(len(data.keys()), 0)
