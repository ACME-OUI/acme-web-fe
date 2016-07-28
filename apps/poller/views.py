from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import JsonResponse
from poller.models import UserRuns
import json
from util.utilities import print_debug, print_message


@csrf_exempt
def update(request):
    if request.method == 'GET':
        try:
            request_type = request.GET.get('request')
            user = request.GET.get('user')
            if not request_type:
                return HttpResponse(status=400)
            # request for all jobs
            if request_type == 'all':
                if user:
                    data = UserRuns.objects.filter(user=user)
                else:
                    data = UserRuns.objects.all()
            # request for the next job in the queue
            elif request_type == 'next':
                try:
                    data = UserRuns.objects.filter(status='new').latest()
                    data.status = 'in_progress'
                    data.save()
                except Exception as e:
                    return JsonResponse({})

                if not data:
                    return JsonResponse({})

                config = json.loads(data.config_options)
                r = {}
                r['job_id'] = data.id
                r['user'] = data.user
                r.update(config)
                return JsonResponse(r, safe=False)
            # request for jobs that match status
            elif request_type in ['new', 'in_progress', 'complete', 'failed']:
                if user:
                    data = UserRuns.objects.filter(status=request_type, user=user)
                else:
                    data = UserRuns.objects.filter(status=request_type)
            # request for a specific job
            elif request_type == 'job':
                job_id = request.GET.get('job_id')  # todo: write tests for this
                if not job_id or not job_id.isdigit():
                    return HttpResponse(status=400)
                try:
                    data = UserRuns.objects.get(id=job_id)
                    config = json.loads(data.config_options)
                    obj = {
                        'job_id': data.id,
                        'user': data.user,
                        'status': data.status,
                    }
                    obj.update(config)
                    return JsonResponse(obj, safe=False)
                except Exception as e:
                    print_debug(e)
                    return JsonResponse({}, status=500)
            else:
                return HttpResponse(status=400)

            if not data:
                print_message('No jobs found', 'ok')
                return JsonResponse({}, status=200)
            obj_list = []
            for obj in data:
                config = json.loads(obj.config_options)
                obj_dict = {}
                obj_dict['job_id'] = obj.id
                obj_dict['user'] = obj.user
                obj_dict['status'] = obj.status
                obj_dict.update(config)
                obj_list.append(obj_dict)
            return JsonResponse(obj_list, safe=False)

        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)

        print_message('unhandled request')
        return HttpResponse(status=400)

    if request.method == 'POST':
        try:
            print_message(request.body)
            data = json.loads(request.body)
            request_type = data.get('request')
            if not request_type:
                print_message('no request type given')
                return HttpResponse(status=404)
            if request_type not in ['new', 'in_progress', 'complete', 'failed', 'all', 'delete', 'stop']:
                print_message('Unrecognized request type')
                return HttpResponse(status=400)

            user = data.get('user')
            status = data.get('status')

            if request_type == 'stop':
                try:
                    job_id = data.get('job_id')
                    job = UserRuns.objects.get(id=job_id)
                    job.status = 'stopped'
                    job.save()
                except Exception as e:
                    print_debug(e)
                    return HttpResponse(status=500)
                return HttpResponse()

            # request to update all of a users jobs to a given status
            if request_type == 'all':
                if status not in ['new', 'in_progress', 'complete', 'failed', 'stop']:
                    return HttpResponse(status=400)
                if user:
                    jobs = UserRuns.objects.filter(user=user)
                    for job in jobs:
                        job.status = status
                        job.save()
                    return HttpResponse(status=200)
                else:
                    jobs = UserRuns.objects.all()
                    for job in jobs:
                        job.status = status
                        job.save()
                    return HttpResponse(status=200)
            # new job request
            if request_type == 'new':
                if not user:
                    return HttpResponse(status=400)
                config = {}
                for key in data:
                    value = data.get(key)
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
                return JsonResponse({'job_id': new_run.id})
            # request to delete a job
            if request_type == 'delete':
                try:
                    job_id = data.get('job_id')
                    if not job_id:
                        return HttpResponse(status=404)

                    UserRuns.objects.get(id=job_id).delete()
                    return HttpResponse(status=200)
                except Exception as e:
                    print_debug(e)
                    return HttpResponse(status=400)

            # request to change the status of an existant job
            if request_type not in ['in_progress', 'complete', 'failed']:
                return HttpResponse(status=400)  # Unrecognized request
            job_id = data.get('id')
            if not job_id:
                return HttpResponse(status=400)
            try:
                job = UserRuns.objects.get(id=job_id)
                job.status = request_type
                output = data.get('output')
                if output:
                    job.output = output
                job.save()
                return HttpResponse(status=200)
            except Exception as e:
                print_debug(e)
                return HttpResponse(status=500)

        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        print_message('Http verb {} is not used'.format(request.method))
        return HttpResponse(status=404)
