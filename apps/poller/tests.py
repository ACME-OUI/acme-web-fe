from django.test import TestCase
from django.test import LiveServerTestCase
from django.test import Client
from django.contrib.auth.models import User
from web_fe.models import Notification
from util.utilities import print_message
import json

fixtures = ['testdata.yaml']


class TestGetNext(LiveServerTestCase):
    ''' Tests the get_next functionality of the poller '''
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.note = Notification(user='test')
        self.note.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')

    def test_get_next(self):
        ''' Tests popping the next job off the queue '''
        payload = {'request': 'next'}
        r = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        self.assertTrue(r.status_code == 200)


class TestGetAll(LiveServerTestCase):
    ''' Tests the get_all functionaility of the poller '''
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.note = Notification(user='test')
        self.note.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')

    def test_get_all_no_user(self):
        ''' tests getting all jobs globally '''
        payload = {'request': 'all'}
        r = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        self.assertTrue(r.status_code == 200)

    def test_get_all_with_user(self):
        ''' tests getting all jobs for a specific user '''
        payload = {'request': 'all', 'user': 'acmetest'}
        r = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        self.assertTrue(r.status_code == 200)
        for record in json.loads(r.content):
            self.assertTrue(record['user'] == 'acmetest')

    def test_post_all_with_user(self):
        ''' tests changing the status of all jobs for a specific user '''
        payload = {'request': 'all', 'user': 'acmetest', 'status': 'complete'}
        r = self.c.post(self.live_server_url + '/poller/update/', data=json.dumps(payload), content_type='application/json')
        self.assertTrue(r.status_code == 200)
        payload = {'request': 'all', 'user': 'acmetest'}
        r = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        for job in r.json():
            self.assertEquals(job['status'], 'complete')
        payload = {'request': 'all', 'user': 'acme'}
        r = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        for job in r.json():
            self.assertNotEquals(job['status'], 'complete')


class TestNew(LiveServerTestCase):
    ''' Tests when request is 'new' '''
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.note = Notification(user='test')
        self.note.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')

    def test_get_new_no_user(self):
        payload = {'request': 'new'}
        r = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        self.assertTrue(r.status_code == 200)

    def test_get_new_with_user(self):
        payload = {'request': 'new', 'user': 'acmetest'}
        r = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        print_message('status code: {}'.format(r.status_code))
        self.assertTrue(r.status_code == 200)
        for record in json.loads(r.content):
            self.assertTrue(record['user'] == 'acmetest')

    def test_post_new(self):
        payload = {'request': 'new', 'user': 'test', 'testdata': 'hello', 'model': 'CMIP5'}
        print_message('Sending payload to poller {}'.format(payload), 'ok')
        r = self.c.post(self.live_server_url + '/poller/update/', data=json.dumps(payload), content_type='application/json')
        print_message('Got status code {}'.format(r.status_code))
        self.assertTrue(r.status_code == 200)

        payload = {'request': 'all', 'user': 'test'}
        print_message('Sending payload to poller {}'.format(payload), 'ok')
        r = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        print_message('Got status code {}'.format(r.status_code))
        self.assertTrue(r.status_code == 200)
        for job in r.json():
            self.assertEquals(job['status'], 'new')


class TestInProgress(LiveServerTestCase):
    ''' Tests when request is 'in_progress' '''
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.note = Notification(user='test')
        self.note.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')

    def test_get_in_progress(self):
        payload = {'request': 'in_progress'}
        r = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        self.assertTrue(r.status_code == 200)

    def test_post_in_progress(self):
        payload = {'request': 'new', 'user': 'test', 'testdata': 'hello', 'model': 'CMIP5', 'run_name': 'testrun'}
        r = self.c.post(self.live_server_url + '/poller/update/', data=json.dumps(payload), content_type='application/json')
        job_id = json.loads(r.content).get('job_id')
        self.assertTrue(job_id)

        payload = {'request': 'in_progress', 'job_id': job_id}
        r = self.c.post(self.live_server_url + '/poller/update/', data=json.dumps(payload), content_type='application/json')
        self.assertTrue(r.status_code == 200)

        payload = {'request': 'job', 'job_id': job_id}
        r = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        self.assertTrue(r.status_code == 200)
        data = json.loads(r.content)
        self.assertEquals(data['status'], 'in_progress')


class TestComplete(LiveServerTestCase):
    ''' Tests when request is 'complete' '''
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.note = Notification(user='test')
        self.note.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')

    def test_get_complete(self):
        payload = {'request': 'complete'}
        r = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        self.assertTrue(r.status_code == 200)

    def test_post_comlete(self):
        payload = {'request': 'new','user': 'test', 'testdata': 'hello', 'model': 'CMIP5'}
        r = self.c.post(self.live_server_url + '/poller/update/', data=json.dumps(payload), content_type='application/json')
        job_id = json.loads(r.content).get('job_id')
        self.assertTrue(job_id)

        payload = {'request': 'complete', 'job_id': job_id}
        r = self.c.post(self.live_server_url + '/poller/update/', data=json.dumps(payload), content_type='application/json')
        print_message(r.status_code)
        self.assertTrue(r.status_code == 200)

        payload = {'request': 'job', 'job_id': job_id}
        r = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        self.assertTrue(r.status_code == 200)
        data = json.loads(r.content)
        self.assertEquals(data['status'], 'complete')


