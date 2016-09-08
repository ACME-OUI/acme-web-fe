from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from models import ESGFNode
from models import PublishConfig
from models import FavoritePlot

from pyesgf.logon import LogonManager
from pyesgf.search import SearchConnection

from constants import ESGF_SEARCH_SUFFIX
from constants import ESGF_CREDENTIALS
from constants import NODE_HOSTNAMES
from run_manager.constants import USER_DATA_PREFIX
from run_manager.constants import RUN_SCRIPT_PATH
from poller.views import update as poller_update

from util.utilities import get_client_ip
from util.utilities import print_debug
from util.utilities import print_message
from util.utilities import get_directory_structure
from util.utilities import check_params
from util.esgf_publication_client import IngestionClient

import json
import requests
import os.path
import shutil
import subprocess
import os


# An empty dict subclass, to allow me to call poller views directly
# without needing to make an http request
class mydict(dict):
    pass


# Logs the user into ESGF with their given openID and password
# Inputs: username, password
# returns: status 200 if successful, 403 otherwise
def logon(request):
    credential = {
        'username': request.GET.get('username'),
        'password': request.GET.get('password')
    }
    if not credential['username']:
        print "[-] No username in logon request"
        return HttpResponse(status=403)
    elif not credential['password']:
        print "[-] No password in logon request"
        return HttpResponse(status=403)

    lm = LogonManager()
    bootstrap = False
    if not os.path.exists(ESGF_CREDENTIALS):
        bootstrap = True
    try:
        lm.logon_with_openid(credential['username'], credential['password'], bootstrap=bootstrap)
    except Exception as e:
        print_debug(e)
        return HttpResponse(status=403)
    if lm.is_logged_on():
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


