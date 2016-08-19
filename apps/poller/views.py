from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import JsonResponse
from poller.models import UserRuns
import json
import os

from util.utilities import print_debug, print_message
from run_manager.constants import DIAG_OUTPUT_PREFIX
from run_manager.dispatcher import group_job_update

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
                data = get_all(user)
            # request for the next job in the queue
            elif request_type == 'next':
                data = get_next()
                return JsonResponse(data, safe=False)
            # request for jobs that match status
            elif request_type in ['new', 'in_progress', 'complete', 'failed']:
                data = get_job_with_status(request_type, user)
            # request for a specific job
            elif request_type == 'job':
                job_id = request.GET.get('job_id')  # todo: write tests for this
                return get_job(job_id)
            else:
                return HttpResponse(status=400)

            return send_data(data)

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
            job_id = data.get('job_id')

            if request_type == 'stop':
                job_id = data.get('job_id')
                return post_stop(job_id)

            # request to update all of a users jobs to a given status
            if request_type == 'all':
                return post_all(user, status)

            # new job request
            if request_type == 'new':
                return post_new(user, data)
            # request to delete a job
            if request_type == 'delete':
                return post_delete(job_id)
            # request to change the status of an existant job
            if request_type not in ['in_progress', 'complete', 'failed']:
                print_message("Unrecognized request type {}".format(request_type))
                return HttpResponse(status=400)  # Unrecognized request

            if not job_id:
                print_message("no job id")
                return HttpResponse(status=400)

            return post_update(job_id, data, request_type)

        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        print_message('Http verb {} is not used'.format(request.method))
        return HttpResponse(status=404)


def post_update(job_id, data, request_type):
    try:
        job = UserRuns.objects.get(id=job_id)
        job.status = request_type
        output = data.get('output')
        # Check if the job finished and has output
        # if it does, write it to the db and an output file
        if output:
            job.output = output
            options = json.loads(job.config_options)
            request_attr = options.get('request_attr')
            outputdir = DIAG_OUTPUT_PREFIX + job.user \
                + '/' + options.get('run_name') + '_' + str(job_id) \
                + request_attr.get('outputdir') \
                + '/' + request_attr.get('diag_type').lower()
            print_message('output dir: {}'.format(outputdir))
            if not os.path.exists(outputdir):
                os.makedirs(outputdir)
            with open(outputdir + '/console_output.txt', 'w+') as output_file:
                output_file.write(' '.join(output))
                output_file.close()
        job.save()
        group_job_update(job_id, job.user, request_type)
        return HttpResponse(status=200)
    except Exception as e:
        print_debug(e)
        return HttpResponse(status=500)

def post_delete(job_id):
    if not job_id:
        return HttpResponse(status=404)
    try:
        job = UserRuns.objects.get(id=job_id)
        group_job_update(job_id, job.user, 'deleted')
        job.delete()
        return HttpResponse(status=200)
    except Exception as e:
        print_debug(e)
        return HttpResponse(status=400)


def post_new(user, data):
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
    print_message('returning job_id: {}'.format(new_run.id))
    response = json.dumps({
        'job_id': new_run.id,
    })
    print_message('returning new job response {}'.format(response))
    res = HttpResponse(response, content_type='application/json')
    group_job_update(new_run.id, new_run.user, 'new')
    return res

def post_all(user, status):
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

def post_stop(job_id):
    try:
        job = UserRuns.objects.get(id=job_id)
        job.status = 'stopped'
        job.save()
    except Exception as e:
        print_debug(e)
        return HttpResponse(status=500)
    group_job_update(job_id, job.user, 'stopped')
    return HttpResponse()

def send_data(data):
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


def get_job(job_id):
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

def get_job_with_status(request_type, user):
    if user:
        data = UserRuns.objects.filter(status=request_type, user=user)
    else:
        data = UserRuns.objects.filter(status=request_type)
    return data


def get_all(user=None):
    if user:
        data = UserRuns.objects.filter(user=user)
    else:
        data = UserRuns.objects.all()
    return data

def get_next():
    try:
        runs = UserRuns.objects.filter(status='new')
        if len(runs) == 0:
            return {}
        data = runs.latest()
        data.status = 'in_progress'
        data.save()
    except Exception as e:
        print_message('Error getting next job from database')
        print_debug(e)
        return {}
    if not data:
        return {}

    config = json.loads(data.config_options)
    r = {}
    r['job_id'] = data.id
    r['user'] = data.user
    r.update(config)
    group_job_update(data.id, data.user, 'in_progress')
    return r
