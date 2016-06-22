from django.shortcuts import render
from django.conf import settings
import requests


@csrf_exempt  # should probably fix this at some point
@login_required
def vtkweb_launcher(request):
    """Proxy requests to the configured launcher service."""
    try:
        VISUALIZATION_LAUNCHER = settings.VISUALIZATION_LAUNCHER
    except ImportError:
        VISUALIZATION_LAUNCHER = None

    if not VISUALIZATION_LAUNCHER:
        # unconfigured launcher
        return HttpResponse(status=404)

    # TODO: add status and delete methods
    if request.method == 'POST':
        req = requests.post(VISUALIZATION_LAUNCHER, request.body)
        if req.ok:
            return HttpResponse(req.content)
        else:
            return HttpResponse(status=500)

    return HttpResponse(status=404)
