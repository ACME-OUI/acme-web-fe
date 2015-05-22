from django.db import models
from api_client import GithubClient, JIRAClient
from django.core.exceptions import ValidationError
from django.conf import settings


def validate_acyclic_linked_source(value):
    """
    Validates that the linked field on IssueSource is acyclic
    Cycles are bad. Very bad. Infinite loop bad.
    """
    try:
        source = IssueSource.objects.get(id=value)
        visited = set()
        while source.linked is not None:
            if source.id in visited:
                break
            visited.add(source.id)
            source = source.linked
        else:
            return
        raise ValidationError("Cycle detected at %d" % source.id)
    except IssueSource.DoesNotExist:
        raise ValidationError("Linked source doesn't exist")


def validate_source_type(value):
    if value in ("jira", "github"):
        return
    else:
        raise ValidationError("Source Type %s not implemented." % value)


class IssueSource(models.Model):

    """
    Used to retrieve/post issues from/to external services

    Stores a URL that can be polled for all issues from this source.
    """
    # Name of the source
    name = models.CharField(max_length=512, unique=True, blank=False)
    # The base URL of the service
    base_url = models.URLField()
    # Currently just github or jira; derive issues/creation urls from this and
    # base
    source_type = models.CharField(max_length=512, unique=False, blank=False, validators=[validate_source_type])
    # Text asking for specific information from a user
    required_info = models.TextField(unique=False)
    # If an issue is made in this source, also make it in the linked source
    linked = models.ForeignKey("IssueSource", blank=True, null=True,
                               validators=[validate_acyclic_linked_source])

    def __init__(self, *args, **kwargs):
        super(IssueSource, self).__init__(*args, **kwargs)
        self._client = None

    def is_github(self):
        return self.source_type == "github"

    def is_jira(self):
        return self.source_type == "jira"

    @property
    def client(self):
        if self._client is None:
            if self.is_github():
                self._client = GithubClient(self.base_url, settings.GITHUB_KEY)
            elif self.is_jira():
                self._client = JIRAClient(self.base_url, (settings.JIRA_USER, settings.JIRA_PASSWORD))
        return self._client

    def get_labels(self):
        return self.client.get_labels()

    def submit_issue(self, category, title, description, parent_issue=None):
        issue = self.client.submit_issue(category, title, description)
        local_tracker = Issue(url=issue.url, source=self)
        if parent_issue is None:
            parent_issue = local_tracker
        else:
            local_tracker.matched_issue = parent_issue
        local_tracker.save()
        local_tracker.categories.add(category)

        if self.linked is not None:
            self.linked.submit_issue(category, title, description, parent_issue=parent_issue)

        return local_tracker

    def get_issue(self, issue):
        return self.client.get_issue(issue)

    def clean(self):
        """
        A safeguard against cycles
        """
        l = self.linked
        previous = self
        while l is not None:
            if l.id == self.id:
                raise ValidationError("Linking from %s to %s would create a cycle; %s pointed to by %s" %
                                      (self.name, self.linked.name, self.name, previous.name))
            previous = l
            l = l.linked

    def __str__(self):
        return self.base_url


class IssueCategory(models.Model):

    """
    Labels for issues
    """
    name = models.CharField(max_length=512, unique=False, blank=False)
    source = models.ForeignKey(IssueSource)

    def has_question(self):
        """
        Builds complex query to check if any category questions point
        to this object
        """
        yes_query = models.Q(yes_type="category", yes=self.id)
        no_query = models.Q(no_type="category", no=self.id)

        objects = CategoryQuestion.objects.filter(yes_query | no_query)
        return len(objects) > 0

    def __str__(self):
        return self.name + " (%s)" % self.source


