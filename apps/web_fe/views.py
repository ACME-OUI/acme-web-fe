from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.forms.models import model_to_dict
from django.forms.utils import ErrorList
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from web_fe.models import TileLayout, Credential, ESGFNode
from pyesgf.search import SearchConnection
import sys
import json
import simplejson
import os
import urllib
import urllib2
import base64
import time
import datetime
from subprocess import Popen, PIPE
from sets import Set


# General


def render_template(request, template, context):
    template = loader.get_template(template)
    context = RequestContext(request, context)
    return template.render(context)


# Index
def index(request):
    return HttpResponse(render_template(request, "web_fe/home.html", {}))


# Login
def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user:
            if user.is_active:
                login(request, user)
                messages.success(
                    request, 'User: ' + request.POST['username'] + ' successfully loged in')
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                messages.error(
                    request, 'User: ' + request.POST['username'] + ' is a disactivated account')
                return HttpResponseRedirect('login')
        else:
            messages.error(request, "Username or password incorrect")
            return HttpResponseRedirect('login')
    else:
        if 'next' in request.GET:
            redirect = request.GET.get('next')

        else:
            redirect = ''
        response = HttpResponse(
            render_template(request, "web_fe/login.html", {"next": redirect}))
        return response


# Allows the user to add ESGF and Velo credentials to their account
@login_required
def add_credentials(request):
    if request.method == 'POST':
        print request.body
        try:
            data = json.loads(request.body)
            if len(data) != 0:
                for s in data:
                    creds = Credential.objects.filter(
                        service=s, site_user_name=str(request.user))
                    if len(creds) != 0:
                        for i in creds:
                            i.password = data[s]['password']
                            i.service_user_name = data[s]['username']
                            i.save()
                    else:
                        c = Credential(service_user_name=data[s]['username'], password=data[s][
                                       'password'], service=s, site_user_name=str(request.user))
                        c.save()

                return HttpResponse(render_template(request, 'web_fe/add_credentials.html', {'added': 'true'}))
            else:
                return HttpResponse(render_template(request, 'web_fe/add_credentials.html', {'added': 'false'}))
        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        creds = Credential.objects.filter(site_user_name=str(request.user))
        stored_credentials = []
        for s in creds:
            stored_credentials.append(s.service)
        return HttpResponse(render_template(request, 'web_fe/add_credentials.html', {'added': 'false', 'stored_credentials': stored_credentials}))

# This whole thing needs to be refactored


@login_required
def check_credentials(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response = {}
            creds = Credential.objects.filter(site_user_name=request.user)
            velo_started = False
            if len(creds) != 0:
                for c in creds:
                    try:
                        if c.service == 'esgf':
                            import pyesgf
                            from pyesgf.logon import LogonManager
                            lm = LogonManager()
                            lm.logon_with_openid(
                                c.service_user_name, c.password)
                            if lm.is_logged_on():
                                response[s] = 'success'
                                print 'esgf log in successful'
                            else:
                                print 'esgf log in failed'
                                response[s] = 'fail'
                        if c.service == 'velo':
                            lib_path = os.path.abspath(
                                os.path.join('apps', 'velo'))
                            sys.path.append(lib_path)

                            rm = velo_api.init(c.service_user_name, c.password)

                            if rm.getRepositoryUrlBase() == 'u\'http://acmetest.ornl.gov:80/alfresco\'':
                                response[s] = 'success'
                                velo_api.shutdown_jvm()
                                print 'velo log in successful'
                            else:
                                velo_api.shutdown_jvm()
                                response[s] = 'fail'
                                print 'Error in velo initialization', rm.getRepositoryUrlBase()

                        if c.service == 'github':
                            import github3
                            from github3 import login
                            gh = login(c.site_user_name, password=c.password)
                            if gh.user() == c.site_user_name:
                                print 'Github login successful'
                                response[s] = 'success'
                            else:
                                print 'Github login failure'
                                response[s] = 'fail'

                        if c.service == 'jira':
                            print 'Working on jira....'
                    except:
                        print_debug(e)
                        return HttpResponse(status=500)

            return HttpResponse(json.dumps(response))

        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=404)


