from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import json
import os
from constants import RUN_SCRIPT_PATH
from util.utilities import print_debug, print_message
from models import ModelRun
import shutil


#
# Creates a new model run configuration
# input: user, the user requesting a new run config folder
#        run_name, the name of the new run config
#        optional: template, the name of their predefined template
@login_required
def create_run(request):
    path = os.path.abspath(os.path.dirname(__file__))
    user_directory = path + RUN_SCRIPT_PATH + str(request.user)

    # TODO: make this not hard coded
    template_directory = path + '/resources/'
    if not os.path.exists(user_directory):
        print_message("Creating directory {}".format(user_directory), 'ok')
        os.makedirs(user_directory)


    new_run = request.POST.get('run_name')
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

    template = request.POST.get('template')
    if not template:
        return JsonResponse({'new_run_dir': new_run_dir})
    else:
        found_template = False
        template_path = False
        template_search_dirs = [str(request.user), 'global']
        template_search_dirs = [ str(template_directory + x) for x in template_search_dirs]
        print "template_search_dirs {}".format(template_search_dirs)
        for directory in template_search_dirs:
            if os.path.exists(directory):
                if template in os.listdir(directory):
                    found_template = True
                    template_path = directory + '/' + template
            else:
                os.mkdir(directory)

        if found_template:
            try:
                shutil.copyfile(template_path, template_directory + '/' + str(request.user) + '/'+ template)
            except Exception as e:
                print_debug(e)
                print_message("Error saving template {} for user {}".format(template, request.user), 'error')
                return JsonResponse({'new_run_dir': new_run_dir, 'error': 'template not saved'})
            return JsonResponse({'new_run_dir': new_run_dir, 'template': 'template saved'})
        else:
            return JsonResponse({'new_run_dir': new_run_dir, 'error': 'template not found'})

#
# Delete a model run
# input: user, the user making the request
#        run_name, the name of the run to be deleted
@login_required
def delete_run(request):
    run_directory = request.POST.get('run_name')
    if not run_directory:
        return HttpResponse(status=400)

    path = os.path.abspath(os.path.dirname(__file__))
    run_directory = path + RUN_SCRIPT_PATH + str(request.user) + '/' + run_directory

    if not os.path.exists(run_directory):
        print_message("Attempt to delete directory that doesnt exist", 'error')
        return HttpResponse(status=400)

    if request.user != run_directory.split('/')[-2]:
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

def view_runs(request):
    return JsonResponse({})


def create_script(request):
    return JsonResponse({})


def update_script(request):
    return JsonResponse({})


def read_script(request):
    return JsonResponse({})


def delete_script(request):
    return JsonResponse({})
