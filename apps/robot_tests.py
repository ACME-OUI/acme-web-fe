from django.contrib.staticfiles.testing import StaticLiveServerTestCase as LiveServerTestCase
from django.core.management import call_command
from issues.models import *
from web_fe.models import Credential
import robot
import os
from django.contrib.auth.models import User


def init_db():
    """
    Used to prepopulate DB with data for manipulation
    """
    User.objects.create_user('testuser', 'test@test.test', 'testpass')
    Credential(service="velo", site_user_name="testuser", service_user_name="acmetest", password="acmetest").save()
    issues_db()


def issues_db():
    # acme-web-fe project on github
    s = IssueSource()
    s.name = "acme-web-fe"
    s.base_url = "https://api.github.com/repos/ACME-OUI/acme-web-fe"
    s.source_type = "github"
    s.required_info = "None"
    s.save()

    s = IssueSource()
    s.name = "n-to-n-ui"
    s.base_url = "https://acme-climate.atlassian.net/rest/api/2/component/10300"
    s.source_type = "jira"
    s.required_info = "None"
    s.save()

    call_command("getlabels")


class RobotTest(LiveServerTestCase):

    def setUp(self):
        init_db()

    def test_robot(self):
        """
        Invoke robot tests
        """
        r_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests", "robot")
        self.assertEqual(robot.run(r_path), 1, "Robot Tests failed")
