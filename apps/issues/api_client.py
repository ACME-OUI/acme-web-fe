from django.conf import settings
from datetime import date
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


def github_to_generic(json):
    api_url = json["url"]
    web_url = json["html_url"]
    title = json["title"]
    author = json["user"]["login"]
    labels = [l["name"] for l in json["labels"]]
    text = json["body"]
    return DictBacked(url=api_url, web=web_url, title=title, author=author, labels=labels, text=text, type="github", backing=json)


def jira_to_generic(obj):
    api_url = obj.self
    web_url = obj.permalink()
    title = obj.fields.summary
    author = obj.fields.creator.emailAddress
    labels = obj.fields.labels
    text = obj.fields.description
    return DictBacked(url=api_url, web=web_url, title=title, author=author, labels=labels, text=text, type="jira", backing=obj)


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

    def update(self, model, issue):
        raise NotImplementedError("update not implemented for %s" % type(self))

    def authenticate(self):
        raise NotImplementedError("authenticate not implemented for %s" % type(self))

    def get_labels(self):
        raise NotImplementedError("get_labels not implemented for %s" % type(self))

    def submit_issue(self, category, title, description):
        raise NotImplementedError("submit_issue not implemented for %s" % type(self))

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

    def close(self, issue, days, hours, minutes):
        self.get_issue(issue).api.close()

    def open(self, issue):
        self.get_issue(issue).api.reopen()

    def get_representation(self, json):
        if type(json) == DictBacked:
            return json
        return github_to_generic(json)

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
        self.project = None
        self.component = None

    def authenticate(self):
        server = urlparse.urlparse(self.url)
        server = server.scheme + "://" + server.netloc
        self._client = JIRA(server=server, basic_auth=self.auth)
        c = self._client.component(self.url.split("/")[-1])
        self.component = c.name
        self.project = c.projectId

    def create_issue(self, issue):
        self.authenticate()
        duedate = date.today() + settings.JIRA_DUEDATE_OFFSET  # Extract this to a setting
        fields = {
            "summary": issue.title,
            "description": issue.text,
            "project": {
                "id": self.project
            },
            "components": [
                {"name": self.component}
            ],
            "issuetype": {
                "id": settings.JIRA_ISSUE_TYPE
            },
            "duedate": duedate.isoformat(),
            "labels": [l.replace(" ", "-") for l in issue.labels],
        }

        i = self.client.create_issue(fields=fields)

        return jira_to_generic(i)

    def get_labels(self):
        # Grab all labels from issues with the project/component
        issues = self.client.search_issues("project='%s' and component='%s'" % (self.project, self.component))

        labels = []
        l_names = set()
        for issue in issues:
            for label in issue.fields.labels:
                if label not in l_names:
                    labels.append(DictBacked(api={}, source=self, name=label))
                    l_names.add(label)
        return labels

    def close_issue(self, issue, days, hours, minutes):
        # JIRA wants seconds for timespent
        time_spent = 60 * (60 * (24 * days + hours) + minutes)

        issue = self.get_issue(issue).api

        self.client.add_worklog(issue=issue, timeSpentSeconds=time_spent)
        self.client.transition_issue(issue, settings.JIRA_RESOLVED_STATE)

    def open_issue(self, issue):
        issue = self.get_issue(issue).api
        self.client.transition_issue(issue, settings.JIRA_REOPENED_STATE)

    def submit_issue(self, category, title, description):
        duedate = date.today() + settings.JIRA_DUEDATE_OFFSET  # Extract this to a setting

        fields = {
            "summary": title,
            "description": description,
            "project": {
                "id": self.project
            },
            "components": [
                {"name": self.component}
            ],
            "issuetype": {
                "id": settings.JIRA_ISSUE_TYPE
            },
            "duedate": duedate.isoformat()
        }

        fields["labels"] = [category.name]
        i = self.client.create_issue(fields=fields)
        return DictBacked(url=i.self, api=i)

    def update(self, model, issue):
        i = self.get_issue(model)
        i = i.api
        i.api.update(summary=issue.title, description=issue.text, labels=issue.labels)

    def get_issue(self, issue):
        issue_id = urlparse.urlparse(issue.url).path.split("/")[-1]
        i = self.client.issue(issue_id)
        return DictBacked(name=i.fields.summary, web_url=i.permalink(), api=i)
