from django.shortcuts import render
from django.http import JsonResponse
import json

#
# Creates a new model run configuration
# input: user, the user requesting a new run config folder
#        optional: template, the name of their predefined template
def create_run(request):
    return JsonResponse({})


def view_runs(request):
    return JsonResponse({})


def delete_run(request):
    return JsonResponse({})


def create_script(request):
    return JsonResponse({})


def update_script(request):
    return JsonResponse({})


def read_script(request):
    return JsonResponse({})


def delete_script(request):
    return JsonResponse({})
