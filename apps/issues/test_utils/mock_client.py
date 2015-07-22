from issues.api_client import APIClient, DictBacked


class MockClient(APIClient):
    """
    Abstract class for wrapping API clients with the functions that I actually want from them
    """
    def __init__(self, model_type, auth=None):
        super(MockClient, self).__init__('', auth=auth)
        self.type = model_type

    @property
    def client(self):
        """
        Delay client initialization till we're actually needing it
        """
        if self._client is None:
            self.authenticate()
        return self._client

    def update(self, model, issue):
        return

    def authenticate(self):
        return

    def get_labels(self):
        return []

    def submit_issue(self, category, title, description):
        if self.type == "github":
            url = "https://api.github.com/repos/ACME-OUI/acme-web-fe/issues/81"
        elif self.type == 'jira':
            url = "https://acme-climate.atlassian.net/rest/api/2/issue/WG-111"

        return DictBacked(url=url, api=None)

    def get_issue(self, issue):
        if self.type == "github":
            url = "https://github.com/ACME-OUI/acme-web-fe/issues/81"
            title = "Testing Login"
        elif self.type == "jira":
            url = "https://acme-climate.atlassian.net/browse/WG-111"
            title = "Testing Login"

        return DictBacked(web_url=url, name=title, api=None)

    def get_representation(self, json):
        title = "Testing Login"
        text = """using [robot](http://robotframework.org) write a [Selenium](http://www.seleniumhq.org) test:

    Valid user login
    Non-valid user login
    using [PyUnit](http://pyunit.sourceforge.net) write a unit test for:
    Registration view [function](https://github.com/ACME-OUI/acme-web-fe/blob/master/apps/web_fe/views.py#L47)"""
        if self.type == "github":
            web_url = "https://github.com/ACME-OUI/acme-web-fe/issues/81"
            api_url = "https://api.github.com/repos/ACME-OUI/acme-web-fe/issues/81"
            author = "mattben"
            labels = ["Sprint 2"]
        elif self.type == "jira":
            web_url = "https://acme-climate.atlassian.net/browse/WG-111"
            api_url = "https://acme-climate.atlassian.net/rest/api/2/issue/WG-111"
            author = "fries2@llnl.gov"
            labels = ["Sprint-2"]
        return DictBacked(url=api_url, web=web_url, title=title, author=author, labels=labels, text=text, type=self.type, backing=None)

    def create_issue(self, representation):
        return self.get_representation(None)

    def close_issue(self, issue, days, hours, minutes):
        return

    def open_issue(self, issue):
        return
