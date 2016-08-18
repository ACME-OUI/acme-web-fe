from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.forms.models import model_to_dict
from django.forms.utils import ErrorList
from django.core.files import File
from forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from web_fe.models import TileLayout, Credential
import json
import simplejson
import os
import urllib
import urllib2
import base64
import time
import requests
from sendfile import sendfile
from util.utilities import print_debug
from django.views.decorators.csrf import csrf_exempt


def render_template(request, template, context):
    template = loader.get_template(template)
    context = RequestContext(request, context)
    return template.render(context)


# Index
def index(request):
    return HttpResponse(render_template(request, "web_fe/home.html", {}))


# Login
@csrf_exempt
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
                return HttpResponseRedirect('/acme')
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
                res = render_template(request, 'web_fe/add_credentials.html', {'added': 'true'})
                return HttpResponse(res)
            else:
                res = render_template(request, 'web_fe/add_credentials.html', {'added': 'false'})
                return HttpResponse(res)
        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        creds = Credential.objects.filter(site_user_name=str(request.user))
        stored_credentials = []
        for s in creds:
            stored_credentials.append(s.service)
        response = {'added': 'false', 'stored_credentials': stored_credentials}
        return HttpResponse(render_template(request, 'web_fe/add_credentials.html', response))

# This whole thing needs to be refactored


@login_required
def check_credentials(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response = {}
            creds = Credential.objects.filter(site_user_name=request.user)
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
                            user, password = c.service_user_name, c.password
                            velo_creds = {
                                "velo_user": user,
                                "velo_pass": password,
                                "command": "init"
                            }
                            result = velo_request(velo_creds)
                            # TODO: Extract values out to CAPITAL_NAMED_CONSTANTS
                            if result == "Success":
                                print "velo login successful"
                            else:
                                print "velo login failed"
                                response[s] = "fail"

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
                        print_debug(c)
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
                message = 'User: {} created an account and logged in'.format(request.POST['username'])
                messages.success(request, message)
        else:
            print user_form.errors
    else:
        user_form = UserCreationForm()

    data = {
        "user_form": user_form,
        "registered": registered
    }
    return render_to_response("web_fe/register.html", data, context)


@login_required
def dashboard(request):
    import xml.etree.ElementTree as ET
    from StringIO import StringIO
    try:
        from local_settings import VISUALIZATION_LAUNCHER
    except ImportError:
        VISUALIZATION_LAUNCHER = None
        '''
    nodes = ESGFNode.objects.all()
    r = requests.get(
        'https://pcmdi.llnl.gov/esgf-node-manager/registration.xml')
    if r.status_code == 200:
        print "######### Node Manager is back online!  ############"
        tree = ET.parse(StringIO(r.content))
        for node in tree.getroot():
            print node
            new_node = ESGFNode(host=node.attrib['hostname'])
            new_node.save()
        for node in ESGFNode.objects.all():
            print "refreshing"
            node.refresh()
    else:
        if len(nodes) == 0:
            # bootstrapping off of the australian node since its up
            bootstrap_node = ESGFNode(host='esg2.nci.org.au')
            bootstrap_node.save()
            bootstrap_node.refresh()
            print bootstrap_node.node_data
        else:
            node_list = [
                'dev.esg.anl.gov', 'esg.bnu.edu.cn', 'esg.ccs.ornl.gov']
            for node_name in node_list:
                new_node = ESGFNode.objects.filter(host=node_name)
                if len(new_node) == 0:
                    new_node = ESGFNode(host=node_name)
                    new_node.save()

            for node in nodes:
                node.refresh()
                    '''
    data = {'vis_launcher': VISUALIZATION_LAUNCHER}
    return HttpResponse(render_template(request, "web_fe/dashboard.html", data))

    '''
    import xml.etree.ElementTree as ET
    from StringIO import StringIO
    try:

        from django.conf import settings
        VISUALIZATION_LAUNCHER = settings.VISUALIZATION_LAUNCHER
    except ImportError:
        VISUALIZATION_LAUNCHER = None
    data = {'vis_launcher': VISUALIZATION_LAUNCHER}
    return HttpResponse(render_template(request, "web_fe/dashboard.html", data))
    '''


@login_required
def save_layout(request):
    print "got save request"
    if request.method == 'POST':
        try:
            print "got post save request"
            data = json.loads(request.body)
            layout = TileLayout.objects.filter(
                layout_name=data['name'], user_name=str(request.user))
            if len(layout) == 0:
                if data['default_layout'] == 1:
                    print 'got to 1'
                    isDefault = TileLayout.objects.filter(
                        user_name=request.user, default=1)
                    if isDefault:
                        for i in isDefault:
                            i.default = 0
                            i.save()

                layout = TileLayout(
                    user_name=str(request.user),
                    layout_name=data['name'],
                    board_layout=json.dumps(data['layout']),
                    mode=data['mode'],
                    default=data['default_layout'])
                layout.save()
                return HttpResponse(status=200)
            else:
                print 'got to 2'
                print data['name']
                print data['default_layout']
                for x in layout:
                    x.board_layout = json.dumps(data['layout'])
                    x.mode = data['mode']
                    x.default = data['default_layout']
                    x.save()
                return HttpResponse(status=200)
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


@login_required
def send_image(request, path):
    fullpath = os.path.join(os.getcwd(), path)

    if os.path.isfile(fullpath):
        return sendfile(request, fullpath)
    else:
        return HttpResponse(status=404)
