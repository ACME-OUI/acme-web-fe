from github3 import login as gh_login
from jira.client import JIRA
import urlparse


class DictBacked(object):
    """
    APIClients will stick relevant info into this label class
    """
    def __init__(self, **args):
        self._backing = args
        super(DictBacked, self).__init__()

    def __getattribute__(self, attribute):
        try:
            return object.__getattribute__(self, "_backing")[attribute]
        except KeyError:
            raise AttributeError("'DictBacked' does not have an attribute %s" % attribute)


class APIClient(object):
    """
    Abstract class for wrapping API clients with the functions that I actually want from them
    """
    def __init__(self, url, auth=None):
        super(APIClient, self).__init__()
        self.url = url
        self.auth = auth
        self._client = None

    @property
    def client(self):
        """
        Delay client initialization till we're actually needing it
        """
        if self._client is None:
            self.authenticate()
        return self._client

    def authenticate(self):
        raise NotImplementedError("authenticate not implemented for %s" % type(self))

    def get_labels(self):
        raise NotImplementedError("get_labels not implemented for %s" % type(self))

    def submit_issue(self, category, title, description):
        raise NotImplementedError("submit_issue not implemented for %s" % type(self))

    def get_issue(self, issue):
        raise NotImplementedError("get_issue not implemented for %s" % type(self))


class GithubClient(APIClient):
    def __init__(self, url, auth=None):
        super(GithubClient, self).__init__(url, auth)

    def repo_info(self):
        # Get the user and repo from the url
        parts = urlparse.urlparse(self.url)
        path = parts.path

        path_components = path.split("/")
        user = path_components[2]
        repo = path_components[3]
        return user, repo

    def get_repo(self):
        user, repo = self.repo_info()
        return self.client.repository(user, repo)

    def authenticate(self):
        self._client = gh_login(token=self.auth)

    def get_labels(self):
        repository = self.get_repo()

        labels = []
        for label in repository.iter_labels():
            l = DictBacked(name=label.name, api=label, source=self)
            labels.append(l)
        return labels

    def submit_issue(self, category, title, description):
        user, repo = self.repo_info()
        r = self.client.repository(user, repo)
        i = r.create_issue(title, description, labels=[category.name])
        return DictBacked(url=i._api, api=i)

    def get_issue(self, issue):
        repo = self.get_repo()
        parts = urlparse.urlparse(issue.url)
        path = parts.path
        issue_number = path.split("/")[-1]
        i = repo.issue(issue_number)
        return DictBacked(
            name=i.title,
            web_url=i.html_url,
            api=i
        )


class JIRAClient(APIClient):
    def __init__(self, url, auth=None):
        super(JIRAClient, self).__init__(url, auth)

    def authenticate(self):
        server = urlparse.urlparse(self.url)
        server = server.scheme + "://" + server.netloc
        self._client = JIRA(server=server, basic_auth=self.auth)

    def get_project(self):
        parts = urlparse.urlparse(self.url)
        project_id = parts.path.split("/")[-1]
        return project_id

    def get_labels(self):
        # Grab the Components from the project
        components = self.client.project_components(self.get_project())
        labels = []
        for label in components:
            labels.append(DictBacked(api=label, source=self, name=label.name))
        return labels

    def submit_issue(self, category, title, description):
        fields = {
            "summary": title,
            "description": description,
            "project": {
                "id": self.get_project()
            },
            "issuetype": {
                "id": 3  # Extract this to a setting... or maybe a field on the source?
            },
            "duedate": "2015-05-31"  # Extract this to a setting
        }
        if category.source.base_url == self.url:
            # This category is associated with this endpoint
            # It's a component
            fields["components"] = [{"name": category.name}]
        else:
            fields["labels"] = [category.name]
        i = self.client.create_issue(fields=fields)
        return DictBacked(url=i.self, api=i)

    def get_issue(self, issue):
        issue_id = urlparse.urlparse(issue.url).path.split("/")[-1]
        i = self.client.issue(issue_id)
        return DictBacked(name=i.fields.summary, web_url=i.permalink(), api=i)
