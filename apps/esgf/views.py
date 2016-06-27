from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from util.utilities import get_client_ip, print_debug
from django.contrib.auth.decorators import login_required
from models import ESGFNode
from pyesgf.logon import LogonManager
from pyesgf.search import SearchConnection
from util.utilities import print_debug
import json
import os.path



def download(request):
    return HttpResponse(status=200)

# Logs the user into ESGF with their given openID and password
# Inputs: username, password
# returns: status 200 if successful, 403 otherwise
def logon(request):
    credential = json.loads(request.body)
    if 'username' not in credential or 'password' not in credential:
        return HttpResponse(status=403)
    lm = LogonManager()
    try:
        bootstrap = False
        if not os.path.exists('~/.esf/certificats/'):
            bootstrap = True
        lm.logon_with_openid(credential['username'], credential['password'], bootstrap=bootstrap)
    except Exception as e:
        print_debug(e)
    if lm.is_logged_on():
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)

# Queries a set of nodes for their facets
# Inputs: { 'nodes': ['list', 'of', 'hostnames'] }
# returns: facet information from the requested nodes
def load_facets(request):
    nodes = json.loads(request.body)
    if 'nodes' not in nodes:
        return HttpResponse(status=400)
    facets = {}
    for node in nodes['nodes']:
        try:
            conn = SearchConnection(
                'http://' + node + '/esg-search/', distrib=True)
            context = conn.new_context()
            for facet in context.get_facet_options():
                facets[facet] = context.facet_counts[facet]
        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    return HttpResponse(json.dumps(facets))

# Searches a set of nodes for all datasets that match given criteria
# Inputs: { 'nodes': ['list', 'of', 'hostnames'], 'terms': ['list', 'of', 'terms'] }
# Returns: list of datasets matching given terms from given nodes
def node_search(request):

    searchString = json.loads(request.body)
    if 'nodes' not in searchString:
        return HttpResponse(403)

    response = {}
    for node in searchString['nodes']:
        try:
            conn = SearchConnection(
                'http://' + node + '/esg-search/', distrib=True)
            print searchString['terms']
            context = conn.new_context(**searchString['terms'])
            rs = context.search()
            response['hits'] = context.hit_count
            for i in range(len(rs)):
                response[str(i)] = rs[i].json

        except Exception as e:
            print_debug(e)

        return HttpResponse(json.dumps(response))
    else:
        print "Improperly formatted request, no nodes specified"
        return HttpResponse(status=500)



@login_required
def node_info(request):
    try:
        response = {}
        nodes = ESGFNode.objects.all()
        for node in nodes:
            response[node.short_name] = node.node_data
            if 'children' not in response[node.short_name]:
                continue

            if 'Node' in response[node.short_name]['children']:
                response[node.short_name]['children']['Node'][
                    'attributes']['status'] = str(node.available)
                response[node.short_name]['children']['Node'][
                    'attributes']['last_seen'] = str(node.last_seen)
            else:
                response[node.short_name]['children']['Node'] = {}
                response[node.short_name]['children'][
                    'Node']['attributes'] = {}
                response[node.short_name]['children']['Node'][
                    'attributes']['status'] = str(node.available)
                response[node.short_name]['children']['Node'][
                    'attributes']['last_seen'] = str(node.last_seen)
                response[node.short_name]['children']['Node'][
                    'attributes']['hostname'] = node.short_name
        return HttpResponse(json.dumps(response))
    except Exception as e:
        print_debug(e)
        return HttpResponse(status=500)
