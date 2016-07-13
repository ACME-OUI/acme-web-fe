from django.test import TestCase
from django.test import LiveServerTestCase
from django.test import Client
from django.contrib.auth.models import User
import json
import shutil
import os
from constants import RUN_SCRIPT_PATH
from util.utilities import print_message

class TestCreateRun(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.c = Client()
        self.url = self.live_server_url + '/acme/run_manager/create_run/'
        logged_in = self.c.login(username='test', password='test')

    def tearDown(self):
        path = os.path.abspath(os.path.dirname(__file__))
        run_directory = path + RUN_SCRIPT_PATH + 'test'
        shutil.rmtree(run_directory, ignore_errors=True)

    def test_valid_run(self):
        request = {
            'run_name': 'test_run'
        }
        r = self.c.post(self.url, request)
        print_message('status code given' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

    def test_create_run_with_valid_template(self):
        request = {
            'run_name': 'test_run_with_template',
            'template': 'ACME_script.csh'
        }
        r = self.c.post(self.url, request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)
        self.assertTrue('template saved' in r.content)
        template_path = '/Users/baldwin32/projects/acme-web-fe/apps/run_manager/resources//test/ACME_script.csh'
        shutil.rmtree(template_path, ignore_errors=True)


    def test_invalid_run(self):
        request = {
            'run_name': 'test_run'
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/create_run/', request)

        request = {
            'run_name': 'test_run'
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/create_run/', request)
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


    def test_delete_valid_run(self):
        request = {
            'run_name': 'test_run'
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/create_run/', {'run_name': 'test_run'})
        r = self.c.post(self.live_server_url + '/acme/run_manager/delete_run/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        path = os.path.abspath(os.path.dirname(__file__))
        run_directory = path + RUN_SCRIPT_PATH +  'test/test_run'
        print_message('run directory still exists {}'.format(run_directory), 'error')
        self.assertFalse(os.path.exists(run_directory))


    def test_delete_run_invalid_user(self):
        request = {
            'run_name': 'test_run'
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/create_run/', request)
        r = self.c2.post(self.live_server_url + '/acme/run_manager/delete_run/', request)
        self.assertTrue(r.status_code == 401)
        path = os.path.abspath(os.path.dirname(__file__))
        run_directory = path + RUN_SCRIPT_PATH +  'test/test_run'
        print_message('run directory was removed {}'.format(run_directory), 'error')
        self.assertTrue(os.path.exists(run_directory))
        # c is cleaning up
        r = self.c.post(self.live_server_url + '/acme/run_manager/delete_run/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)


    def test_delete_run_invalid_run_name(self):
        request = {
            'asdf': 'test_run'
        }
        r = self.c2.post(self.live_server_url + '/acme/run_manager/delete_run/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_delete_run_does_not_exist(self):
        request = {
            'run_name': 'this_does_not_exist'
        }
        r = self.c2.post(self.live_server_url + '/acme/run_manager/delete_run/', request)
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
            'run_name': 'test_run_name'
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/create_run/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': 'script_test',
            'run_name': 'test_run_name',
            'contents': 'Hello World'
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/create_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'run_name': 'test_run_name'
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/delete_run/', request)
        if r.status_code != 200:
            print_message('failed to delete run {}'.format(request), 'error')
            print_message('status_code: {}'.format(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

    def test_create_script_without_login(self):
        self.c2 = Client()

        request = {
            'script_name': 'test_name',
            'run_name': 'test_run_name',
            'contents': 'Hello World'
        }
        r = self.c2.post(self.live_server_url + '/acme/run_manager/create_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 302)

    def test_create_script_missing_script_name(self):
        request = {
            'run_name': 'test_run_name',
            'contents': 'Hello World'
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/create_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_create_script_without_run_name(self):
        request = {
            'script_name': 'test_name',
            'contents': 'Hello World'
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/create_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_create_script_without_content(self):
        request = {
            'script_name': 'test_name',
            'run_name': 'test_run_name',
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/create_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_create_script_with_blank_script_name(self):
        request = {
            'script_name': '',
            'run_name': 'test_run_name',
            'contents': 'Hello World'
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/create_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_create_script_with_blank_run_name(self):
        request = {
            'script_name': 'test_name',
            'run_name': '',
            'contents': 'Hello World'
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/create_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_create_script_with_blank_contents(self):
        request = {
            'script_name': 'test_name',
            'run_name': 'test_run_name',
            'contents': ''
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/create_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

    def test_create_script_with_invalid_run(self):
        request = {
            'script_name': 'test_name',
            'run_name': 'not_a_run_name',
            'contents': 'Hello World'
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/create_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)



class TestGetRuns(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')
        self.url = self.live_server_url + '/acme/run_manager/view_runs/'

    def test_get_runs_valid_user(self):
        r = self.c.post(self.live_server_url + '/acme/run_manager/create_run/', {'run_name': 'test_run'})
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
        self.url = self.live_server_url + '/acme/run_manager/'

    def test_update_script(self):
        run_name = 'update_script_run1'
        script_name = 'update_script_name'
        script_contents = 'update script contents'

        request = {
            'run_name': run_name
        }
        r = self.c.post(self.url + 'create_run/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents
        }
        r = self.c.post(self.url + 'create_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents + ' ver 2'
        }
        r = self.c.post(self.url + 'update_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'run_name': run_name
        }
        r = self.c.post(self.url + 'delete_run/', request)
        if r.status_code != 200:
            print_message('failed to delete run {}'.format(request), 'error')
            print_message('status_code: {}'.format(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

    def test_update_script_without_script_name(self):
        run_name = 'update_script_run2'
        script_name = 'update_script_name'
        script_contents = 'update script contents'

        request = {
            'run_name': run_name
        }
        r = self.c.post(self.url + 'create_run/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents
        }
        r = self.c.post(self.url + 'create_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'run_name': run_name,
            'contents': script_contents + ' ver 2'
        }
        r = self.c.post(self.url + 'update_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)

        request = {
            'run_name': run_name
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/delete_run/', request)
        if r.status_code != 200:
            print_message('failed to delete run {}'.format(request), 'error')
            print_message('status_code: {}'.format(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

    def test_update_script_without_run_name(self):
        run_name = 'update_script_run3'
        script_name = 'update_script_name'
        script_contents = 'update script contents'

        request = {
            'run_name': run_name
        }
        r = self.c.post(self.url + 'create_run/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents
        }
        r = self.c.post(self.url + 'create_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'contents': script_contents + ' ver 2'
        }
        r = self.c.post(self.url + 'update_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)
        # Any way to check the contents without relying on readscript?

        request = {
            'run_name': run_name
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/delete_run/', request)
        if r.status_code != 200:
            print_message('failed to delete run {}'.format(request), 'error')
            print_message('status_code: {}'.format(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

    def test_update_script_without_contents(self):
        run_name = 'update_script_run4'
        script_name = 'update_script_name'
        script_contents = 'update script contents'

        request = {
            'run_name': run_name
        }
        r = self.c.post(self.url + 'create_run/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents
        }
        r = self.c.post(self.url + 'create_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name
        }
        r = self.c.post(self.url + 'update_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 400)
        # Any way to check the contents without relying on readscript?

        request = {
            'run_name': run_name
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/delete_run/', request)
        if r.status_code != 200:
            print_message('failed to delete run {}'.format(request), 'error')
            print_message('status_code: {}'.format(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

    def test_update_script_with_non_existent_run_name(self):
        run_name = 'test_run_name1'
        script_name = 'script_name'
        script_contents = 'update script contents'

        request = {
            'run_name': run_name
        }
        r = self.c.post(self.url + 'create_run/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents
        }
        r = self.c.post(self.url + 'create_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': 'not_a_script',
            'run_name': run_name,
            'contents': 'Should fail'
        }
        r = self.c.post(self.url + 'update_script/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 404)

        request = {
            'run_name': run_name
        }
        r = self.c.post(self.url + 'delete_run/', request)
        if r.status_code != 200:
            print_message('failed to delete run {}'.format(request), 'error')
            print_message('status_code: {}'.format(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)


class TestReadScript(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')
        self.url = self.live_server_url + '/acme/run_manager/'

    def test_get_a_script(self):
        run_name = 'read_script_run1'
        script_name = 'read_script_name'
        script_contents = 'Hello World'

        request = {
            'run_name': run_name
        }
        r = self.c.post(self.url + 'create_run/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents
        }
        r = self.c.post(self.url + 'create_script/', request)
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
            'run_name': run_name
        }
        r = self.c.post(self.url + 'delete_run/', request)
        if r.status_code != 200:
            print_message('failed to delete run {}'.format(request), 'error')
            print_message('status_code: {}'.format(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

    def test_read_script_with_version(self):
        run_name = 'read_script_run2'
        script_name = 'read_script_name'
        script_contents = 'Hello World'
        new_script_contents = 'Hello World Version 2'

        request = {
            'run_name': run_name
        }
        r = self.c.post(self.url + 'create_run/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

        request = {
            'script_name': script_name,
            'run_name': run_name,
            'contents': script_contents
        }
        r = self.c.post(self.url + 'create_script/', request)
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
        r = self.c.post(self.url + 'update_script/', request)
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

        request = {
            'run_name': run_name
        }
        r = self.c.post(self.url + 'delete_run/', request)
        if r.status_code != 200:
            print_message('failed to delete run {}'.format(request), 'error')
            print_message('status_code: {}'.format(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

# class TestGetScripts(LiveServerTestCase):
#
#     def test_get_scripts(self):

# class TestUpdateScript(LiveServerTestCase):
#
#     def test_update_valid_script(self):
#         self.assertTrue(False)
#
#     def test_update_invalid_script(self):
#         self.assertTrue(False)
#
#

# class TestGetScripts(LiveServerTestCase):
#
#     def test_get_scripts_valid_run(self):
#         self.assertTrue(False)
#
#     def test_get_scripts_invalid_run(self):
#         self.assertTrue(False)
#
#
# class TestCreateTemplate(LiveServerTestCase):
#
#     def test_create_template_valid_user(self):
#         self.assertTrue(False)
#
#     def test_create_template_invalid_user(self):
#         self.assertTrue(False)
#
#
# class TestGetTemplates(LiveServerTestCase):
#
#     def test_get_template_valid_user(self):
#         self.assertTrue(False)
#
#     def test_get_template_invalid_user(self):
#         self.assertTrue(False)
#
#
# class TestDeleteTemplate(LiveServerTestCase):
#
#     def test_delete_template_valid_user(self):
#         self.assertTrue(False)
#
#     def test_delete_template_invalid_user(self):
#         self.assertTrue(False)
