from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.forms.models import model_to_dict
from django.forms.util import ErrorList
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
import sys

##### For user registration
from forms import UserCreationForm
from forms import IssuesForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#from acme_site.filters import
from acme_site.models import TileLayout
#from acme_site.forms import

import json
import xmltodict
import simplejson
import os
import urllib
import urllib2
import base64
import time
import datetime


##### General
def render_template(request, template, context):
    template = loader.get_template(template)
    context = RequestContext(request, context)
    return template.render(context)

def not_done(request, *args, **kwargs):
    return HttpResponse("Stub")

##### Index
def index(request):
    return HttpResponse(render_template(request, "home.html", {}))

##### Issues
@login_required(login_url='login')
def issues(request):
    form = IssuesForm()

    return HttpResponse(render_template(request, "issues.html", {"form":form}))

##### Login
def user_login(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, 'User: '+ request.POST['username'] + ' successfully loged in')
                print 'POSTnext: ' + request.POST.get('next')
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                messages.error(request, 'User: ' + request.POST['username'] + ' is a disactivated account')
                return HttpResponseRedirect('login')
        else:
            messages.error(request, "Username or password incorrect")
            return HttpResponseRedirect('login')
    else:
        if 'next' in request.GET:
            redirect = request.GET.get('next')
            print "GETnext:" + request.GET.get('next')

        else:
            redirect = ''
        print 'redirect:' + redirect
        response = HttpResponse(render_template(request, "acme_site/login.html", {"next": redirect}))
        return response

##### Logout
def user_logout(request):
    logout(request)
    messages.success(request, 'Log out successful')
    return HttpResponse(render_template(request, "home.html", {}))

##### Register new user
def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserCreationForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserCreationForm()
   
    return render_to_response("acme_site/register.html", {"user_form": user_form, "registered": registered}, context)

def slick(request):
    return HttpResponse(render_template(request, "acme_site/slick.html", {}))

##### Work Flows
@login_required(login_url='login')
def workflow(request):
    return HttpResponse(render_template(request, "demo/work_flow_home.html", {}))

@login_required(login_url='login')
def code(request):
    return HttpResponse(render_template(request, "demo/work_flow_edit.html", {}))

@login_required(login_url='login')
def jspanel(request):
    return HttpResponse(render_template(request, "acme_site/jspanel.html", {}))

@login_required(login_url='login')
def grid(request):
    ''' For demo purposes this is loading a local file '''    
    from xml.etree.ElementTree import parse
    tree = parse('acme_site/demo_data/registration.xml')

    node_name_list = []
    node_peer_list = []
    node_url_list = []
    node_location_list = []
    for node in tree.getroot():
        attrs = node.attrib
        node_name_list.append(attrs["shortName"])
        node_peer_list.append(attrs["adminPeer"])
        node_url_list.append(attrs["hostname"])
        for child in node:
            if child.tag[-11:] == "GeoLocation":
                node_location_list.append(child.attrib["city"])
    node_list = zip(node_peer_list, node_url_list, node_name_list, node_location_list)
    print node_list, node_peer_list, node_url_list, node_name_list, node_location_list
    return HttpResponse(render_template(request, "acme_site/grid.html", {'nodes': node_list}))


@login_required(login_url='login')
def save_layout(request):
    print 'got a save request'
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if len(TileLayout.objects.filter(layout_name=data['name'])) == 0:
                if data['default_layout'] == 1:
                    print 'got a new default'
                    isDefault = TileLayout.objects.filter(user_name=request.user, default=1)
                    if isDefault:
                        for i in isDefault:
                            print 'found old default named ' + i.layout_name
                            i.default = 0
                            i.save()
                    
                layout = TileLayout(user_name=request.user, layout_name=data['name'], board_layout=json.dumps(data['layout']), mode=data['mode'], default=data['default_layout'])
                layout.save()
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=422)
        except Exception as e:
            print "Unexpected error:", repr(e)
            return HttpResponse(status=500)


@login_required(login_url='login')
def load_layout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            layout = TileLayout.objects.filter(layout_name=data['layout_name'])
            j = {}
            for i in layout:
                j['board_layout'] = json.loads(i.board_layout)
                j['mode'] = i.mode
                return HttpResponse(json.dumps(j), status=200, content_type="application/json")
        except Exception as e:
            print "Unexpected error:", repr(e)
            return HttpResponse(status=500)
    elif request.method == 'GET':
        all_layouts = TileLayout.objects.filter(user_name=request.user)
        print all_layouts
        layouts = []
        for layout in all_layouts:
            curlayout = {}
            curlayout['name'] = layout.layout_name
            curlayout['default'] = layout.default
            curlayout['layout'] = json.loads(layout.board_layout)
            curlayout['mode'] = layout.mode
            layouts.append(curlayout)
        return HttpResponse(json.dumps(layouts))

