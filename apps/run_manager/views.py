from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import json
import os
from constants import RUN_SCRIPT_PATH, TEMPLATE_PATH, RUN_CONFIG_DEFAULT_PATH, POLLER_URL
from util.utilities import print_debug, print_message
from models import ModelRun, RunScript
import shutil
import requests


#
# Creates a new model run configuration
# input: user, the user requesting a new run config folder
#        run_name, the name of the new run config
#        run_type, the type of the run being created (model, diagnostic)
#        optional, template, the name of their predefined template
@login_required
def create_run(request):
    print request.body
    data = json.loads(request.body)
    user = str(request.user)
    path = os.path.abspath(os.path.dirname(__file__))
    user_directory = path + RUN_SCRIPT_PATH + user
    template_directory = path + TEMPLATE_PATH
    config_path = path + RUN_CONFIG_DEFAULT_PATH

    if not os.path.exists(user_directory):
        print_message("Creating directory {}".format(user_directory), 'ok')
        os.makedirs(user_directory)

    new_run = data.get('run_name')
    if not new_run:
        print_message('No new run_name specied', 'error')
        return HttpResponse(status=400)

    new_run_dir = os.path.join(user_directory, new_run)
    if os.path.exists(new_run_dir):
        print_message('Run directory already exists', 'error')
        return HttpResponse(status=409)

    try:
        os.makedirs(new_run_dir)
    except Exception as e:
        print_debug(e)
        return HttpResponse(status=500)

    try:
        run = ModelRun(user=request.user)
        run.save()
    except Exception as e:
        print_message("Error saving run {} in database for user {}".format(new_run_dir, request.user), 'error')
        shutil.rmtree(new_run_dir, ignore_errors=True)
        print_debug(e)
        return JsonResponse({'error': 'error saving run in database'})

    run_type = data.get('run_type')
    if not run_type:
        print_message('No run_type specied', 'error')
        return HttpResponse(status=400)

    config_path += run_type + '.json'
    try:
        shutil.copyfile(config_path, new_run_dir + '/config.json')
    except Exception as e:
        print_debug(e)
        print_message("Error saving config file {} for user {}".format(config_path, user), 'error')
        return JsonResponse({'error': 'config not saved'})


    template = data.get('template')
    if not template:
        return JsonResponse({'new_run_dir': new_run_dir})

    if user in template:
        template_search_dirs = [user]
    else:
        template_search_dirs = [user, 'global']

    template = template.split('/')[-1]
    found_template = False
    template_path = False
    template_search_dirs = [ str(template_directory + x) for x in template_search_dirs]
    for directory in template_search_dirs:
        if os.path.exists(directory):
            if template in os.listdir(directory):
                found_template = True
                template_path = directory + '/' + template
        else:
            os.mkdir(directory)

    if found_template:
        try:
            shutil.copyfile(template_path, new_run_dir + '/' + template)
        except Exception as e:
            print_debug(e)
            print_message("Error saving template {} for user {}".format(template, request.user), 'error')
            return JsonResponse({'new_run_dir': new_run_dir, 'error': 'template not saved'})
        return JsonResponse({'new_run_dir': new_run_dir, 'template': 'template saved'})
    else:
        return JsonResponse({'new_run_dir': new_run_dir, 'error': 'template not found'})



#
# Starts a run by passing it over to the poller
# input: user, the user making the job request
#        run_name, the name of the run they want to start
# returns: no user: status 302,
#          no run_name: status 400
#          file read error: status 500
#          poller request error: status 500
@login_required
def start_run(request):
    user = str(request.user)
    data = json.loads(request.body)
    print_message(data)
    run_name = data.get('run_name')
    if not run_name:
        print_message('No run name given', 'error')
        return HttpResponse(status=400)

    path = os.path.abspath(os.path.dirname(__file__))
    run_directory = path + RUN_SCRIPT_PATH + user + '/' + run_name + '/'
    config_path = None
    for f in os.listdir(run_directory):
        if f.endswith('.json'):
            config_path = f
            break
    if not config_path:
        print_message('Unable to find config file in run directory {}'.format(run_directory))
        return HttpResponse(status=500)
    config_path = run_directory + config_path
    try:
        with open(config_path, 'r') as f:
            config = f.read()
            f.close()
        config_options = json.loads(config)
    except Exception as e:
        print_message('Error reading file {}'.format(config_path))

    request = {
        'user': user,
        'request': 'new'
    }
    for key in config_options:
        request[key] = config_options[key]
    try:
        request = json.dumps(request)
        print_message(request)
        r = requests.post(POLLER_URL, request)
        if(r.status_code != 200):
            print_message('Error communicating with poller')
            return HttpResponse(status=500)
    except Exception as e:
        print_message('Error making request to poller')
        print_debug(e)
        return HttpResponse(status=500)

    return HttpResponse()


