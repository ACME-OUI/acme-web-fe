from django.contrib import admin
from models import IssueSource, IssueCategory, CategoryQuestion, Issue, Subscriber

# Register your models here.
admin.site.register(IssueSource)
admin.site.register(IssueCategory)
admin.site.register(CategoryQuestion)
admin.site.register(Issue)
admin.site.register(Subscriber)