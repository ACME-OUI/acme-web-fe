from django.test import TestCase
from django.test import LiveServerTestCase
import json
import requests


class TestCreateRun(LiveServerTestCase):

    def test_valid_run(self):
        self.assertTrue(False)

    def test_invalid_run(self):
        self.assertTrue(False)


class TestDeleteRun(LiveServerTestCase):

    def test_delete_valid_run(self):
        self.assertTrue(False)

    def test_delete_invalid_run(self):
        self.assertTrue(False)


class TestUpdateScript(LiveServerTestCase):

    def test_update_valid_script(self):
        self.assertTrue(False)

    def test_update_invalid_script(self):
        self.assertTrue(False)


class TestGetRuns(LiveServerTestCase):

    def test_get_runs_valid_user(self):
        self.assertTrue(False)

    def test_get_runs_invalid_user(self):
        self.assertTrue(False)


class TestGetScripts(LiveServerTestCase):

    def test_get_scripts_valid_run(self):
        self.assertTrue(False)

    def test_get_scripts_invalid_run(self):
        self.assertTrue(False)


class TestCreateTemplate(LiveServerTestCase):

    def test_create_template_valid_user(self):
        self.assertTrue(False)

    def test_create_template_invalid_user(self):
        self.assertTrue(False)


class TestGetTemplates(LiveServerTestCase):

    def test_get_template_valid_user(self):
        self.assertTrue(False)

    def test_get_template_invalid_user(self):
        self.assertTrue(False)


class TestDeleteTemplate(LiveServerTestCase):

    def test_delete_template_valid_user(self):
        self.assertTrue(False)

    def test_delete_template_invalid_user(self):
        self.assertTrue(False)
