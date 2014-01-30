from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from misago.core import errorpages


def raise_misago_403(request):
    raise PermissionDenied('Misago 403')


def raise_misago_404(request):
    raise Http404('Misago 404')


def raise_403(request):
    raise PermissionDenied()


def raise_404(request):
    raise Http404()


@errorpages.shared_403_exception_handler
def mock_custom_403_error_page(request):
    return HttpResponse("Custom 403", status=403)


@errorpages.shared_404_exception_handler
def mock_custom_404_error_page(request):
    return HttpResponse("Custom 404", status=404)
