from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import json
import os
from constants import RUN_SCRIPT_PATH
from util.utilities import print_debug
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
        print "[+] Creating directory {}".format(user_directory)
        os.makedirs(user_directory)


    new_run = request.POST.get('run_name')
    if not new_run:
        print '[-] No new run_name specied'
        return HttpResponse(status=400)

    new_run_dir = os.path.join(user_directory, new_run)
    if os.path.exists(new_run_dir):
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
        print "[-] Error saving run {} in database for user {}".format(new_run_dir, request.user)
        shutil.rmtree(new_run_dir, ignore_errors=True)
        print_debug(e)
        return JsonResponse({'error': 'error saving run in database'})

    template = request.POST.get('template')
    if not template:
        print "[+] No template request"
        return JsonResponse({'new_run_dir': new_run_dir})
    else:
        print "[+] got template request: {}".format(template)
        found_template = False
        template_path = False
        template_search_dirs = [str(request.user), 'global']
        template_search_dirs = [ str(template_directory + x) for x in template_search_dirs]
        print "template_search_dirs {}".format(template_search_dirs)
        for directory in template_search_dirs:
            print "[+] testing {}".format(directory)
            if os.path.exists(directory):
                print "[+] folder contents {}".format(os.listdir(directory))
                if template in os.listdir(directory):
                    print "[+] found tempalte at {}".format(directory)
                    found_template = True
                    template_path = directory + '/' + template
            else:
                print "[+] creating new resource folder {}".format(directory)
                os.mkdir(directory)

        if found_template:
            try:
                print "[+] Copying file from {} to {}".format(template_path, template_directory + '/' + str(request.user) + '/'+ template)
                shutil.copyfile(template_path, template_directory + '/' + str(request.user) + '/'+ template)
            except Exception as e:
                print_debug(e)
                print "[-] Error saving template {} for user {}".format(template, request.user)
                return JsonResponse({'new_run_dir': new_run_dir, 'error': 'template not saved'})
            return JsonResponse({'new_run_dir': new_run_dir, 'template': 'template saved'})
        else:
            return JsonResponse({'new_run_dir': new_run_dir, 'error': 'template not found'})

#
#
#
@login_required
def delete_run(request):
    run_directory = request.DELETE.get('run_name')
    if not run_directory:
        return HttpResponse(status=400)

    path = os.path.abspath(os.path.dirname(__file__))
    run_directory = path + RUN_SCRIPT_PATH + str(request.user) + '/' + run_directory

    if not os.path.exists(run_directory):
        print "[-] Attempt to delete directory that doesnt exist"
        return HttpResponse(status=400)

    if request.user != run_directory.split('/')[-2]:
        print "[-] Attempt to delete someone elses run directory"
        return HttpResponse(status=403)

    try:
        shutil.rmtree(run_directory, ignore_errors=True)
    except Exception as e:
        print "[-] Error removing run directory"
        return HttpResponse(status=500)

    if os.path.exists(run_directory):
        print "[-] Failed to remove directory {}".format(run_directory)
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
