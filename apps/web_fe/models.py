from django.db import models
from jsonfield import JSONField
import json
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

        if r.status_code != 200:
            self.available = False
            self.save()
            return
        self.available = True
        self.last_seen = datetime.datetime.now()
        node_xml = r.content
        tree = ET.parse(StringIO(node_xml))
        self.node_data = self.xml_to_json(tree.getroot())
        self.node_data = json.dumps(self.node_data).replace(
            '{http://www.esgf.org/registry}', '')
        self.node_data = json.loads(self.node_data)
        if 'Node' in self.node_data['children']:
            self.short_name = self.node_data['children'][
                'Node']['attributes']['shortName']
        self.save()

    def xml_to_json(self, node):
        node_data = {
            "children": {},
            "attributes": {key: value for key, value in node.items()}
        }

        for item in node:
            node_data["children"][item.tag] = self.xml_to_json(item)
        return node_data
