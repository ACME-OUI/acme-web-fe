from django.db import models
from django.utils import timezone
import xml.etree.ElementTree as ET
# from jsonfield import JSONField
import requests


# class ESGFNode(models.Model):
#     short_name = models.CharField(max_length=100, default='default_node')
#     last_seen = models.DateTimeField(default=timezone.now())
#     available = models.BooleanField(default=False)
#     host = models.CharField(max_length=100, default='unknown host')
#     node_data = JSONField()

#     def refresh(self):
#         status = False
#         try:
#             url = "http://%s/esgf-node-manager/registration.xml" % self.host
#             r = requests.get(url, timeout=1)
#             if r.status == 200:
#                 status = True
#         except Exception:
#             print "[-] Failed to connect to host %s" % self.host

#         if not status:
#             self.available = False
#             self.save()
#         else:
#             self.available = True
#             self.last_seen = timezone.now()
#             node_xml = r.content
#             tree = ET.parse(StringIO(node_xml))
#             self.node_data = self.xml_to_json(tree.getroot())
#             url = '{http://www.esgf.org/registry}'
#             self.node_data = json.dumps(self.node_data).replace(url, '')
#             self.node_data = json.loads(self.node_data)
#             if 'Node' in self.node_data['children']:
#                 self.short_name = self.node_data['children']['Node']['attributes']['shortName']
#             self.save()

#     def xml_to_json(self, node):
#         node_data = {
#             "children": {},
#             "attributes": {key: value for key, value in node.items()}
#         }
#         for item in node:
#             node_data["children"][item.tag] = self.xml_to_json(item)

#         return node_data


class PublishConfig(models.Model):
    config_name = models.CharField(max_length=100, unique=True, default='default_config_name')
    user = models.CharField(max_length=100, default='default_user')
    firstname = models.CharField(max_length=100, default='default_first_name')
    lastname = models.CharField(max_length=100, default='default_last_name')
    organization = models.CharField(max_length=100, default='default_org')
    description = models.CharField(max_length=100, default='default_description')
    datanode = models.CharField(max_length=100, default='default_datanode')
    facets = models.TextField(null=True)


class FavoritePlot(models.Model):
    user = models.CharField(max_length=100, default='default_user')
    plot = models.TextField()
