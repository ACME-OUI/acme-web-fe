from django.utils import unittest
from django.test.client import Client
from django.contrib.auth.models import User
from issues.views import *
from issues.models import *
from django.core.management import call_command


def userSetup(test):
    # First create a new user
    test.test_user = User.objects.create_user(
        'testuser', 'test@test.test', 'testpass')
    # Now login as that user
    test.client = Client()
    test.client.login(username='testuser', password='testpass')


def acme_web_fe_source():
    try:
        s = IssueSource.get(name="acme-web-fe")
    except IssueSource.DoesNotExist:
        # acme-web-fe project on github
        s = IssueSource()
        s.name = "acme-web-fe"
        s.base_url = "https://api.github.com/repos/ACME-OUI/acme-web-fe"
        s.source_type = "github"
        s.required_info = "None"
        s.save()
    return s


def n_to_n_ui_source():
    try:
        s = IssueSource.get(name="n-to-n-ui")
    except IssueSource.DoesNotExist:
        # acme-web-fe project on github
        s = IssueSource()
        s.name = "n-to-n-ui"
        s.base_url = "https://acme-climate.atlassian.net/rest/api/2/component/10300"
        s.source_type = "jira"
        s.required_info = "None"
        s.save()
    return s


class IssueSourceTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.gh_source = None
        self.jira_source = None
        super(IssueSourceTest, self).__init__(*args, **kwargs)

    def setUp(self):
        userSetup(self)
        self.gh_source = acme_web_fe_source()
        self.jira_source = n_to_n_ui_source()

    def tearDown(self):
        self.test_user.delete()
        self.source.delete()

    def test_is_github(self):
        self.assertTrue(self.gh_source.is_github())
        self.assertFalse(self.jira_source.is_github())

    def test_is_jira(self):
        self.assertFalse(self.gh_source.is_jira())
        self.assertTrue(self.jira_source.is_jira())

    def test_client(self):
        self.assertTrue(self.gh_source.client is not None)
        self.assertTrue(self.jira_source.client is not None)

    def test_get_labels(self):
        try:
            labels = self.gh_source.get_labels()
            labels = self.jira_source.get_labels()
        except Exception:
            self.assertTrue(False)

    def test_submit_issue(self, category, title, description, parent_issue=None):
        pass

    def test_create_issue(self, i, parent=None):
        pass

    def test_get_issue(self, issue):
        pass

    def test_cyclic_links(self):
        pass
