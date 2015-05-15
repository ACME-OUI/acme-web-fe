from django.db import models

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
	token = models.CharField(max_length=32, unique=True, blank=True)
	# Used to timeout tokens
	signed_in = models.DateTimeField(auto_now=True)
	# Default to sending an email digest for a user, rather than individual notifications
	digest = models.BooleanField(default=True)
	# Every issue that this subscriber is associated with
	subscriptions = models.ManyToManyField(Issue)

	def __str__(self):
		return self.email


