from django.core.management.base import BaseCommand, CommandError
import github3 as gh
from acme_issues.models import IssueSource, IssueCategory
from django.conf import settings
import urlparse

class Command(BaseCommand):
	help = "Sync IssueCategories for all IssueSources"

	def handle(self, *args, **options):
		github = gh.login(token=settings.GITHUB_KEY)

		gh_sources = IssueSource.objects.filter(source_type__startswith="github")
		for source in gh_sources:
			url = source.base_url
			parts = urlparse.urlparse(url)
			path = parts.path

			path_components = path.split("/")
			user = path_components[2]
			repo = path_components[3]

			existing_categories = source.issuecategory_set.all()
			cat_names = [c.name for c in existing_categories]

			repo = github.repository(user, repo)
			labels = []
			for label in repo.iter_labels():
				labels.append(label)
				if label in cat_names:
					continue
				c = IssueCategory(name=label, source=source)
				c.save()
			for c in cat_names:
				if c.name not in labels:
					print source.name, "does not have label", c.name, "anymore. You should clean this up manually."