@login_required
def upload_to_viewer(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    user = str(request.user)
    expected_params = [
        'run_name',
        'username',
        'password',
        'server',
    ]
    params = check_params(json.loads(request.body), expected_params)
    for p in expected_params:
        if not params[p]:
            return HttpResponse(status=400)

    run_directory = USER_DATA_PREFIX \
        + user + '/diagnostic_output/' \
        + params['run_name'] + '/diagnostic_output/amwg/'

    request = mydict()
    request.body = json.dumps({
        'user': user,
        'request': 'new',
        'run_type': 'upload_to_viewer',
        'request_attr': {
            'run_name': params['run_name'],
            'username': params['username'],
            'password': params['password'],
            'server': params['server'],
            'path': run_directory
        }
    })
    request.method = 'POST'
    try:
        r = poller_update(request)
        if(r.status_code != 200):
            print_message('Error communicating with poller')
            return HttpResponse(status=500)
        return HttpResponse(r.content)
    except Exception as e:
        print_message('Error making request to poller')
        print_debug(e)
        return HttpResponse(status=500)
    return HttpResponse(status=400)


#
# Gets a specified publish config by name
# input: config_name, the name of the config
@login_required
def get_publish_config(request):
    user = str(request.user)
    config = request.GET.get('config_name')
    if not config:
        print_message('No config name given')
        return HttpResponse(status=403)
    res = PublishConfig.objects.get(config_name=config)
    data = {}
    for field in PublishConfig._meta.get_fields():
        item = str(field).split('.')[-1]
        print_message(item)
        data[item] = getattr(res, item)
    return HttpResponse(json.dumps(data))


@login_required
def get_publish_config_list(request):
    user = str(request.user)
    res = PublishConfig.objects.all().filter(user=user)
    if len(res) == 0:
        print_message('{} has no stored publication configs'.format(user))
        return HttpResponse()
    data = {}
    for r in res:
        data[ getattr(r, 'config_name') ] = getattr(r, 'facets')
    return HttpResponse(json.dumps(data))


@login_required
def get_favorite_plots(request):
    user = str(request.user)
    res = FavoritePlot.objects.all().filter(user=user)
    plots = []
    for r in res:
        plots.append(getattr(r, 'plot'))
    return HttpResponse(json.dumps(plots))


@login_required
def set_favorite_plot(request):
    user = str(request.user)
    data = json.loads(request.body)
    plot = data.get('plot')
    if not plot:
        print_message('no plot given')
        return HttpResponse(status=400)

    new_fav = FavoritePlot(user=user, plot=plot)
    try:
        new_fav.save()
    except Exception as e:
        print_debug(e)
        return HttpResponse(status=500)
    return HttpResponse()


#
# Saves a publication config
#
# input: config_name, the name of the dataset
#        organization, the publishing org
#        firstname, the authors first name
#        lastname, the authors last name
#        description, a short description of the dataset
#        datanode, the node to publish to
#        facets: a JSON object holding a list of facets
@login_required
def save_publish_config(request):
    user = str(request.user)
    data = json.loads(request.body)
    metadata = data.get('metadata')
    if not metadata:
        print_message('no metadata given')
        return HttpResponse(status=400)
    params = {
        'config_name': data.get('config_name'),
        'organization': metadata.get('organization'),
        'firstname': metadata.get('firstname'),
        'lastname': metadata.get('lastname'),
        'description': metadata.get('description'),
        'datanode': metadata.get('datanode'),
        'facets': json.dumps(data.get('facets'))
    }
    for item in params:
        if not params[item]:
            print_message('No {} given'.format(item))
            return HttpResponse(status=400)
    config = PublishConfig(
        user=user,
        config_name=params['config_name'],
        organization=params['organization'],
        firstname=params['firstname'],
        lastname=params['lastname'],
        description=params['description'],
        datanode=params['datanode'],
        facets=params['facets'])
    try:
        config.save()
    except Exception as e:
        print_debug(e)
        print_message('error saveing new config')
        return HttpResponse(status=500)
    return HttpResponse()


#
# publish a local dataset to ESGF
# input: config_name, the name of the dataset (optional)
#        data_name, the name of the dataset (if no config_name)
#        organization, the publishing org (if no config_name)
#        firstname, the authors first name (if no config_name)
#        lastname, the authors last name (if no config_name)
#        description, a short description of the dataset (if no config_name)
#        datanode, the node to publish to (if no config_name)
#        facets: an object holding a list of facets (if no config_name)
#        server: the esgf server to publish to
#        esgf_user: the username to publish with
#        esgf_password: the password for the user
@login_required
def publish(request):
    expected_params = [
        'metadata',
        'config_name',
        'server',
        'esgf_user',
        'esgf_password',
        'path',
        'facets',
    ]
    params = check_params(json.loads(request.body), expected_params)
    # print_message(params)
    config_name = params.get('config_name')
    data_name = params.get('metadata').get('name')
    server = params.get('server')
    esgf_user = params.get('esgf_user')
    esgf_password = params.get('esgf_password')
    path = params.get('path')
    facets = params.get('facets')

    client_config = {
        'server': server,
        'openid': esgf_user,
        'password': esgf_password
    }
    submission_config = {
        'scan': {
            'options': '',
            'path': path,
        },
        'publish': {
            'options': {
                'files': 'all'
            },
            'files': [],
        },
    }
    if config_name:
        res = PublishConfig.objects.get(config_name=config_name)
        if not res:
            print_message('No PublishConfig matching {}'.format(config_name))
            return HttpResponse(status=400)
        submission_config['metadata'] = []
        submission_config['facets'] = []
        for field in PublishConfig._meta.get_fields():
            item = str(field).split('.')[-1]
            if item != 'facets':
                if item == 'id' or item == 'config_name':
                    continue
                submission_config['metadata'].append({
                    'name': item,
                    'value': getattr(res, item)
                })
            else:
                facets = json.loads(getattr(res, item))
                for k in facets:
                    submission_config['facets'].append({
                        'name': k,
                        'value': facets[k]
                    })
    else:
        submission_config = {
            'metadata': [
                {
                    'name': 'name',
                    'value': data_name
                },{
                    'name': 'organization',
                    'value': params.get('organization')
                },{
                    'name': 'firstname',
                    'value': params.get('firstname')
                },{
                    'name': 'lastname',
                    'value': params.get('lastname')
                }, {
                    'name': 'description',
                    'value': params.get('description')
                }, {
                    'name': 'datanode',
                    'value': params.get('data_node')
                }
            ],
            'facets': [],
            'scan': {
                'options': '',
                'path': path,
            },
            'publish': {
                'options': {
                    'files': 'all'
                },
                'files': [],
            },
        }
        for k in facets:
            submission_config['facets'].append({
                'name': k,
                'value': facets[k]
            })
    print_message(client_config)
    print_message(submission_config)
    client = IngestionClient(client_config)
    if client is None:
        print_message('Unable to create connection with ESGF ingestion service')
        return HttpResponse(500)
    response, content = client.submit(submission_config)
    return HttpResponse(status=400)


# Queries a set of nodes for their facets
# Inputs: { 'nodes': ['list', 'of', 'hostnames'] }
# returns: facet information from the requested nodes
def load_facets(request):
    print request.GET.get('nodes')
    nodes = json.loads(request.GET.get('nodes'))
    print nodes
    # if 'nodes' not in nodes:
    #     return HttpResponse(status=400)
    facets = {}
    for node in nodes:
        try:
            print "[+] Connecting to " + 'http://' + node + ESGF_SEARCH_SUFFIX
            conn = SearchConnection(
                'http://' + node + ESGF_SEARCH_SUFFIX, distrib=True)
            context = conn.new_context()
            for facet in context.get_facet_options():
                facets[facet] = context.facet_counts[facet]
        except Exception as e:
            # print_debug(e)
            return HttpResponse(status=500)
    return HttpResponse(json.dumps(facets))


# Searches a set of nodes for all datasets that match given criteria
# Inputs: { 'nodes': ['list', 'of', 'hostnames'], 'terms': ['list', 'of', 'terms'] }
# Returns: list of datasets matching given terms from given nodes
def node_search(request):

    searchString = json.loads(request.GET.get('searchString'))
    nodes = json.loads(request.GET.get('nodes'))
    print searchString
    print nodes

    if not nodes:
        print "Invalid node selection"
        return HttpResponse(status=400)
    else:
        print nodes

    if not searchString:
        print "Invalid search terms"
        return HttpResponse(status=400)
    else:
        print searchString

    response = {}
    for node in nodes:
        print node
        try:
            print '[+] searching ' + node + ' for ' + str(searchString)
            conn = SearchConnection(
                'http://' + node + ESGF_SEARCH_SUFFIX, distrib=True)
            context = conn.new_context(**searchString)
            rs = context.search()
            print '[+] got reply from search node'
            response['hits'] = context.hit_count
            for i in range(len(rs)):
                response[str(i)] = rs[i].json

        except Exception as e:
            print_debug(e)
            return HttpResponse(status=400)

    return HttpResponse(json.dumps(response))


# TODO: Once the node manager is running, this should call their API to get the current lise of nodes
def node_list(request):
    response = json.dumps(NODE_HOSTNAMES)
    return HttpResponse(response)


#
# reads the contents of the users data directory, returning a list
# of their obs, model, and diagnostic data
#
@login_required
def get_user_data(request):
    user = str(request.user)
    path = os.path.abspath(os.path.dirname(__file__)) + '/../../userdata/' + user
    userdata = get_directory_structure(path)
    return HttpResponse(json.dumps(userdata))


@login_required
def file_upload(request):
    if request.method == 'POST':
        print_message('files: {}'.format(request.FILES))
        folder = request.FILES.keys()[0]
        print_message(request.FILES.get(folder))
        print_message('folder: {}'.format(folder))
        print_message('folder contents: {}'.format(request.FILES.getlist(folder)))
        type = request.POST.get('type')
        user = str(request.user)
        path = USER_DATA_PREFIX + user
        if type == 'observation':
            path += '/observations/'
        elif type == 'model':
            path += '/model_output/'
        else:
            print_message('unrecognised type {}'.format(type))
            return HttpResponse(status=400)
        path += folder
        if os.path.exists(path):
            print_message('Folder {} already exists'.format(path))
            return HttpResponse(status=400)
        os.makedirs(path)
        for item in request.FILES.getlist(folder):
            print item
            print 'writing to {}/{}'.format(path, item)
            with open('{}/{}'.format(path,item), 'wb') as target:
                for chunk in item.chunks():
                    target.write(chunk)
                target.close()
    return HttpResponse()


# Im not sure if we're still going to need this. Will update once I have a better idea
#
# @login_required
# def node_info(request):
#     try:
#         response = {}
#         nodes = ESGFNode.objects.all()
#         for node in nodes:
#             response[node.short_name] = node.node_data
#             if 'children' not in response[node.short_name]:
#                 continue
#
#             if 'Node' in response[node.short_name]['children']:
#                 response[node.short_name]['children']['Node'][
#                     'attributes']['status'] = str(node.available)
#                 response[node.short_name]['children']['Node'][
#                     'attributes']['last_seen'] = str(node.last_seen)
#             else:
#                 response[node.short_name]['children']['Node'] = {}
#                 response[node.short_name]['children'][
#                     'Node']['attributes'] = {}
#                 response[node.short_name]['children']['Node'][
#                     'attributes']['status'] = str(node.available)
#                 response[node.short_name]['children']['Node'][
#                     'attributes']['last_seen'] = str(node.last_seen)
#                 response[node.short_name]['children']['Node'][
#                     'attributes']['hostname'] = node.short_name
#         return HttpResponse(json.dumps(response))
#     except Exception as e:
#         # print_debug(e)
#         return HttpResponse(status=500)
