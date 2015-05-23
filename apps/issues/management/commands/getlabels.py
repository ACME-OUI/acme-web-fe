from django.core.management.base import BaseCommand
from issues.models import IssueSource, IssueCategory


class Command(BaseCommand):
    help = "Sync IssueCategories for all IssueSources"

    def handle(self, *args, **options):
        sources = IssueSource.objects.all()
        for source in sources:
            existing_categories = source.issuecategory_set.all()
            cat_names = [c.name for c in existing_categories]
            labels = []
            for label in source.get_labels():
                labels.append(label.name)
                if label.name in cat_names:
                    continue
                c = IssueCategory(name=label.name, source=source)
                c.save()

            for c in cat_names:
                if c not in labels:
                    s = "%s does not have label %s anymore."
                    print s % (source.name, c.name)
                    print "You should clean this up manually."