class TestFailed(LiveServerTestCase):
    ''' Tests when request is 'failed' '''
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.note = Notification(user='test')
        self.note.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')

    def test_get_failed(self):
        payload = {'request': 'failed'}
        r = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        self.assertTrue(r.status_code == 200)

    def test_post_failed(self):
        # first create a new job
        payload = {'request': 'new', 'user': 'test', 'testdata': 'hello', 'model': 'CMIP5'}
        print_message('Sending payload to poller {}'.format(payload), 'ok')
        r = self.c.post(self.live_server_url + '/poller/update/', data=json.dumps(payload), content_type='application/json')
        print_message('Got status code {}'.format(r.status_code))
        self.assertTrue(r.status_code == 200)
        job_id = json.loads(r.content).get('job_id')
        self.assertTrue(job_id)

        # next set the job to 'failed'
        payload = {'request': 'failed', 'job_id': job_id}
        print_message('sending payload to poller {}'.format(payload), 'ok')
        r = self.c.post(self.live_server_url + '/poller/update/', data=json.dumps(payload), content_type='application/json')
        print_message('Status code {}'.format(r.status_code))
        self.assertTrue(r.status_code == 200)

        # finally check that it was set correctly
        payload = {'request': 'job', 'job_id': job_id}
        print_message('sending payload to poller {}'.format(payload), 'ok')
        r = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        print_message('Status code {}'.format(r.status_code))
        self.assertTrue(r.status_code == 200)
        data = json.loads(r.content)
        self.assertEquals(data['status'], 'failed')


class TestDelete(LiveServerTestCase):
    ''' Tests when request is 'delete' '''
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.note = Notification(user='test')
        self.note.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')

    def test_delete(self):
        ''' test the ability to delete a job '''
        # setup test by adding a job
        payload = {
            'request': 'new',
            'user': 'test',
            'testdata': 'hello',
            'model': 'CMIP5',
            'run_type': 'diagnostic',
            'run_name': 'test_run'
        }
        r = self.c.post(self.live_server_url + '/poller/update/', data=json.dumps(payload), content_type='application/json')
        self.assertTrue(r.status_code == 200)
        job_id = json.loads(r.content).get('job_id')
        self.assertTrue(job_id)

        # now test if the job can be deleted
        payload = {'request': 'delete', 'job_id': job_id}
        r = self.c.post(self.live_server_url + '/poller/update/', data=json.dumps(payload), content_type='application/json')
        self.assertTrue(r.status_code == 200)  # delete job successfully


class TestBehavior(LiveServerTestCase):
    ''' Testing behavior '''
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.note = Notification(user='test')
        self.note.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')

    def test_queueing(self):
        '''
         Test the queue gives jobs back in the correct order
        '''
        #first seed the db with two jobs
        payload = {
            'request': 'new',
            'user': 'test',
            'testdata': 'hello',
            'model': 'CMIP5',
            'run_type': 'diagnostic',
            'run_name': 'test_run'
        }
        r = self.c.post(self.live_server_url + '/poller/update/', data=json.dumps(payload), content_type='application/json')
        self.assertTrue(r.status_code == 200)
        job_id_1 = json.loads(r.content).get('job_id')
        self.assertTrue(job_id_1)

        payload = {
            'request': 'new',
            'user': 'test',
            'testdata': 'hello',
            'model': 'CMIP5',
            'run_type': 'diagnostic',
            'run_name': 'test_run'
        }
        r = self.c.post(self.live_server_url + '/poller/update/', data=json.dumps(payload), content_type='application/json')
        self.assertTrue(r.status_code == 200)
        job_id_2 = json.loads(r.content).get('job_id')
        self.assertTrue(job_id_2)

        # next pop the jobs off the queue
        payload1 = {'request': 'next'}
        r1 = self.c.get(self.live_server_url + '/poller/update/', data=payload1, content_type='application/json')
        self.assertTrue(r1.status_code == 200)
        oldid = json.loads(r1.content)['job_id']

        # finished getting first user run
        payload2 = {'request': 'complete', 'job_id': oldid}
        r2 = self.c.post(self.live_server_url + '/poller/update/', data=payload2, content_type='application/json')
        self.assertTrue(r2.status_code == 200)
        # finished updated the run's status
        r3 = self.c.get(self.live_server_url + '/poller/update/', data=payload1, content_type='application/json')
        self.assertTrue(r3.status_code == 200)
        # r3 run should be a different id
        newid = json.loads(r3.content)['job_id']
        self.assertNotEqual(oldid, newid)

    # def test_next_repeat(self):
    #     payload = {'request': 'next'}
    #     r = requests.get(self.live_server_url + '/poller/update/', data=payload)
    #     datanew = json.loads(r.content)
    #     for i in range(20):
    #         dataold = datanew
    #         r = requests.get(self.live_server_url + '/poller/update/', data=payload)
    #         datanew = json.loads(r.content)
    #         self.assertTrue(dataold['job_id'] == datanew['job_id'])

    def test_get_bad_request(self):
        payload = {'request': 'bad_parameter', 'job_id': 1, 'status': 'complete'}
        r2 = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        self.assertTrue(r2.status_code == 400)

    def test_post_bad_request(self):
        payload = {'request': 'bad_parameter', 'job_id': 1, 'status': 'complete'}
        r = self.c.post(self.live_server_url + '/poller/update/', data=json.dumps(payload), content_type='application/json')
        self.assertTrue(r.status_code == 400)

    def test_get_empty(self):
        payload = {'request': 'all', 'status': 'complete'}
        r = self.c.post(self.live_server_url + '/poller/update/', data=json.dumps(payload), content_type='application/json')
        self.assertTrue(r.status_code == 200)
        payload = {'request': 'next'}
        r = self.c.get(self.live_server_url + '/poller/update/', data=payload, content_type='application/json')
        data = json.loads(r.content)
        self.assertEquals(len(data.keys()), 0)