#
# Sends a stop run request to the poller
# input: user, the user making the job request
#        run_name, the name of the run they want to stop
# returns: no user: status 302,
#          no run_name: status 400
#          poller request error: status 500
def stop_run(request):
    return HttpResponse()

#
# Checks the status of all of a users running jobs
# input: user, the user making the request
# returns: a list of jobs with their statuses
#          if poller error, returns status 500
def run_status(request):
    user = str(request.user)
    params = {'user': user, 'request': 'all'}
    r = requests.get(POLLER_URL, params={'user': user, 'request': 'all'})
    if(r.status_code != 200):
        print_message('Poller error with params {}'.format(params))
        return HttpResponse(status=500)
    return HttpResponse(r.content)

#
# Delete a model run
# input: user, the user making the request
#        run_name, the name of the run to be deleted
@login_required
def delete_run(request):
    data = json.loads(request.body)
    run_directory = data.get('run_name')
    user = str(request.user)
    if not run_directory:
        return HttpResponse(status=400)

    path = os.path.abspath(os.path.dirname(__file__))
    run_directory = path + RUN_SCRIPT_PATH + str(request.user) + '/' + run_directory

    if not os.path.exists(run_directory):
        print_message("Attempt to delete directory that doesnt exist {}".format(run_directory), 'error')
        return HttpResponse(status=401)

    if user != run_directory.split('/')[-2]:
        print_message("Attempt to delete someone elses run directory", 'error')
        return HttpResponse(status=403)

    try:
        shutil.rmtree(run_directory, ignore_errors=True)
    except Exception as e:
        print_message("Error removing run directory", 'error')
        return HttpResponse(status=500)

    if os.path.exists(run_directory):
        print_message("Failed to remove directory {}".format(run_directory), 'error')
        return HttpResponse(status=500)

    return HttpResponse()

#
# View all of a users runs
# input: user, the user requesting their runs
@login_required
def view_runs(request):
    user = str(request.user)
    path = os.path.abspath(os.path.dirname(__file__))
    run_directory = path + RUN_SCRIPT_PATH + user + '/'
    if not os.path.exists(run_directory):
        try:
            os.mkdir(run_directory)
        except Exception as e:
            print_message('Error creating user directory for {}'.format(user), 'error')
            print_debug(e)
            return HttpResponse(status=500)
    run_dirs = os.listdir(run_directory)
    return HttpResponse(json.dumps(run_dirs))


#
# Create a new run script under a given run config folder
# inputs: user, the user creating a new run script
#         script_name, the name of the new script
#         run_name, the name of the run folder
#         contents, the contents of the new script
# returns: no script_name: status 400
#          no run_name: status 400
#          no contents: status 400
#          run directory not found: status 400
#          script already exists: status 403
#          file write error: status 500
#          model save error: status 500
@login_required
def create_script(request):
    data = json.loads(request.body)
    script_name = data.get('script_name')
    run_name = data.get('run_name')
    contents = data.get('contents')
    user = str(request.user)
    if not script_name:
        print_message('No script name given', 'error')
        return HttpResponse(status=400)
    if not run_name:
        print_message('No run name given', 'error')
        return HttpResponse(status=400)
    if not contents:
        print_message('No contents given', 'error')
        return HttpResponse(status=400)

    path = os.path.abspath(os.path.dirname(__file__))
    run_directory = path + RUN_SCRIPT_PATH + user + '/' + run_name
    if not os.path.exists(run_directory):
        print_message('Run directory not found {}'.format(run_directory), 'error')
        return HttpResponse(status=400)

    script_path = run_directory + '/' + script_name + '_1'
    if os.path.exists(script_path):
        print_message('Attempting to overwrite script {}'.format(script_path), 'error')
        return HttpResponse(status=403)

    try:
        newScript = RunScript(user=user, version=1, name=script_name, run=run_name)
        newScript.save()
    except Exception as e:
        print_message('Error saving model for script {}'.format(script_name), 'error')
        print_debug(e)
        return HttpResponse(status=500)

    try:
        f = open( script_path, 'w+')
        f.write(contents)
        f.close()
    except Exception as e:
        print_message('Error writing script to file {}'.format, 'error')
        print_debug(e)
        return HttpResponse(status=500)

    return HttpResponse()

