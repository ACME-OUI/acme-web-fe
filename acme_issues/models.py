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

	def __str__(self):
		return self.name + " (%s)" % self.source

class CategoryQuestion(models.Model):
	"""
	Used to determine what category an issue goes into
	"""
	question = models.CharField(max_length=512, unique=False, blank=False)
	# "text", "boolean"
	question_type = models.CharField(max_length=32, unique=False)
	# If next_question is blank, category should be filled
	category = models.ForeignKey(IssueCategory, blank=True, null=True)
	# If you need to narrow something down, you can use several questions
	next_question = models.ForeignKey("CategoryQuestion", blank=True, null=True)

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