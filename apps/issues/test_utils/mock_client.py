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
            return "https://api.github.com/repo/ACME-OUI/acme-web-fe/issues/86"
        if self.type == 'jira':
            return "https://acme-climate.atlassian.net/rest/api/2/issues/WG-111"

    def get_issue(self, issue):
        raise NotImplementedError("get_issue not implemented for %s" % type(self))

    def get_representation(self, json):
        raise NotImplementedError("get_representation not implemented for %s" % type(self))

    def create_issue(self, representation):
        raise NotImplementedError("create_issue not implemented for %s" % type(self))

    def close_issue(self, issue, days, hours, minutes):
        raise NotImplementedError("close_issue not implemented for %s" % type(self))

    def open_issue(self, issue):
        raise NotImplementedError("open_issue not implemented for %s" % type(self))