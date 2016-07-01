from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import JsonResponse
from poller.models import UserRuns

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
                    job_id = request.GET.get('job_id')  # todo: write tests for this
                    if job_id and job_id.isdigit():
                        try:
                            data = UserRuns.objects.get(id=job_id)
                            obj = {
                                'id': data.id,
                                'user': data.user,
                                'status': data.status,
                                'config_options': data.config_options
                            }
                            return JsonResponse(obj, safe=False)
                        except Exception as e:
                            print e
                            print 'job_id: ', job_id
                            return HttpResponse(status=400)  # Currently throws 400 on bad id. Might want empty object instead
                    else:
                        return HttpResponse(status=400)
                else:
                    return HttpResponse(status=400)
                obj_list = []

                for obj in data:
                    obj_dict = {}
                    obj_dict['id'] = obj.id
                    obj_dict['user'] = obj.user
                    obj_dict['status'] = obj.status
                    obj_dict['config_options'] = obj.config_options
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
                config_options = request.POST.get('config_options')
                if 'user' and 'config_options':
                    new_run = UserRuns.objects.create(
                        status='new',
                        config_options=config_options,
                        user=user
                    )
                    new_run.save()
                    return JsonResponse({'id': new_run.id})  # TODO: write tests for this
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
