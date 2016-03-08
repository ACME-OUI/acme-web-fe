from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    if request.method == 'GET':
        status = request.GET.get('status')
        if status:
            if status == 'all':
                return HttpResponse('got status: all')
            if status == 'new':
                return HttpResponse('got status: new')
            if status == 'in_progress':
                return HttpResponse('got status: in_progress')
            if status == 'complete':
                return HttpResponse('got status: complete')
            if status == 'failed':
                return HttpResponse('got status: failed')
            
        return HttpResponse("Hello, world. You're at the polls index.")

    if request.method == 'POST':
        return HttpResponse("Hello, world. You posted to the polls index.")