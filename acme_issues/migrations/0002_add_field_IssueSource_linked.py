# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'IssueSource.linked'
        db.add_column(u'acme_issues_issuesource', 'linked',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['acme_issues.IssueSource'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'IssueSource.linked'
        db.delete_column(u'acme_issues_issuesource', 'linked_id')


    models = {
        u'acme_issues.categoryquestion': {
            'Meta': {'object_name': 'CategoryQuestion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'no_type': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'yes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'yes_type': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'})
        },
        u'acme_issues.issue': {
            'Meta': {'object_name': 'Issue'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['acme_issues.IssueCategory']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matched_issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['acme_issues.Issue']", 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['acme_issues.IssueSource']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'acme_issues.issuecategory': {
            'Meta': {'object_name': 'IssueCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['acme_issues.IssueSource']"})
        },
        u'acme_issues.issuesource': {
            'Meta': {'object_name': 'IssueSource'},
            'base_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linked': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['acme_issues.IssueSource']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'required_info': ('django.db.models.fields.TextField', [], {}),
            'source_type': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'acme_issues.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'digest': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'signed_in': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'subscriptions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['acme_issues.Issue']", 'symmetrical': 'False'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['acme_issues']