@login_required
def node_info(request):
    if request.method == 'POST':
        ''' For demo purposes this is loading a local file '''
        try:
            from xml.etree.ElementTree import parse

            tree = parse('acme_site/demo_data/registration.xml')
            root = tree.getroot()
            name = json.loads(request.body)['node']
            
            response = {}
            for node in root:
                if node.attrib['shortName'] == name:
                    response['org'] = node.attrib['organization']
                    response['namespace'] = node.attrib['namespace']
                    response['email'] = node.attrib['supportEmail']
                    response['ip'] = node.attrib['ip']
                    response['longName'] = node.attrib['longName']
                    response['version'] = node.attrib['version']
                    response['shortName'] = name
                    response['adminPeer'] = node.attrib['adminPeer']
                    response['hostname'] = node.attrib['hostname']


                    for child in list(node):
                        if child.tag[-len('AuthorizationService'):] == "AuthorizationService":
                            response['authService'] = child.attrib["endpoint"]
                        if child.tag[-len('GeoLocation'):] == "GeoLocation":
                            response['location'] = child.attrib["city"]
                        if child.tag[-len('Metrics'):] == "Metrics":
                            for gchild in list(child):
                                if gchild.tag[-len('DownloadedData'):] == "DownloadedData":
                                    response['dataDownCount'] = gchild.attrib['count']
                                    response['dataDownSize'] = gchild.attrib['size']
                                    response['dataDownUsers'] = gchild.attrib['users']
                                if gchild.tag[-len('RegisteredUsers'):] == "RegisteredUsers":
                                    response['registeredUsers'] = gchild.attrib['count']


                    from pyesgf.search import SearchConnection
                    print 'attempting to connect to ' + 'http://' + response['hostname'] + 'esg-search/'
                    conn = SearchConnection('http://' + response['hostname'] + '/esg-search/', distrib=True)
                    try:
                        conn.get_shard_list()
                        response['status'] = 'up'
                    except Exception as e:
                        print repr(e)
                        response['status'] = 'down'


                    return HttpResponse(json.dumps(response))
        except Exception as e:
            print "Unexpected error:", repr(e)
            return HttpResponse(status=500)
    elif request.method == 'POST':
        print "Unexpected POST request"
        return HttpResponse(status=500)

@login_required
def node_search(request):
    if request.method == 'POST':
        from pyesgf.search import SearchConnection
        import random
        searchString = json.loads(request.body)
        print searchString
        if 'node' in searchString:
            if 'test_connection' in searchString:
                try:
                    print 'testing connection to', searchString['node']
                    conn = SearchConnection(searchString['node'], distrib=True)
                    context = conn.new_context()
                    response = {}
                    response['status'] = 'success'
                    return HttpResponse(json.dumps(context.get_facet_options()))
                except Exception as e:
                    print "Unexpected error:", repr(e)
                    return HttpResponse(status=500)
            else:
                try:
                    conn = SearchConnection(searchString['node'], distrib=True)
                    del searchString["node"]
                    print 'Searching:', searchString
                    context = conn.new_context(**searchString)
                    searchResponse = {}
                    searchResponse['hits'] = context.hit_count
                    print 'hits', context.hit_count
                    print 'realms', context.facet_counts['realm']
                    return HttpResponse(json.dumps(searchResponse))
                except Exception as e:
                    print "Unexpected error:", repr(e)
                    return HttpResponse(status=500)
        else:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=500)



@login_required(login_url='login')
def config(request):
    return HttpResponse(render_template(request, "acme_site/work_flows/work_flow_config.html", {}))

@login_required(login_url='login')
def inputs(request):
    return HttpResponse(render_template(request, "acme_site/work_flows/work_flow_inputs.html", {}))

@login_required(login_url='login')
def build(request):
    return HttpResponse(render_template(request, "acme_site/work_flows/work_flow_build.html", {}))

@login_required(login_url='login')
def run(request):
    return HttpResponse(render_template(request, "acme_site/work_flows/work_flow_run.html", {}))

@login_required(login_url='login')
def output(request):
    return HttpResponse(render_template(request, "acme_site/work_flows/work_flow_output.html", {}))


### AJAX
@csrf_exempt
def gettemplates(request): 
    ## GET call ##
    status = ""
    try:
        inputstring = request.POST.get('user')
        inputjson = simplejson.loads(inputstring)
        
        username = inputjson['username']
        password = inputjson['password']
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

        url = "https://acmetest.ornl.gov/alfresco/service/cssef/listWorkflowPackageTemplates"
        request = urllib2.Request(url)
        request.add_header("Authorization", "Basic %s" % base64string)
        response = urllib2.urlopen(request)
        page = response.read()
        
        status = page
    except Exception,e:
        status = "fail: " + str(e)
    json_data = {}
    json_data['key'] = status
    return HttpResponse(json.dumps(json_data))

