from django.http import HttpResponse
from django.http import JsonResponse
from poller.models import UserRuns
import json


def index(request):
    if request.method == 'GET':
        try:
            status = request.GET.get('status')
            user = request.GET.get('user')
            if status:
                if status == 'all':
                    data = UserRuns.objects.all()
                elif status == 'new':
                    data = UserRuns.objects.filter(status='new')
                elif status == 'in_progress':
                    data = UserRuns.objects.filter(status='in_progress')
                elif status == 'complete':
                    data = UserRuns.objects.filter(status='complete')
                elif status == 'failed':
                    data = UserRuns.objects.filter(status='failed')
                else:
                    print "got here"
                    return HttpResponse(status=404)
                obj_list = []
                for obj in data:
                    obj_dict = {}
                    obj_dict['runspec'] = obj.runspec
                    obj_list.append(obj_dict)
                return JsonResponse(obj_list, safe=False)
        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_run = UserRuns.objects.create(user=data['user'], runspec=data['runspec'], status='new')
            new_run.save
            return HttpResponse("Successfully posted ")
        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