#
# Changes a script to a new version, updating the content while
# maintaining a verson of the old script
# input: user, the user changing the script
#        script_name, the name of the script being changed
#        run_name, the run configuration folder the script belongs to
#        contents, the contents of the new version of the script
# return: no user: status 302
#         no script_name: status 400
#         no contents: status 400
#         run config folder doesnt exist: status 400
#         script previously does not exist: status 403
#         file write error: status 500
#         db lookup error: status 500
@login_required
def update_script(request):
    data = json.loads(request.body)
    script_name = data.get('script_name')
    run_name = data.get('run_name')
    contents = data.get('contents')
    user = str(request.user)
    if not script_name:
        print_message('No script name given', 'error')
        return HttpResponse(status=400)

    if not run_name:
        print_message('No run name given', 'error')
        return HttpResponse(status=400)
    if not contents:
        print_message('No contents given', 'error')
        return HttpResponse(status=400)
    path = os.path.abspath(os.path.dirname(__file__))
    run_directory = path + RUN_SCRIPT_PATH + user + '/' + run_name
    if not os.path.exists(run_directory):
        print_message('Run directory not found {}'.format(run_directory), 'error')
        return HttpResponse(status=400)

    try:
        run_scripts = RunScript.objects.filter(user=user, name=script_name, run=run_name)
        if not run_scripts:
            return HttpResponse(status=404)
        latest = run_scripts.latest()
        latest.version += 1
        # latest.edited = latest.edited + json.dumps({
        #    user: user,
        #    edited_date: datetime.datetime.now()
        # })
        latest.save()
    except Exception as e:
        print_message('Error finding latest script {}'.format(script_name), 'error')
        print_debug(e)
        return HttpResponse(status=500)

    script_path = run_directory + '/' + script_name
    if not os.path.exists(script_path + '_' + str(latest.version-1)):
        print_message('Run script {} cannot be updated as it doesn\'t exist'.format(script_name), 'error')
        return HttpResponse(status=403)
    script_path = script_path + '_' + str(latest.version)
    try:
        f = open(script_path, 'w+')
        f.write(contents)
        f.close()
    except Exception as e:
        print_message('Error writing script to file {}'.format, 'error')
        print_debug(e)
        return HttpResponse(status=500)

    return HttpResponse()


#
# Gets a list of all scripts stored in a run config folder
# inputs: user, the user requeting the script list
#         run_name, the name of the run config folder
# returns: no user: status 302
#          no run_name: status 400
#          request for run folder that doesnt exist: status 403
@login_required
def get_scripts(request):
    run_name = request.GET.get('run_name')
    user = str(request.user)
    if not run_name:
        print_message('No run name specified in get scripts request', 'error')
        return HttpResponse(status=400)

    path = os.path.abspath(os.path.dirname(__file__))
    run_directory = path + RUN_SCRIPT_PATH + user + '/' + run_name
    if not os.path.exists(run_directory):
        print_message('Request for config folder that doesnt exist {}'.format(run_name), 'error')
        return HttpResponse(status=403)

    try:
        script_list = []
        directory_contents = os.listdir(run_directory)
        for item in directory_contents:
            if not os.path.isdir(item):
                item = item.rsplit('_', 1)[0]
                script_list.append(item)
    except Exception as e:
        print_message('Error retrieving directory items', 'error')
        print_debug(e)
        return HttpResponse(status=500)

    return HttpResponse(json.dumps(script_list))