class CategoryQuestion(models.Model):

    """
    Used to determine what category an issue goes into
    """

    question = models.CharField(max_length=512, unique=False, blank=False)

    # Points to either another CategoryQuestion or an IssueCategory
    yes = models.IntegerField(blank=True, null=True)
    no = models.IntegerField(blank=True, null=True)

    # Either "category" or "question"
    yes_type = models.CharField(max_length=12, blank=True, null=True)
    no_type = models.CharField(max_length=12, blank=True, null=True)

    source = models.ForeignKey(IssueSource, null=True, blank=True)

    def get_parents(self):
        yes = models.Q(yes_type="question", yes=self.id)
        no = models.Q(no_type="question", no=self.id)
        objects = CategoryQuestion.objects.filter(yes | no)
        return objects

    def points_to(self, source):
        y = self.get_yes()
        n = self.get_no()

        if self.yes_type == "category":
            if y.source.id == source.id:
                return True
        elif y is not None and y.points_to(source):
            return True

        if self.no_type == "category":
            if n.source.id == source.id:
                return True
        elif n is not None and n.points_to(source):
            return True

        return False

    def is_root(self):
        objects = self.get_parents()
        return len(objects) == 0

    def get_yes(self):
        if self.yes_type == "question":
            try:
                return CategoryQuestion.objects.get(id=self.yes)
            except CategoryQuestion.DoesNotExist:
                self.set_yes(None)
                self.save()
        elif self.yes_type == "category":
            try:
                return IssueCategory.objects.get(id=self.yes)
            except IssueCategory.DoesNotExist:
                self.set_yes(None)
                self.save()
        else:
            return None

    def get_no(self):
        if self.no_type == "question":
            try:
                return CategoryQuestion.objects.get(id=self.no)
            except CategoryQuestion.DoesNotExist:
                self.set_no(None)
                self.save()
        elif self.no_type == "category":
            try:
                return IssueCategory.objects.get(id=self.no)
            except IssueCategory.DoesNotExist:
                self.set_no(None)
                self.save()
        else:
            return None

    def set_yes(self, value):
        if type(value) == CategoryQuestion:
            self.yes_type = "question"
        elif type(value) == IssueCategory:
            self.yes_type = "category"
        else:
            self.yes_type = None
            self.yes = None
            return
        self.yes = value.id

    def set_no(self, value):
        if type(value) == CategoryQuestion:
            self.no_type = "question"
        elif type(value) == IssueCategory:
            self.no_type = "category"
        else:
            self.no_type = None
            self.yes = None
            return
        self.no = value.id

    def delete_chain(self):
        if self.yes is not None:
            if self.yes_type == "question":
                self.get_yes().delete_chain()
        if self.no is not None:
            if self.no_type == "question":
                self.get_no().delete_chain()

        parents = self.get_parents()
        for p in parents:
            if p.yes == self.id:
                p.set_yes(None)
            if p.no == self.id:
                p.set_no(None)
            p.save()

        self.delete()

    def __str__(self):
        return self.question


class Issue(models.Model):

    """
    Internal representation of an issue from an external source
    """
    # URL for the endpoint for this issue
    url = models.URLField()
    # JIRA -> GitHub and vice versa
    matched_issue = models.ForeignKey("Issue", blank=True, null=True)
    # The origin of this issue
    source = models.ForeignKey(IssueSource)
    # Tags for this issue
    categories = models.ManyToManyField(IssueCategory)

    subscribers = models.ManyToManyField(getattr(settings, "AUTH_USER_MODEL", "auth.User"))

    def __init__(self, *args, **kwargs):
        super(Issue, self).__init__(*args, **kwargs)
        self._api_cache = None

    @property
    def name(self):
        if self._api_cache is None:
            self._api_cache = self.source.get_issue(self)
        return self._api_cache.name

    @property
    def web_url(self):
        if self._api_cache is None:
            self._api_cache = self.source.get_issue(self)
        return self._api_cache.web_url

    def subscribe(self, user):
        self.subscribers.add(user)

    def notify(self, subject, message):
        from django.core.mail import send_mass_mail
        from smtplib import SMTPException

        subs = [user.email for user in self.subscribers.all() if user.email is not None]
        try:
            send_mass_mail((subject, message, settings.ISSUES_MAIL_ADDRESS, subs))
        except SMTPException as e:
            print "Issue Notification: Couldn't send mail because", e

    def get_all_matched(self):
        if self.matched_issue is not None:
            return Issue.objects.filter(matched_issue=self.matched_issue)
        else:
            return Issue.objects.filter(matched_issue=self)

    def __str__(self):
        return self.url
