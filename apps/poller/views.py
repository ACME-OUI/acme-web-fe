from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from poller.models import UserRuns
import json
import pdb

@csrf_exempt
def update(request):
    if request.method == 'GET':
        try:
            request_type = request.GET.get('request')
            user = request.GET.get('user')
            if request_type:
                if request_type == 'all':
                    if user:
                        db_objs = UserRuns.objects.filter(user=user)
                    else:
                        db_objs = UserRuns.objects.all()
                    data = []
                    for entry in db_objs:
                        data.append({
                            'id': entry.id,
                            'config_options': entry.config_options,
                            'user': entry.user,
                            'status': entry.status,
                        })
                    return JsonResponse(data, safe=False)
                elif request_type == 'next':
                    data = UserRuns.objects.filter(status='new').order_by('created')
                    if not data:
                        return JsonResponse({}, safe=False)
                    else:
                        data = data[0]
                        r = {}
                        r['id'] = data.id
                        r['user'] = data.user
                        r['config_options'] = data.config_options
                        return JsonResponse(r, safe=False)
                elif request_type == 'new':
                    if user:
                        data = UserRuns.objects.filter(status='new', user=user)
                    else:
                        data = UserRuns.objects.filter(status='new')
                elif request_type == 'in_progress':
                    if user:
                        data = UserRuns.objects.filter(status='in_progress', user=user)
                    else:
                        data = UserRuns.objects.filter(status='in_progress')
                elif request_type == 'complete':
                    if user:
                        data = UserRuns.objects.filter(status='complete', user=user)
                    else:
                        data = UserRuns.objects.filter(status='complete')
                elif request_type == 'failed':
                    if user:
                        data = UserRuns.objects.filter(status='failed', user=user)
                    else:
                        data = UserRuns.objects.filter(status='failed')
                elif request_type == 'job':
                    job_id = request.GET.get('job_id')
                    if job_id:
                        try:
                            data = UserRuns.objects.get(id=job_id)
                        except Exception as e:
                            print e
                            print 'job_id: ', job_id
                            return HttpResponse(status=400)  # Currently throws 400 on bad id. Might want empty object instead
                    else:
                        return HttpResponse(status=400)
                else:
                    print "Invalid request recieved"
                    return HttpResponse(status=400)
                obj_list = []
                for obj in data:
                    obj_dict = {}
                    obj_dict['id'] = obj.id
                    obj_dict['user'] = obj.user
                    obj_dict['config_options'] = obj.config_options
                    obj_list.append(obj_dict)
                return JsonResponse(obj_list, safe=False)
            else:
                return HttpResponse(render(request, "poller/token.html", {}))
        except Exception as e:
            print e
            return HttpResponse(status=500)

    if request.method == 'POST':
        try:
            request_type = request.POST.get('request')
            user = request.POST.get('user')
            status = request.POST.get('status')
            if request_type == 'all':
                if user:
                    if status in ['new', 'in_progress', 'complete', 'failed']:
                        jobs = UserRuns.objects.filter(user=user)
                        for job in jobs:
                            job.status = status
                            job.save()
                        return HttpResponse(status=200)
                else:
                    if status in ['new', 'in_progress', 'complete', 'failed']:
                        jobs = UserRuns.objects.all()
                        for job in jobs:
                            job.status = status
                            job.save()
                        return HttpResponse(status=200)
                return HttpResponse(status=400)  # If request was 'all' and we get to here, the request was bad
            if request_type == 'new':
                data = json.loads(request.body)
                if 'user' and 'config_options' in data:
                    user = data['user']
                    del data['user']
                    new_run = UserRuns.objects.create(
                        status='new',
                        config_options=data['config_options'],
                        user=user
                    )
                    new_run.save()
                    return JsonResponse({'id': new_run.id})  # TODO: write tests for this
                else:
                    return HttpResponse(status=400)
        except Exception as e:
            print e
            pdb.set_trace()
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
            try:
                data = json.loads(request.body)
                if 'user' and 'config_options' in data:
                    new_run = UserRuns.objects.create(
                        status='new',
                        user=data['user'],
                        config_options = data['config_options'],
                    )
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
