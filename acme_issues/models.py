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

class IssueCategory(models.Model):
	"""
	Labels for issues
	"""
	name = models.CharField(max_length=512, unique=False, blank=False)
	source = models.ForeignKey(IssueSource)

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

class Issue(models.Model):
	"""
	Internal representation of an issue from an external source
	"""
	url = models.URLField()
	source = models.ForeignKey(IssueSource)
	categories = models.ManyToManyField(IssueCategory)

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
	subscriptions = models.ManyToManyField(Issue)