from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User
import xml.etree.ElementTree as ET
import requests
from StringIO import StringIO
import datetime


class TileLayout(models.Model):
    user_name = models.CharField(max_length=100)
    layout_name = models.CharField(max_length=100, default='layout1')
    board_layout = models.CharField(max_length=2000)
    mode = models.CharField(max_length=10, default='day')
    default = models.BooleanField(default=0)


class Credential(models.Model):
    site_user_name = models.CharField(max_length=100, default='default_user')
    service_user_name = models.CharField(
        max_length=100, default='default_user')
    password = models.CharField(max_length=100)
    service = models.CharField(max_length=100)


class ESGFNode(models.Model):
    short_name = models.CharField(max_length=100, default='default_node')
    last_seen = models.DateTimeField(default=datetime.datetime.now())
    available = models.BooleanField(default=False)
    host = models.CharField(max_length=100, default='unknown host')
    node_data = JSONField()

    def refresh(self):
        r = requests.get(
            'http://' + self.host + '/esgf-node-manager/registration.xml', timeout=1)
        if r.status_code == 404:
            self.available = False
            self.save()
            return
        self.available = True
        self.last_seen = datetime.datetime.now()
        tree = ET.parse(StringIO(r.content))
        self.node_data = self.xml_to_json(tree.getroot())
        self.short_name = self.node_data['children']['{http://www.esgf.org/registry}Node']['attributes']['shortName']
        self.save()

    def xml_to_json(self, node):
        node_data = {
            "children": {},
            "attributes": {key: value for key, value in node.items()}
        }

        for item in node:
            node_data["children"][item.tag] = self.xml_to_json(item)
        return node_data
