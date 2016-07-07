from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import json
import os
from constants import RUN_SCRIPT_PATH
from util.utilities import print_debug
import shutil


#
# Creates a new model run configuration
# input: user, the user requesting a new run config folder
#        run_name, the name of the new run config
#        optional: template, the name of their predefined template
@login_required
def create_run(request):
    user_directory = os.path.join(str(os.getcwd()), RUN_SCRIPT_PATH, str(request.user))
    user_directory = '/Users/baldwin32/projects/acme-web-fe/run_manager/run_scripts/test'
    print "[+] in dir %s" % os.getcwd()
    print "[+] attempting to create %s" % user_directory
    if not os.path.exists(user_directory):
        print "[+] Creating directory %s" %  user_directory
        os.makedirs(user_directory)


    new_run = request.GET.get('run_name')
    if not new_run:
        return HttpResponse(status=400)

    new_run_dir = os.path.join(user_directory, new_run)
    if os.path.exists(new_run_dir):
        return HttpResponse(status=409)

    try:
        os.makedirs(new_run_dir)
    except Exception as e:
        print_debug(e)
        return HttpResponse(status=500)

    return JsonResponse({'new_run_dir': new_run_dir})


@login_required
def delete_run(request):
    run_directory = request.DELETE.get('run_name')
    run_directory = user_directory = os.path.join(str(os.getcwd()), RUN_SCRIPT_PATH, run_directory)
    run_directory = '/Users/baldwin32/projects/acme-web-fe/run_scripts/test/test_run'
    if not os.path.exists(run_directory):
        print "[-] Attempt to delete directory that doesnt exist"
        return HttpResponse(status=400)

    if request.user != run_directory.split('/')[-2]:
        print "[-] Attempt to delete someone elses run directory"
        return HttpResponse(status=403)

    shutil.rmtree(run_directory, ignore_errors=True)
    if os.path.exists(run_directory):
        print "[-] Failed to remove directory %s" % run_directory
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
