from django.shortcuts import render
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.template import Template
from django.http import HttpResponse
from django.http import JsonResponse
from poller.models import UserRuns
from django.conf import settings
import json
import pdb


def index(request):
    if request.method == 'GET':
        try:
            status = request.GET.get('status')
            user = request.GET.get('user')
            if status:
                if status == 'all':
                    data = UserRuns.objects.all()
                elif status == 'next':
                    data = UserRuns.objects.filter(status='new').order_by('created')
                    if not data:
                        return JsonResponse({}, safe=False)
                    else:
                        data = data[0]
                        r = {}
                        r['runspec'] = data.runspec
                        r['id'] = data.id
                        r['user'] = data.user
                        r['destination'] = data.destination
                        r['casename'] = data.casename
                        r['mppwidth'] = data.mppwidth
                        r['stop_option'] = data.stop_option
                        r['stop_n'] = data.stop_n
                        r['walltime'] = data.walltime
                        r['mach'] = data.mach
                        r['compset'] = data.compset
                        r['res'] = data.res
                        r['project'] = data.project
                        r['compiler'] = data.compiler
                        return JsonResponse(r, safe=False)
                elif status == 'new':
                    data = UserRuns.objects.filter(status='new')
                elif status == 'in_progress':
                    data = UserRuns.objects.filter(status='in_progress')
                elif status == 'complete':
                    data = UserRuns.objects.filter(status='complete')
                elif status == 'failed':
                    data = UserRuns.objects.filter(status='failed')
                else:
                    print "Invalid status recieved"
                    return HttpResponse(status=404)
                obj_list = []
                # if data is empty:
                for obj in data:
                    obj_dict = {}
                    obj_dict['runspec'] = obj.runspec
                    obj_dict['id'] = obj.id
                    obj_dict['user'] = obj.user
                    obj_dict['destination'] = obj.destination
                    obj_dict['casename'] = obj.casename
                    obj_dict['mppwidth'] = obj.mppwidth
                    obj_dict['stop_option'] = obj.stop_option
                    obj_dict['stop_n'] = obj.stop_n
                    obj_dict['walltime'] = obj.walltime
                    obj_dict['mach'] = obj.mach
                    obj_dict['compset'] = obj.compset
                    obj_dict['res'] = obj.res
                    obj_dict['project'] = obj.project
                    obj_dict['compiler'] = obj.compiler
                    obj_list.append(obj_dict)
                return JsonResponse(obj_list, safe=False)
            else:
                return HttpResponse(render(request, "poller/token.html", {}))
        except Exception as e:
            print e
            return HttpResponse(status=500)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if 'user' and 'runspec' in data:
                new_run = UserRuns.objects.create(
                    status='new',
                    user=data['user'],
                    runspec=data['runspec'],
                    destination=data['destination'],
                    casename=data['casename'],
                    mppwidth=data['mppwidth'],
                    stop_option=data['stop_option'],
                    stop_n=data['stop_n'],
                    walltime=data['walltime'],
                    mach=data['mach'],
                    compset=data['compset'],
                    res=data['res'],
                    project=data['project'],
                    compiler=data['compiler'])
                new_run.save()
                return HttpResponse("Successfully updated status")
            else:
                return HttpResponse(status=400)
        except Exception as e:
            print e
            return HttpResponse(status=500)

    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            if str(data['id']).isdigit() and data['status'] in ['new', 'in_progress', 'complete', 'failed']:
                db_id = data['id']
                newstatus = data['status']
                try:
                    entry = UserRuns.objects.get(id=db_id)
                    entry.status = newstatus
                    entry.save()
                except Exception as e:
                    print e
                    return HttpResponse(status=500)
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        except KeyError as e:
            print e
            return HttpResponse(status=400)
        except Exception as e:
            print e
            return HttpResponse(status=500)

    if request.method == 'PUT':
        # if settings.DEBUG == True
            try:
                data = json.loads(request.body)
                if 'user' and 'runspec' in data:
                    new_run = UserRuns.objects.create(
                        status='new', user=data['user'],
                        runspec=data['runspec'],
                        destination=data['destination'],
                        casename=data['casename'],
                        mppwidth=data['mppwidth'],
                        stop_option=data['stop_option'],
                        stop_n=data['stop_n'],
                        walltime=data['walltime'],
                        mach=data['mach'],
                        compset=data['compset'],
                        res=data['res'],
                        project=data['project'],
                        compiler=data['compiler'])
                    new_run.save()
                    # Success
                    return HttpResponse(status=200)
                else:
                    # Request must have both user and runspec
                    return HttpResponse(status=400)
            except Exception as e:
                print e
                return HttpResponse(status=500)
        # else:
        #     JsonResponse(status=404)

    if request.method == 'DELETE':
        # if settings.DEBUG == True
            try:
                data = json.loads(request.body)
                if 'id' in data:
                    UserRuns.objects.get(id=data['id']).delete()
                else:
                    return HttpResponse(status=400)
            except Exception as e:
                print e
                return HttpResponse(status=500)
        # else:
        #     JsonResponse(status=404)
