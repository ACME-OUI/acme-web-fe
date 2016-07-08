from django.test import TestCase
from django.test import LiveServerTestCase
from django.test import Client
from django.contrib.auth.models import User
import json
import requests
import shutil
import os
from constants import RUN_SCRIPT_PATH

class TestCreateRun(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('test')
        self.user.save()
        self.c = Client()
        logged_in = self.c.login(username='test', password='test')

    def tearDown(self):
        # run_directory = '/Users/baldwin32/projects/acme-web-fe/run_manager/run_scripts/test/test_run'
        path = os.path.abspath(os.path.dirname(__file__))
        run_directory = path + RUN_SCRIPT_PATH
        shutil.rmtree(run_directory, ignore_errors=True)

    def test_valid_run(self):
        request = {
            'run_name': 'test_run'
        }
        r = self.c.get(self.live_server_url + '/acme/run_manager/create_run/', request)
        print r.status_code
        self.assertTrue(r.status_code == 200)


    def test_invalid_run(self):
        request = {
            'run_name': 'test_run'
        }
        r = self.c.get(self.live_server_url + '/acme/run_manager/create_run/', request)
        request = {
            'run_name': 'test_run'
        }
        r = self.c.get(self.live_server_url + '/acme/run_manager/create_run/', request)
        if r.status_code != 409:
            print r.status_code
        self.assertTrue(r.status_code == 409)


# class TestDeleteRun(LiveServerTestCase):
#
#     def test_delete_valid_run(self):
#         self.assertTrue(False)
#
#     def test_delete_invalid_run(self):
#         self.assertTrue(False)
#

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