# Logout
def user_logout(request):
    logout(request)
    messages.success(request, 'Log out successful')
    return HttpResponse(render_template(request, "web_fe/home.html", {'logout': 'success    '}))


# Register new user
def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserCreationForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            try:
                group = Group.objects.get(name="Default")
                user.groups.add(group)
            except Group.DoesNotExist:
                # Don't do anything, no default set up
                pass

            user.save()
            registered = True
            user = authenticate(
                username=request.POST['username'], password=request.POST['password1'])
            if user:
                login(request, user)
                messages.success(
                    request, 'User: ' + request.POST['username'] + ' successfully created an account and logged in')
        else:
            print user_form.errors
    else:
        user_form = UserCreationForm()

    return render_to_response("web_fe/register.html", {"user_form": user_form, "registered": registered}, context)


@login_required
def dashboard(request):
    import xml.etree.ElementTree as ET
    import requests
    from StringIO import StringIO

    nodes = ESGFNode.objects.all()
    if len(nodes) == 0:
        # bootstrapping off of the australian node since its up
        bootstrap_node = ESGFNode(host='esg2.nci.org.au')
        bootstrap_node.save()
        bootstrap_node.refresh()
        print bootstrap_node.node_data
    else:
        for node in nodes:
            node.refresh()

    return HttpResponse(render_template(request, "web_fe/dashboard.html", {}))


@login_required
def save_layout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if len(TileLayout.objects.filter(layout_name=data['name'])) == 0:
                if data['default_layout'] == 1:
                    isDefault = TileLayout.objects.filter(
                        user_name=request.user, default=1)
                    if isDefault:
                        for i in isDefault:
                            i.default = 0
                            i.save()

                layout = TileLayout(user_name=request.user, layout_name=data['name'], board_layout=json.dumps(
                    data['layout']), mode=data['mode'], default=data['default_layout'])
                layout.save()
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=422)
        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)


@login_required
def load_layout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            layout = TileLayout.objects.filter(layout_name=data['layout_name'])
            if len(layout) == 0:
                return HttpResponse(status=500)

            j = {}
            for i in layout:
                j['board_layout'] = json.loads(i.board_layout)
                j['mode'] = i.mode
                return HttpResponse(json.dumps(j), status=200, content_type="application/json")
        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    elif request.method == 'GET':
        try:
            all_layouts = TileLayout.objects.filter(user_name=request.user)
            layouts = []
            for layout in all_layouts:
                curlayout = {}
                curlayout['name'] = layout.layout_name
                curlayout['default'] = layout.default
                curlayout['layout'] = json.loads(layout.board_layout)
                curlayout['mode'] = layout.mode
                layouts.append(curlayout)
            return HttpResponse(json.dumps(layouts))
        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)


@login_required
def node_info(request):
    if request.method == 'GET':
        try:
            response = {}
            nodes = ESGFNode.objects.all()
            for node in nodes:
                response[node.short_name] = node.node_data
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
    elif request.method == 'POST':
        print "Unexpected POST request"
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
        return HttpResponse(status=500)


@login_required
def get_folder(request):
    if request.method == 'POST':
        folder = json.loads(request.body)
        try:
            cred = Credential.objects.get(
                site_user_name=request.user, service='velo')
            process = Popen(
                ['python', './apps/velo/get_folder.py', folder['file'], cred.service_user_name, cred.password], stdout=PIPE)
            (out, err) = process.communicate()
            exit_code = process.wait()
            out = out.splitlines(False)
            out.insert(0, folder['file'])
            return HttpResponse(json.dumps(out))

        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=404)


