from django.db import models
from github3 import login as gh_login
from django.core.exceptions import ValidationError
from django.conf import settings
import urlparse


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


class IssueSource(models.Model):
	"""
	Used to retrieve/post issues from/to external services

	Stores a URL that can be polled for all issues from this source.
	"""
	# Name of the source
	name = models.CharField(max_length=512, unique=True, blank=False)
	# The base URL of the service
	base_url = models.URLField()
	# Currently just github or jira; derive issues/creation urls from this and base
	source_type = models.CharField(max_length=512, unique=False, blank=False)
	# Text asking for specific information from a user
	required_info = models.TextField(unique=False)
	# If an issue is made in this source, also make it in the linked source
	linked = models.ForeignKey("IssueSource", blank=True, null=True, validators=[validate_acyclic_linked_source])

	def submit_github_issue(self, category, title, description):
		gh = gh_login(token=settings.GITHUB_KEY)
		# Parse the base_url to get the user & repo info
		parts = urlparse.urlparse(self.base_url)
		path = parts.path

		_, _, user, repo = path.split("/")
		r = gh.repository(user, repo)
		i = r.create_issue(title, description, labels=[category.name])
		local_tracker = Issue(url=i._api, source=self)
		local_tracker.save()
		local_tracker.categories.add(category)

		return local_tracker

	def submit_issue(self, category, title, description):
		if self.source_type == "github":
			issue = self.submit_github_issue(category, title, description)
		elif self.source_type == "jira":
			raise NotImplementedError("JIRA integration not yet implemented")

		if self.linked is not None:
			linked_issue = self.linked.submit_issue(category, title, description)
			issue.matched_issue = linked_issue
		
		issue.save()
		return issue

	def get_issue(self, issue):
		if self.source_type == "github":
			import requests
			response = requests.get(issue.url, headers={"Authorization": "token %s" % settings.GITHUB_KEY})
			obj = response.json()
			return obj
		else:
			raise NotImplementedError("Only GitHub works right now.")

	def clean(self):
		"""
		A safeguard against cycles
		"""
		l = self.linked
		previous = self
		while l is not None:
			if l.id == self.id:
				raise ValidationError("Linking from %s to %s would create a cycle; %s pointed to by %s" % (self.name, self.linked.name, self.name, previous.name))
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

	@property
	def name(self):
		# Use the appropriate API to grab the name for this issue
		api_self = self.source.get_issue(self)
		return api_self["title"]


	def get_all_matched(self):
		if self.matched_issue is not None:
			return Issue.objects.filter(matched_issue=self.matched_issue)
		else:
			return Issue.objects.filter(matched_issue=self)

	def __str__(self):
		return self.url

class Subscriber(models.Model):
	"""
	Users interested in issues; requires email confirmation of account
	"""
	email = models.EmailField(max_length=254, unique=True)
	# Send an email with a link to confirm address
	confirmed = models.BooleanField(default=False)
	# Used for temporary authentication; allows additional subscriptions without reauthing via email
	token = models.CharField(max_length=64, unique=True, blank=True, null=True)
	# Used to timeout tokens
	signed_in = models.DateTimeField(auto_now=True)
	# Every issue that this subscriber is associated with
	subscriptions = models.ManyToManyField(Issue)

	def subscribe(self, issue):
		if self.confirmed is False and self.token is None:
			self.confirm_email()
			self.subscriptions.add(issue)
		elif self.confirmed:
			self.confirm_subscription(issue)

	def confirm_email(self):
		from uuid import uuid4
		self.token = uuid4().hex
		from django.core.mail import send_mail
		send_mail("Welcome to ACME Issues!", "Please confirm your email address at <http://localhost:8000/issues/confirm?token=%s>" % self.token, "fries2@llnl.gov", [self.email])
		self.save()

	def subscriptions_token(self, issue):
		from hashlib import sha256
		digest = sha256()
		digest.update(self.email)
		for sub in self.subscriptions.all():
			digest.update(sub.url)
		digest.update(issue.url)
		digest.update(settings.SECRET_KEY)
		return digest.hexdigest()

	def confirm(self):
		self.token = None
		self.confirmed = True
		self.save()

	def confirm_subscription(self, issue):
		from django.core.mail import send_mail
		self.token = self.subscriptions_token(issue)
		send_mail("ACME Issues: Confirm issue subscription", "Please click here to confirm your subscription to the issue '%s': <http://localhost:8000/issues/confirm/subscription?token=%s&issue=%d>" % (issue.name, self.token, issue.id), "fries2@llnl.gov", [self.email])
		self.save()

	def __str__(self):
		return self.email


