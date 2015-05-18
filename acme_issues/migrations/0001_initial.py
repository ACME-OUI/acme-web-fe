# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IssueSource'
        db.create_table(u'acme_issues_issuesource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
            ('base_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('source_type', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('required_info', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'acme_issues', ['IssueSource'])

        # Adding model 'IssueCategory'
        db.create_table(u'acme_issues_issuecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['acme_issues.IssueSource'])),
        ))
        db.send_create_signal(u'acme_issues', ['IssueCategory'])

        # Adding model 'CategoryQuestion'
        db.create_table(u'acme_issues_categoryquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('yes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('no', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('yes_type', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('no_type', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
        ))
        db.send_create_signal(u'acme_issues', ['CategoryQuestion'])

        # Adding model 'Issue'
        db.create_table(u'acme_issues_issue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('matched_issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['acme_issues.Issue'], null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['acme_issues.IssueSource'])),
        ))
        db.send_create_signal(u'acme_issues', ['Issue'])

        # Adding M2M table for field categories on 'Issue'
        m2m_table_name = db.shorten_name(u'acme_issues_issue_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('issue', models.ForeignKey(orm[u'acme_issues.issue'], null=False)),
            ('issuecategory', models.ForeignKey(orm[u'acme_issues.issuecategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['issue_id', 'issuecategory_id'])

        # Adding model 'Subscriber'
        db.create_table(u'acme_issues_subscriber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=254)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32, blank=True)),
            ('signed_in', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('digest', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'acme_issues', ['Subscriber'])

        # Adding M2M table for field subscriptions on 'Subscriber'
        m2m_table_name = db.shorten_name(u'acme_issues_subscriber_subscriptions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subscriber', models.ForeignKey(orm[u'acme_issues.subscriber'], null=False)),
            ('issue', models.ForeignKey(orm[u'acme_issues.issue'], null=False))
        ))
        db.create_unique(m2m_table_name, ['subscriber_id', 'issue_id'])


    def backwards(self, orm):
        # Deleting model 'IssueSource'
        db.delete_table(u'acme_issues_issuesource')

        # Deleting model 'IssueCategory'
        db.delete_table(u'acme_issues_issuecategory')

        # Deleting model 'CategoryQuestion'
        db.delete_table(u'acme_issues_categoryquestion')

        # Deleting model 'Issue'
        db.delete_table(u'acme_issues_issue')

        # Removing M2M table for field categories on 'Issue'
        db.delete_table(db.shorten_name(u'acme_issues_issue_categories'))

        # Deleting model 'Subscriber'
        db.delete_table(u'acme_issues_subscriber')

        # Removing M2M table for field subscriptions on 'Subscriber'
        db.delete_table(db.shorten_name(u'acme_issues_subscriber_subscriptions'))


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