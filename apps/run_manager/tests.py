from django.test import TestCase
from django.test import LiveServerTestCase
from django.test import Client
from django.contrib.auth.models import User
import json
import requests
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
        run_directory = path + RUN_SCRIPT_PATH
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

        # setup the delete test by creating a new run
        # r = self.c.post(self.live_server_url + '/acme/run_manager/create_run/', {'run_name': 'test_run'})


    def test_delete_valid_run(self):
        request = {
            'run_name': 'test_run'
        }
        r = self.c.post(self.live_server_url + '/acme/run_manager/create_run/', {'run_name': 'test_run'})
        r = self.c.post(self.live_server_url + '/acme/run_manager/delete_run/', request)
        print_message('status code given ' + str(r.status_code), 'error')
        self.assertTrue(r.status_code == 200)

    def test_delete_run_invalid_user(self):
        request = {
            'run_name': 'test_run'
        }
        r = self.c2.post(self.live_server_url + '/acme/run_manager/delete_run/', request)
        self.assertTrue(r.status_code != 200)


# class TestUpdateScript(LiveServerTestCase):
#
#     def test_update_valid_script(self):
#         self.assertTrue(False)
#
#     def test_update_invalid_script(self):
#         self.assertTrue(False)
#
#
# class TestGetRuns(LiveServerTestCase):
#
#     def test_get_runs_valid_user(self):
#         self.assertTrue(False)
#
#     def test_get_runs_invalid_user(self):
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