#
# Reads the contents of a script and sends it back to the user
# inputs: user, the user making the request
#         script_name, the name of the requested script
#         run_name, the run config folder the script belongs to
#         optional: version, the version of the script being requested, default is latest
# returns: no script_name: status 400
#          no run name: status 400
#          no file with matching version number: status 404
#          script does not exist: status 403
#          file read error: status 500
@login_required
def read_script(request):
    script_name = request.GET.get('script_name')
    run_name = request.GET.get('run_name')
    version_num = request.GET.get('version')
    user = str(request.user)
    if not script_name:
        print_message('No script name given', 'error')
        return HttpResponse(status=400)

    if not run_name:
        print_message('No run config folder given', 'error')
        return HttpResponse(status=400)

    if version_num:
        try:
            script = RunScript.objects.get(
                user=user,
                name=script_name,
                run=run_name,
                version=version_num)
        except ObjectDoesNotExist as e:
            var = RunScript.objects.filter(
                user=user,
                name=script_name,
                run=run_name)
            for i in var:
                print i, i.name, i.version
            print_message('Could not find script {} with version {}'.format(script_name, version_num), 'error')
            print_debug(e)
            return HttpResponse(status=404)
    else:
        script = RunScript.objects.filter(
            user=user,
            name=script_name,
            run=run_name).latest()
        version_num = script.version

    path = os.path.abspath(os.path.dirname(__file__))
    run_directory = path + RUN_SCRIPT_PATH + user + '/' + run_name
    script_name_exists = False
    for i in os.listdir(run_directory):
        if script_name in i:
            script_name_exists = True
            break
    if not script_name_exists:
        print_message('No matching script found in run folder {}'.format(script_name), 'error')
        return HttpResponse(status=403)
    script_path = run_directory + '/' + script_name + '_' + str(version_num)
    if not os.path.exists(script_path):
        print_message('Could not find script {} with version {}'.format(script_name, version_num), 'error')
        return HttpResponse(status=404)

    try:
        contents = ''
        with open(script_path, 'r') as f:
            for line in f:
                contents += line
    except Exception as e:
        print_message('Error reading from file {}'.format(script_path), 'error')
        print_debug(e)
        return HttpResponse(status=500)

    return JsonResponse({'script': contents})

#
# Im going to leave this unimplemented for the time being.
#
@login_required
def delete_script(request):
    return JsonResponse({})

#
# Creates a copy of a template, and adds it to the requesting users template folder
# inputs: user, the user making the request
#         template, the name of the template to be copied
#         new_template, the name of the new template to be created
# returns:
#         no user: status 302
#         no template: status 400
#         no new_template: status 400
#         file write error: status 500
@login_required
def copy_template(request):
    data = json.loads(request.body)
    user = str(request.user)
    template = data.get('template')
    new_template = data.get('new_template')
    if not template:
        print_message('No template name given', 'error')
        return HttpResponse(status=400)
    if not new_template:
        print_message('No new template name given', 'error')
        return HttpResponse(status=400)

    if user in template:
        template_search_dirs = [user]
    else:
        template_search_dirs = [user, 'global']

    path = os.path.abspath(os.path.dirname(__file__))
    template_directory = path + '/resources/'
    template = template.split('/')[-1]
    found_template = False
    template_path = False
    template_search_dirs = [ str(template_directory + x) for x in template_search_dirs]
    for directory in template_search_dirs:
        if os.path.exists(directory):
            if template in os.listdir(directory):
                found_template = True
                template_path = directory + '/' + template
        else:
            os.mkdir(directory)

    if found_template:
        try:
            print_message('copying {} to {}'.format(template_path, template_directory + user + '/' + template), 'ok')
            shutil.copy(template_path, template_directory + user + '/' + new_template)
        except Exception as e:
            print_message("Error saving template {} for user {}".format(template, request.user), 'error')
            print_debug(e)
            return JsonResponse({'error': 'template not saved'})
        return JsonResponse({'template': 'template saved'})
    else:
        return JsonResponse({'error': 'template not found'})

    return HttpResponse()

#
# returns a list of the users templates as well as all global templates
# inputs: user, the user requesting the template list
#

@login_required
def get_templates(request):
    path = os.path.abspath(os.path.dirname(__file__))
    template_list = []
    user_directory = path + RUN_SCRIPT_PATH + str(request.user)
    template_directory = path + '/resources/'
    user = str(request.user)
    template_search_dirs = [user, 'global']
    template_search_dirs = [ str(template_directory + x) for x in template_search_dirs]
    for directory in template_search_dirs:
        if os.path.exists(directory):
            for template in os.listdir(directory):
                template_list.append(directory.split('/')[-1] + '/' + template)

    return HttpResponse(json.dumps(template_list))
