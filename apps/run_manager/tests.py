from django.test import TestCase
from django.test import LiveServerTestCase
from django.test import Client
from django.contrib.auth.models import User
import json
import shutil
import os
import requests
from constants import RUN_SCRIPT_PATH
from util.utilities import print_message


class TestCreateRun(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.c = Client()
        self.url = self.live_server_url + '/run_manager/create_run/'
        logged_in = self.c.login(username='test', password='test')

    def tearDown(self):
        path = os.path.abspath(os.path.dirname(__file__))
        run_directory = path + RUN_SCRIPT_PATH + 'test'
        shutil.rmtree(run_directory, ignore_errors=True)

    def test_valid_run(self):
        request = {
            'run_name': 'test_run',
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.url, data=json.dumps(request), content_type='application/json')
        print_message('status code given' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

    def test_create_run_with_valid_template(self):
        request = {
            'run_name': 'test_run_with_template',
            'template': 'ACME_script.csh',
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.url, data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)
        self.assertTrue('template saved' in r.content)
        template_path = '/Users/baldwin32/projects/acme-web-fe/apps/run_manager/resources//test/ACME_script.csh'
        shutil.rmtree(template_path, ignore_errors=True)

    def test_invalid_run(self):
        request = {
            'run_name': 'test_run',
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.live_server_url + '/run_manager/create_run/', data=json.dumps(request), content_type='application/json')

        request = {
            'run_name': 'test_run',
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.live_server_url + '/run_manager/create_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 409)


class TestDeleteRun(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user2 = User.objects.create(username='test2')
        self.user.set_password('test')
        self.user2.set_password('test')
        self.user.save()
        self.user2.save()
        self.c = Client()
        self.c2 = Client()

        logged_in = self.c.login(username='test', password='test')
        logged_in = self.c2.login(username='test2', password='test')

    def tearDown(self):
        path = os.path.abspath(os.path.dirname(__file__))
        run_directory = path + RUN_SCRIPT_PATH + 'test'
        shutil.rmtree(run_directory, ignore_errors=True)

    def test_delete_valid_run(self):
        request = {
            'run_name': 'test_run',
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.live_server_url + '/run_manager/create_run/', data=json.dumps({'run_name': 'test_run'}), content_type='application/json')
        r = self.c.post(self.live_server_url + '/run_manager/delete_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        path = os.path.abspath(os.path.dirname(__file__))
        run_directory = path + RUN_SCRIPT_PATH + 'test/test_run'
        print_message('run directory still exists {}'.format(run_directory), 'error')
        self.assertFalse(os.path.exists(run_directory))

    def test_delete_run_invalid_user(self):
        request = {
            'run_name': 'test_run',
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.live_server_url + '/run_manager/create_run/', data=json.dumps(request), content_type='application/json')
        r = self.c2.post(self.live_server_url + '/run_manager/delete_run/', data=json.dumps(request), content_type='application/json')
        self.assertTrue(r.status_code == 401)
        path = os.path.abspath(os.path.dirname(__file__))
        run_directory = path + RUN_SCRIPT_PATH + 'test/test_run'
        print_message('run directory was removed {}'.format(run_directory), 'error')
        self.assertTrue(os.path.exists(run_directory))
        # c is cleaning up
        r = self.c.post(self.live_server_url + '/run_manager/delete_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

    def test_delete_run_invalid_run_name(self):
        request = {
            'asdf': 'test_run'
        }
        r = self.c2.post(self.live_server_url + '/run_manager/delete_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_delete_run_does_not_exist(self):
        request = {
            'run_name': 'this_does_not_exist'
        }
        r = self.c2.post(self.live_server_url + '/run_manager/delete_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code != 400)


class TestCreateScript(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')

    def test_create_script(self):
        request = {
            'run_name': 'test_run_name',
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.live_server_url + '/run_manager/create_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': 'script_test',
            'run_name': 'test_run_name',
            'contents': 'Hello World'
        }
        r = self.c.post(self.live_server_url + '/run_manager/create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'run_name': 'test_run_name'
        }

    def test_create_script_without_login(self):
        self.c2 = Client()

        request = {
            'script_name': 'test_name',
            'run_name': 'test_run_name',
            'contents': 'Hello World'
        }
        r = self.c2.post(self.live_server_url + '/run_manager/create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 302)

    def test_create_script_missing_script_name(self):
        request = {
            'run_name': 'test_run_name',
            'contents': 'Hello World'
        }
        r = self.c.post(self.live_server_url + '/run_manager/create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_create_script_without_run_name(self):
        request = {
            'script_name': 'test_name',
            'contents': 'Hello World'
        }
        r = self.c.post(self.live_server_url + '/run_manager/create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_create_script_without_content(self):
        request = {
            'script_name': 'test_name',
            'run_name': 'test_run_name',
        }
        r = self.c.post(self.live_server_url + '/run_manager/create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_create_script_with_blank_script_name(self):
        request = {
            'script_name': '',
            'run_name': 'test_run_name',
            'contents': 'Hello World'
        }
        r = self.c.post(self.live_server_url + '/run_manager/create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_create_script_with_blank_run_name(self):
        request = {
            'script_name': 'test_name',
            'run_name': '',
            'contents': 'Hello World'
        }
        r = self.c.post(self.live_server_url + '/run_manager/create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_create_script_with_blank_contents(self):
        request = {
            'script_name': 'test_name',
            'run_name': 'test_run_name',
            'contents': ''
        }
        r = self.c.post(self.live_server_url + '/run_manager/create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_create_script_with_invalid_run(self):
        request = {
            'script_name': 'test_name',
            'run_name': 'not_a_run_name',
            'contents': 'Hello World'
        }
        r = self.c.post(self.live_server_url + '/run_manager/create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)


class TestGetRuns(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')
        self.url = self.live_server_url + '/run_manager/view_runs/'

    def tearDown(self):
        path = os.path.abspath(os.path.dirname(__file__))
        run_directory = path + RUN_SCRIPT_PATH + 'test'
        shutil.rmtree(run_directory, ignore_errors=True)

    def test_get_runs_valid_user(self):
        request = json.dumps({
            'run_name': 'test_run',
            'run_type': 'diagnostic'
        })
        r = self.c.post(self.live_server_url + '/run_manager/create_run/', data=request, content_type='application/json')
        print_message('status code given {}'.format(str(r.status_code)), 'error')
        self.assertTrue(r.status_code == 200)
        r = self.c.get(self.url)
        print_message("request contents {}".format(r.content), 'error')
        self.assertTrue(r.status_code == 200)
        self.assertTrue('test_run' in r.content)

    def test_get_runs_invalid_user(self):
        c2 = Client()
        r = c2.get(self.url)
        self.assertTrue(r.status_code == 302)


class TestUpdateScript(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')
        self.url = self.live_server_url + '/run_manager/'

    def tearDown(self):
        path = os.path.abspath(os.path.dirname(__file__))
        run_directory = path + RUN_SCRIPT_PATH + 'test'
        shutil.rmtree(run_directory, ignore_errors=True)

    def test_update_script(self):
        run_name = 'update_script_run1'
        script_name = 'update_script_name'
        script_contents = 'update script contents'

        request = {
            'run_name': run_name,
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.url + 'create_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents
        }
        r = self.c.post(self.url + 'create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents + ' ver 2'
        }
        r = self.c.post(self.url + 'update_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

    def test_update_script_without_script_name(self):
        run_name = 'update_script_run2'
        script_name = 'update_script_name'
        script_contents = 'update script contents'

        request = {
            'run_name': run_name,
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.url + 'create_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents
        }
        r = self.c.post(self.url + 'create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'run_name': run_name,
            'contents': script_contents + ' ver 2'
        }
        r = self.c.post(self.url + 'update_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_update_script_without_run_name(self):
        run_name = 'update_script_run3'
        script_name = 'update_script_name'
        script_contents = 'update script contents'

        request = {
            'run_name': run_name,
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.url + 'create_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents
        }
        r = self.c.post(self.url + 'create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'contents': script_contents + ' ver 2'
        }
        r = self.c.post(self.url + 'update_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)
        # Any way to check the contents without relying on readscript?

    def test_update_script_without_contents(self):
        run_name = 'update_script_run4'
        script_name = 'update_script_name'
        script_contents = 'update script contents'

        request = {
            'run_name': run_name,
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.url + 'create_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents
        }
        r = self.c.post(self.url + 'create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name
        }
        r = self.c.post(self.url + 'update_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)
        # Any way to check the contents without relying on readscript?

    def test_update_script_with_non_existent_run_name(self):
        run_name = 'test_run_name1'
        script_name = 'script_name'
        script_contents = 'update script contents'

        request = {
            'run_name': run_name,
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.url + 'create_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents
        }
        r = self.c.post(self.url + 'create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': 'not_a_script',
            'run_name': run_name,
            'contents': 'Should fail'
        }
        r = self.c.post(self.url + 'update_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 404)


class TestReadScript(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')
        self.url = self.live_server_url + '/run_manager/'

    def tearDown(self):
        path = os.path.abspath(os.path.dirname(__file__))
        run_directory = path + RUN_SCRIPT_PATH + 'test'
        shutil.rmtree(run_directory, ignore_errors=True)

    def test_get_a_script(self):
        run_name = 'read_script_run1'
        script_name = 'read_script_name'
        script_contents = 'Hello World'

        request = {
            'run_name': run_name,
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.url + 'create_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents
        }
        r = self.c.post(self.url + 'create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)
        request = {
            'script_name': script_name,
            'run_name': run_name,
        }
        r = self.c.get(self.url + 'read_script/', request)
        self.assertTrue(r.status_code == 200)
        data = json.loads(r.content)
        self.assertEquals(script_contents, data['script'])

    def test_read_script_with_version(self):
        run_name = 'read_script_run2'
        script_name = 'read_script_name'
        script_contents = 'Hello World'
        new_script_contents = 'Hello World Version 2'

        request = {
            'run_name': run_name,
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.url + 'create_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents
        }
        r = self.c.post(self.url + 'create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
        }
        r = self.c.get(self.url + 'read_script/', request)
        self.assertTrue(r.status_code == 200)
        data = json.loads(r.content)
        self.assertEquals(script_contents, data['script'])

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': new_script_contents
        }
        r = self.c.post(self.url + 'update_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'version': 2
        }
        r = self.c.get(self.url + 'read_script/', request)
        self.assertTrue(r.status_code == 200)
        data = json.loads(r.content)
        self.assertEquals(new_script_contents, data['script'])


class TestGetScripts(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')
        self.url = self.live_server_url + '/run_manager/'

    def tearDown(self):
        path = os.path.abspath(os.path.dirname(__file__))
        run_directory = path + RUN_SCRIPT_PATH + 'test'
        shutil.rmtree(run_directory, ignore_errors=True)

    def test_get_scripts(self):
        run_name = 'get_scripts_run'
        script_name1 = 'first_script_name'
        script_contents1 = 'Hello World'
        script_name2 = 'second_script_name'
        script_contents2 = 'Many scripts. Handle it'
        request = {
            'run_name': run_name,
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.url + 'create_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name1,
            'run_name': run_name,
            'contents': script_contents1
        }
        r = self.c.post(self.url + 'create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name2,
            'run_name': run_name,
            'contents': script_contents2
        }
        r = self.c.post(self.url + 'create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'run_name': run_name,
        }
        r = self.c.get(self.url + 'get_scripts/', request, content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        data = json.loads(r.content)
        self.assertTrue(script_name1 in data)
        self.assertTrue(script_name2 in data)

    def test_get_scripts_without_run_name(self):
        run_name = 'get_scripts_run'
        script_name1 = 'first_script_name'
        script_contents1 = 'Hello World'
        script_name2 = 'second_script_name'
        script_contents2 = 'Many scripts. Handle it'
        request = {
            'run_name': run_name,
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.url + 'create_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name1,
            'run_name': run_name,
            'contents': script_contents1
        }
        r = self.c.post(self.url + 'create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name2,
            'run_name': run_name,
            'contents': script_contents2
        }
        r = self.c.post(self.url + 'create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {}
        r = self.c.get(self.url + 'get_scripts/', request, content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_get_scripts_with_invalid_run_name(self):
        run_name = 'valid_run'
        script_name1 = 'first_script_name'
        script_contents1 = 'Hello World'
        script_name2 = 'second_script_name'
        script_contents2 = 'Many scripts. Handle it'
        request = {
            'run_name': run_name,
            'run_type': 'diagnostic'
        }
        r = self.c.post(self.url + 'create_run/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name1,
            'run_name': run_name,
            'contents': script_contents1
        }
        r = self.c.post(self.url + 'create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name2,
            'run_name': run_name,
            'contents': script_contents2
        }
        r = self.c.post(self.url + 'create_script/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'run_name': 'invalid_run'
        }
        r = self.c.get(self.url + 'get_scripts/', request, content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 403)


class TestStartRun(LiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.username = 'test'
        self.c = Client()
        self.c.login(username='test', password='test')
        self.url = self.live_server_url + '/run_manager/start_run/'
        self.run_name = 'start_test_run'

    def tearDown(self):
        path = os.path.abspath(os.path.dirname(__file__))
        run_directory = path + RUN_SCRIPT_PATH + self.username + '/' + self.run_name
        shutil.rmtree(run_directory, ignore_errors=True)

    # THIS IS A MANUAL TEST, MAKE SURE THIS IS COMMETED BEFORE RUNNING ON TRAVIS
    # def test_start_run(self):
    #     request = {
    #         'run_name': self.run_name,
    #         'run_type': 'diagnostic'
    #     }
    #     r = self.c.post(self.live_server_url + '/run_manager/create_run/', data=json.dumps(request), content_type='application/json')
    #     print_message('status code given ' + str(r.status_code), 'error')
    #     self.assertTrue(r.status_code == 200)
    #     request = json.dumps({
    #         'run_name': self.run_name
    #     })
    #     r = self.c.post(self.url, data=request, content_type='application/json')
    #     print_message('status code given ' + str(r.status_code), 'error')
    #     self.assertTrue(r.status_code == 200)


class TestGetStatus(LiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.username = 'test'
        self.c = Client()
        self.c.login(username='test', password='test')
        self.url = self.live_server_url + '/run_manager/start_run/'

    def test_get_run_status(self):
        r = self.c.get(self.live_server_url + '/run_manager/run_status/')
        print_message(r.content)
        self.assertTrue(r.status_code == 200)
        self.assertTrue('user' in r.content)


class TestGetTemplates(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.username = 'test'
        self.c = Client()
        self.c.login(username='test', password='test')
        self.c = Client()
        self.c2 = Client()
        logged_in = self.c.login(username='test', password='test')
        self.url = self.live_server_url + '/run_manager/'

    def test_get_templates(self):
        r = self.c.get(self.url + 'get_templates/', content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)
        data = json.loads(r.content)
        self.assertTrue('global/ACME_script.csh' in data)
        # Todo: update this test with more checks when add templates is a thing

    def test_get_templates_without_log_in(self):
        r = self.c2.get(self.url + 'get_templates/', content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 302)


class TestCopyTemplates(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.c = Client()
        self.c2 = Client()
        logged_in = self.c.login(username='test', password='test')
        self.url = self.live_server_url + '/run_manager/'

    def test_copy_a_template(self):
        request = {
            'template': 'ACME_script.csh',
            'new_template': 'copy_template'
        }
        r = self.c.post(self.url + 'copy_template/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)
        r = self.c.get(self.url + 'get_templates/', content_type='application/json')
        data = json.loads(r.content)
        print_message('templates found: ' + str(data), 'error')
        self.assertTrue('global/ACME_script.csh' in data)
        self.assertTrue('test/copy_template' in data)

    def test_copy_template_without_old_template(self):
        request = {
            'new_template': 'copy_template'
        }
        r = self.c.post(self.url + 'copy_template/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_copy_template_without_new_template(self):
        request = {
            'new_template': 'ACME_script.csh'
        }
        r = self.c.post(self.url + 'copy_template/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_copy_template_with_invalid_old_template(self):
        request = {
            'template': 'this_doesnt_exist',
            'new_template': 'invalid_copy_template'
        }
        r = self.c.post(self.url + 'copy_template/', data=json.dumps(request), content_type='application/json')
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)
        data = json.loads(r.content)
        self.assertTrue('error' in data and data['error'] == 'template not found')
