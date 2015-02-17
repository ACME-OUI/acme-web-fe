from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.forms.models import model_to_dict
from django.forms.util import ErrorList
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File

##### For user registration
from forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#from acme_site.filters import
#from acme_site.models import
#from acme_site.forms import

import json
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
    check= ""
    data = ""
    if request.method == "POST":
        print "POST"
    elif request.method =="GET":
        check = request.GET.get('return')
        if check == "PENDING":
            data = "<center><font color='red'><p><h1>Accont Pending</h1>You will reviece a email with instruction once your account has been approved</p></font></center>"
    else:
        print request.method

    return HttpResponse(render_template(request, "home.html", {"data":data}))

##### Login
def user_login(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, 'User: '+ request.POST['username'] + ' successfully loged in')
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
            print "next:" + request.GET.get('next')

        else:
            redirect = 'home.html'
        response = render_to_response("acme_site/login.html", {"next": redirect}, context)
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


##### Work Flows
@login_required(login_url='login')
def workflow(request):
    return HttpResponse(render_template(request, "demo/work_flow_home.html", {}))

@login_required(login_url='login')
def code(request):
    return HttpResponse(render_template(request, "demo/work_flow_edit.html", {}))

@login_required(login_url='login')
def dashboard(request):
    return HttpResponse(render_template(request, "acme_site/dashboard.html", {}))

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



