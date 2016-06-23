from django.shortcuts import render
from django.conf import settings
import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


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


def _refresh(request):
    """Refresh the visualization session information."""
    # check the session for a vtkweb instance
    vis = request.session.get('vtkweb')
    if vis is None or vtk_launcher.status(vis.get('id', '')) is None:
        # open a visualization instance
        vis = vtk_launcher.new_instance()
        request.session['vtkweb'] = vis
    return dict(vis)


def vtk_viewer(request):
    """Open the main visualizer view."""
    data = {}
    data['base'] = base_path
    data['files'] = [
            f for f in os.listdir(base_path)
            if not os.path.isdir(os.path.join(base_path, f))
            ]
    data['dirs'] = [
            f for f in os.listdir(base_path)
            if os.path.isdir(os.path.join(base_path, f))
            ]
    return render(
            request,
            'vtk_view/cdat_viewer.html',
            data
            )


def vtk_test(request, test="cone"):
    return render(request, 'vtk_view/view_test.html', {"test": test})
