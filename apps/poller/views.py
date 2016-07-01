from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import JsonResponse
from poller.models import UserRuns
import json

@csrf_exempt
def update(request):
    if request.method == 'GET':
        try:
            request_type = request.GET.get('request')
            user = request.GET.get('user')
            if request_type:
                if request_type == 'all':
                    if user:
                        data = UserRuns.objects.filter(user=user)
                    else:
                        data = UserRuns.objects.all()
                elif request_type == 'next':
                    data = UserRuns.objects.filter(status='new').order_by('created')
                    if not data:
                        return JsonResponse({}, safe=False)
                    else:
                        data = data[0]
                        config = json.loads(data.config_options)
                        r = {}
                        r['id'] = data.id
                        r['user'] = data.user
                        r.update(config)
                        return JsonResponse(r, safe=False)
                elif request_type in ['new', 'in_progress', 'complete', 'failed']:
                    if user:
                        data = UserRuns.objects.filter(status=request_type, user=user)
                    else:
                        data = UserRuns.objects.filter(status=request_type)
                elif request_type == 'job':
                    job_id = request.GET.get('job_id')  # todo: write tests for this
                    if job_id and job_id.isdigit():
                        try:
                            data = UserRuns.objects.get(id=job_id)
                            config = json.loads(data.config_options)
                            obj = {
                                'id': data.id,
                                'user': data.user,
                                'status': data.status,
                            }
                            obj.update(config)
                            return JsonResponse(obj, safe=False)
                        except UserRuns.DoesNotExist:
                            return JsonResponse({}, status=200)
                    else:
                        return HttpResponse(status=400)
                else:
                    return HttpResponse(status=400)
                if not data:
                    return JsonResponse({}, status=200)
                obj_list = []
                for obj in data:
                    config = json.loads(obj.config_options)
                    obj_dict = {}
                    obj_dict['id'] = obj.id
                    obj_dict['user'] = obj.user
                    obj_dict['status'] = obj.status
                    obj_dict.update(config)
                    obj_list.append(obj_dict)
                return JsonResponse(obj_list, safe=False)
            else:
                return HttpResponse(status=400)
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
                if user:
                    config = {}
                    for key in request.POST:
                        value = request.POST.get(key)
                        config.update({key: value})
                    del config['user']
                    del config['request']
                    config = json.dumps(config)
                    new_run = UserRuns.objects.create(
                        status='new',
                        config_options=config,
                        user=user
                    )
                    new_run.save()
                    return JsonResponse({'id': new_run.id})
                else:
                    return HttpResponse(status=400)
            if request_type == 'delete':
                try:
                    job_id = request.POST.get('job_id')
                    if not job_id:
                        raise KeyError
                    else:
                        UserRuns.objects.get(id=job_id).delete()
                        return HttpResponse(status=200)
                except (KeyError, AttributeError, UserRuns.DoesNotExist):
                    return HttpResponse(status=400)
            if request_type in ['in_progress', 'complete', 'failed']:
                job_id = request.POST.get('job_id')
                if job_id.isdigit():
                    try:
                        job = UserRuns.objects.get(id=job_id)
                        job.status = request_type
                        job.save()
                        return HttpResponse(status=200)
                    except ObjectDoesNotExist:
                        return HttpResponse(status=400)
            else:
                return HttpResponse(status=400)  # Unrecognized request
        except Exception as e:
            print e
            return HttpResponse(status=500)