@csrf_exempt
def clonetemplates(request):
    ## POST call ##
    status = ""
    try:
        inputstring = request.POST.get('user')
        inputjson = simplejson.loads(inputstring)
        
        username = inputjson['username']
        password = inputjson['password']
        template = inputjson['template']
        case = template + "_" + username + "_" + datetime.datetime.now().isoformat()
        data_args = {'caseName':case,'templateName':template}
        data = urllib.urlencode(data_args)
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

        url = "https://acmetest.ornl.gov/alfresco/service/cssef/cloneWorkflowPackageTemplate"
        request = urllib2.Request(url, data)
        request.add_header("Authorization", "Basic %s" % base64string)
        response = urllib2.urlopen(request)
        page = response.read()
        status = "success"
    except Exception,e:
        status = "fail: " + str(e)

    json_data = {}
    json_data['key'] = status
    return HttpResponse(json.dumps(json_data))

@csrf_exempt
def getchildren(request):
    ## GET call ##
    status = ""
    try:
        inputstring = request.POST.get('user')
        inputjson = simplejson.loads(inputstring)
        
        username = inputjson['username']
        password = inputjson['password']
        path = inputjson['path']
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

        url = "https://acmetest.ornl.gov/alfresco/service/cat/getChildren?path=" + path
        request = urllib2.Request(url)
        request.add_header("Authorization", "Basic %s" % base64string)
        response = urllib2.urlopen(request) 
        page = response.read()
        status = page
    except Exception,e:
        status = "fail: " + str(e)
    
    json_data = {}
    json_data['key'] = status
    return HttpResponse(json.dumps(json_data))

@csrf_exempt
def getfile(request):
    ## GET call ##
    status = ""
    try:
        inputstring = request.POST.get('user')
        inputjson = simplejson.loads(inputstring)
        
        username = inputjson['username']
        password = inputjson['password']
        path = inputjson['path']
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

        url = "https://acmetest.ornl.gov/alfresco/service/cat/getFileContents?path=" + path
        request = urllib2.Request(url)
        request.add_header("Authorization", "Basic %s" % base64string)
        response = urllib2.urlopen(request) 
        page = response.read()
        status = page
    except Exception,e:
        status = "fail: " + str(e)
    
    json_data = {}
    json_data['key'] = status
    return HttpResponse(json.dumps(json_data))

@csrf_exempt
def savefile(request):
     ## POST call ##
    status = ""
    try:
        inputstring = request.POST.get('user')
        inputjson = simplejson.loads(inputstring)
        
        username = inputjson['username']
        password = inputjson['password']
        path = inputjson['path']
        content = inputjson['content']

        data_args = {'path':path,'content':content}
        data = urllib.urlencode(data_args)
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

        url = "https://acmetest.ornl.gov/alfresco/service/cat/upload"
        
        #request = urllib2.Request(url, data)
        #request.add_header("Authorization", "Basic %s" % base64string)
        #response = urllib2.urlopen(request)
        #page = response.read()
        #status = page
        status = "success"
    except Exception,e:
        status = "fail: " + str(e)
    json_data = {}
    json_data['key'] = status
    return HttpResponse(json.dumps(json_data))

@csrf_exempt
def getresource(request):
    ## GET call ##
    status = ""
    try:
        inputstring = request.POST.get('user')
        inputjson = simplejson.loads(inputstring)
        
        username = inputjson['username']
        password = inputjson['password']
        path = inputjson['path']
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

        url = "https://acmetest.ornl.gov/alfresco/service/cssef/getResource?path=" + path
        print url
        request = urllib2.Request(url)
        request.add_header("Authorization", "Basic %s" % base64string)
        print request
        response = urllib2.urlopen(request) 
        print response
        page = response.read()
        print page
        status = page
    except Exception,e:
        status = "fail: " + str(e)
        print status
    json_data = {}
    json_data['key'] = status
    return HttpResponse(json.dumps(json_data))

#### FILE TREE PLUG IN ####
@csrf_exempt
def filetree(request):
   r=['<ul class="jqueryFileTree" style="display: none;">']
   try:
       r=['<ul class="jqueryFileTree" style="display: none;">']
       d=urllib.unquote(request.POST.get('dir','/Users/harris112/Projects/aims/acme-site'))
       for f in os.listdir(d):
           ff=os.path.join(d,f)
           if os.path.isdir(ff):
               r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
           else:
               e=os.path.splitext(f)[1][1:] # get .ext and remove dot
               r.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e,ff,f))
       r.append('</ul>')
   except Exception,e:
       r.append('Could not load directory: %s' % str(e))
   r.append('</ul>')
   return HttpResponse(''.join(r))



