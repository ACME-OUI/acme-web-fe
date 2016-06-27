from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from util.utilities import get_client_ip, print_debug
from django.contrib.auth.decorators import login_required
from models import ESGFNode
from pyesgf.logon import LogonManager
from util.utilities import print_debug
import json



def download(request):
    return HttpResponse(status=200)

def logon(request):
    print '[+] Got a logon request'
    credential = json.loads(request.body)
    if 'username' not in credential or 'password' not in credential:
        return HttpResponse(status=403)
    lm = LogonManager()
    try:
        lm.logon_with_openid(credential['username'], credential['password'], bootstrap=True)
    except Exception as e:
        print_debug(e)
    if lm.is_logged_on():
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)

@login_required
def node_info(request):
    if request.method == 'GET':
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
    else:
        print "Unexpected %s request from %s" % request.method, get_client_ip(request)
        return HttpResponse(status=500)


@login_required
def load_facets(request):
    if request.method == 'POST':
        nodes = json.loads(request.body)
        facets = {}
        for node in nodes:
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
    else:
        print "Unexpected %s request from %s" % request.method, get_client_ip(request)
        return HttpResponse(status=500)


@login_required
def node_search(request):
    if request.method == 'POST':
        searchString = json.loads(request.body)
        print searchString
        if 'nodes' in searchString:
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
    else:
        print "Unexpected %s request from %s" % request.method, get_client_ip(request)
        return HttpResponse(status=500)