@login_required
def get_file(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            filename = data['filename']
            remote_file_path = data['path'] + '/' + filename
            cred = Credential.objects.get(
                site_user_name=request.user, service='velo')

            local_path = os.getcwd() + '/userdata/' + \
                cred.service_user_name + '/'

            # Create the local directories if they dont exist
            remote_path = remote_file_path.split('/')
            prefix = local_path[
                :local_path.index(cred.service_user_name) + len(cred.service_user_name)] + '/'
            if not os.path.isdir(prefix):
                os.makedirs(prefix)

            for i in range(remote_path.index(cred.service_user_name) + 1, len(remote_path) - 1):
                if not os.path.isdir(prefix + remote_path[i]):
                    prefix += remote_path[i] + '/'
                    os.makedirs(prefix)

            process = Popen(
                ['python', './apps/velo/get_file.py', remote_file_path, prefix, filename, cred.site_user_name, cred.service_user_name, cred.password], stdout=PIPE)
            (out, err) = process.communicate()
            exit_code = process.wait()
            if exit_code == -1 or 'NO SUCH FILE' in out:
                print out
                return HttpResponse(status=500)

            path = prefix + filename
            path_components = path.split("/")
            path = os.path.join(
                path_components[path_components.index(cred.service_user_name) + 1:])
            if filename.split('.').pop() == 'png':
                response = {
                    'type': 'image',
                    'location': path
                }
                return HttpResponse(json.dumps(response))
            else:
                out = out.splitlines(True)[1:]
                return HttpResponse(out, content_type='text/plain')

        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=404)


@login_required
def send_image(request, path):
    from sendfile import sendfile
    import os
    cred = Credential.objects.get(service='velo', site_user_name=request.user)
    fullpath = os.path.join('userdata', cred.service_user_name, path)

    print fullpath
    if os.path.isfile(fullpath):
        return sendfile(request, fullpath)
    else:
        return HttpResponse(status=404)


@login_required
def velo_save_file(request):
    if request.method == 'POST':
        try:
            incoming_file = json.loads(request.body)
            filename = incoming_file['filename']
            remote_path = incoming_file['remote_path']
            text = incoming_file['text']

            cred = Credential.objects.get(
                site_user_name=request.user, service="velo")

            remote_path = remote_path[:remote_path.index(filename)]
            print 'filename:', filename, 'remote_path:', remote_path

            process = Popen(
                ['python', './apps/velo/save_file.py', text, filename, remote_path, cred.site_user_name, cred.service_user_name, cred.password], stdout=PIPE)
            (out, err) = process.communicate()
            exit_code = process.wait()
            if exit_code >= 0 and 'File saved' in out:
                return HttpResponse(status=200)
            else:
                print out, err
                return HttpResponse(status=500)
        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=404)


@login_required
def velo_delete(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data['name']

            cred = Credential.objects.get(
                site_user_name=request.user, service="velo")

            process = Popen(
                ['python', './apps/velo/delete.py', name, cred.service_user_name, cred.password], stdout=PIPE)
            (out, err) = process.communicate()
            exit_code = process.wait()
            if exit_code >= 0:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=500)
        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=404)


@login_required
def velo_new_folder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            foldername = data['foldername']

            cred = Credential.objects.get(
                site_user_name=request.user, service="velo")

            process = Popen(
                ['python', './apps/velo/new_folder.py', foldername, cred.service_user_name, cred.password], stdout=PIPE)
            (out, err) = process.communicate()
            exit_code = process.wait()

            if exit_code >= 0 and 'Created new folder' in out:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=500)
        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=404)


@login_required
def credential_check_existance(request):
    if request.method == 'POST':
        try:
            service = json.loads(request.body)['service']
            cred = Credential.objects.filter(
                site_user_name=request.user, service=service)
            if len(cred) != 0:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=500)
        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=404)


def print_debug(e):
    import traceback
    print '1', e.__doc__
    print '2', sys.exc_info()
    print '3', sys.exc_info()[0]
    print '4', sys.exc_info()[1]
    print '5', traceback.tb_lineno(sys.exc_info()[2])
    ex_type, ex, tb = sys.exc_info()
    print '6', traceback.print_tb(tb)
