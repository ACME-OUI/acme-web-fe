from django.utils import unittest
from django.test.client import Client
from django.contrib.auth.models import User
from issues.views import *
from issues.models import *
from django.core.management import call_command
from django.core.exceptions import ValidationError
from test_utils.mock_client import MockClient


def userSetup(test):
    # First create a new user
    test.test_user = User.objects.create_user(
        'testuser', 'test@test.test', 'testpass')
    # Now login as that user
    test.client = Client()
    test.client.login(username='testuser', password='testpass')


def acme_web_fe_source():
    try:
        s = IssueSource.objects.get(name="acme-web-fe")
    except IssueSource.DoesNotExist:
        # acme-web-fe project on github
        s = IssueSource()
        s.name = "acme-web-fe"
        s.base_url = "https://api.github.com/repos/ACME-OUI/acme-web-fe"
        s.source_type = "github"
        s.required_info = "None"
        s.save()
        s._client = MockClient("github")
    return s


def n_to_n_ui_source():
    try:
        s = IssueSource.objects.get(name="n-to-n-ui")
    except IssueSource.DoesNotExist:
        # acme-web-fe project on github
        s = IssueSource()
        s.name = "n-to-n-ui"
        s.base_url = "https://acme-climate.atlassian.net/rest/api/2/component/10300"
        s.source_type = "jira"
        s.required_info = "None"
        s.save()
        s._client = MockClient("jira")
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
        self.gh_source.delete()
        self.jira_source.delete()

    def test_is_github(self):
        self.assertTrue(self.gh_source.is_github(), "GitHub source not reporting as GitHub")
        self.assertFalse(self.jira_source.is_github(), "JIRA source reporting as GitHub")

    def test_is_jira(self):
        self.assertFalse(self.gh_source.is_jira(), "GitHub source reported as JIRA")
        self.assertTrue(self.jira_source.is_jira(), "JIRA source not reporting as JIRA")

    def test_client(self):
        self.assertTrue(self.gh_source.client is not None, "Client property not initialized (GitHub)")
        self.assertTrue(self.jira_source.client is not None, "Client property not initialized (JIRA)")

    def test_cyclic_links(self):
        self.gh_source.linked = self.jira_source
        self.jira_source.linked = self.gh_source
        try:
            self.gh_source.save()
            self.jira_source.full_clean()
            if self.gh_source == self.jira_source.linked and self.jira_source == self.gh_source.linked:
                self.assertTrue(False, "Cyclic link found.")
        except ValidationError:
            pass
        else:
            self.assertTrue(False, "Cyclic Links allowed in IssueSource.linked")
