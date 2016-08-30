from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from util.utilities import get_client_ip, print_debug
from django.contrib.auth.decorators import login_required
from models import ESGFNode, PublishConfig
from pyesgf.logon import LogonManager
from pyesgf.search import SearchConnection
from constants import ESGF_SEARCH_SUFFIX, ESGF_CREDENTIALS, NODE_HOSTNAMES
from run_manager.constants import USER_DATA_PREFIX
import json
import requests
import os.path
import shutil
import subprocess
import os
from util.utilities import print_debug, print_message, get_directory_structure
from util.esgf_publication_client import IngestionClient

# From: https://github.com/apache/climate
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import urllib2, httplib
from os.path import expanduser, join


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
    data = json.loads(request.body)
    config_name = data.get('config_name')
    data_name = data['metadata'].get('name')
    server = data.get('server')
    esgf_user = data.get('esgf_user')
    esgf_password = data.get('esgf_password')

    if not data_name:
        print_message('No data_name given')
        return HttpResponse(status=400)
    if not server:
        print_message('No server given')
        return HttpResponse(status=400)
    if not esgf_user:
        print_message('No esgf_user given')
        return HttpResponse(status=400)
    if not esgf_password:
        print_message('No esgf_password given')
        return HttpResponse(status=400)
    client_config = {
        'server': server,
        'openid': esgf_user,
        'password': esgf_password
    }
    config = {
        'scan': {
            'options': '',
            'path': '',
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
        config['metadata'] = []
        config['facets'] = []
        for field in PublishConfig._meta.get_fields():
            item = str(field).split('.')[-1]
            if item != 'facets':
                if item == 'id' or item == 'config_name':
                    continue
                config['metadata'].append({
                    'name': item,
                    'value': getattr(res, item)
                })
            else:
                facets = json.loads(getattr(res, item))
                for k in facets:
                    print k, facets[k]
                    config['facets'].append({
                        'name': k,
                        'value': facets[k]
                    })
    else:
        config = {
            'metadata': [
                {
                    'name': 'name',
                    'value': data_name
                },{
                    'name': 'organization',
                    'value': data.get('organization')
                },{
                    'name': 'firstname',
                    'value': data.get('firstname')
                },{
                    'name': 'lastname',
                    'value': data.get('lastname')
                }, {
                    'name': 'description',
                    'value': data.get('description')
                }, {
                    'name': 'datanode',
                    'value': data.get('data_node')
                }
            ],
            'facets': [],
            'scan': {
                'options': '',
                'path': '',
            },
            'publish': {
                'options': {
                    'files': 'all'
                },
                'files': [],
            },
        }
        facets = data.get('facets')
        for k in facets:
            config['facets'].append({
                'name': k,
                'value': facets[k]
            })
    client = IngestionClient(client_config)
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
