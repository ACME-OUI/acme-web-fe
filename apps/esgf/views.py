from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from util.utilities import get_client_ip, print_debug
from django.contrib.auth.decorators import login_required
from models import ESGFNode
from pyesgf.logon import LogonManager
from pyesgf.search import SearchConnection
from constants import ESGF_SEARCH_SUFFIX, ESGF_CREDENTIALS, NODE_HOSTNAMES
from run_manager.constants import USER_DATA_PREFIX
import json
import requests
import os.path
import shutil
from subprocess import call

from util.utilities import print_debug, print_message


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


class HTTPSClientAuthHandler(urllib2.HTTPSHandler):
    '''
    HTTP handler that transmits an X509 certificate as part of the request
    '''

    def __init__(self, key, cert):
            urllib2.HTTPSHandler.__init__(self)
            self.key = key
            self.cert = cert

    def https_open(self, req):
            return self.do_open(self.getConnection, req)

    def getConnection(self, host, timeout=300):
            return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)


def esgf_download(url, toDirectory="/tmp"):
    '''
    Function to download a single file from ESGF.

    :param url: the URL of the file to download
    :param toDirectory: target directory where the file will be written
    '''

    # setup HTTP handler
    certFile = expanduser(ESGF_CREDENTIALS)
    opener = urllib2.build_opener(HTTPSClientAuthHandler(certFile,certFile))
    opener.add_handler(urllib2.HTTPCookieProcessor())

    # download file
    localFilePath = join(toDirectory,url.split('/')[-1])
    print "\nDownloading url: %s to local path: %s ..." % (url, localFilePath)
    localFile = open( localFilePath, 'w')
    webFile = opener.open(url)
    localFile.write(webFile.read())

    # cleanup
    localFile.close()
    webFile.close()
    opener.close()
    print "... done"


#
# Downloads the requested file from ESGF
#
# input: username (an OpenID), password, search_string, nodes, data_type (model/obs), data_name (a name for the folder the data will go into)
def download(request):
    user = str(request.user)
    username = request.GET.get('openid_username')
    password = request.GET.get('openid_password')
    search_string = json.loads(request.GET.get('search_string'))
    nodes = request.GET.get('nodes')
    data_type = request.GET.get('data_type')
    data_name = request.GET.get('data_name')
    if not username:
        print_message('No username given')
        return HttpResponse(status=400)
    if not password:
        print_message('No password given')
        return HttpResponse(status=400)
    if not search_string:
        print_message('No search_string given')
        return HttpResponse(status=400)
    if not nodes:
        print_message('No nodes given')
        return HttpResponse(status=400)
    if not data_type:
        print_message('No data_type given')
        return HttpResponse(status=400)
    if not data_name:
        print_message('No data_name given')
        return HttpResponse(status=400)

    lm = LogonManager()
    lm.logon_with_openid(username, password, bootstrap=True)
    if not lm.is_logged_on():
        return HttpResponse(status=403)
    for node in nodes:
        try:
            print '[+] searching {node} for {string}'.format(node=node, string=search_string)
            conn_string = 'http://{node}{suffix}'.format(node=node, suffix=ESGF_SEARCH_SUFFIX)
            conn = SearchConnection(conn_string, distrib=True)
            context = conn.new_context(**search_string)
            rs = context.search()
            print_message('got reply from {node}'.format(node=node))
            if len(rs) == 0:
                continue
            url = rs[0].url
            directory = USER_DATA_PREFIX + user
            if data_type == 'obs':
                directory += '/observations'
            elif data_type == 'model':
                directory += '/model_output'

            print_message('Downloading {url} to {dir}'.format(url=url, dir=directory))
            esgf_download(url, directory)

        except Exception as e:
            print_debug(e)
            return HttpResponse(status=400)
    return HttpResponse(status=200)


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
def get_user_data(request):
    user = str(request.user)
    path = os.path.abspath(os.path.dirname(__file__)) + '/../../userdata/' + user
    userdata = get_directory_structure(path)
    return HttpResponse(json.dumps(userdata))


# see: http://code.activestate.com/recipes/577879-create-a-nested-dictionary-from-oswalk/
def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir
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
