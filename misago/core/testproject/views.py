from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse

from misago.core import errorpages, mail
from misago.core.decorators import require_POST
from misago.core.shortcuts import paginate, validate_slug
from misago.core.testproject.models import Model
from misago.core.views import noscript


def test_mail_user(request):
    User = get_user_model()

    test_user = User.objects.all().first()
    mail.mail_user(request,
                   test_user,
                   "Misago Test Mail",
                   "misago/emails/base")

    return HttpResponse("Mailed user!")


def test_mail_users(request):
    User = get_user_model()

    mail.mail_users(request,
                    User.objects.iterator(),
                    "Misago Test Spam",
                    "misago/emails/base")

    return HttpResponse("Mailed users!")


def test_pagination(request, page=None):
    items = range(15)
    page = paginate(items, page, 5)
    return HttpResponse(",".join([str(x) for x in page.object_list]))


def validate_slug_view(request, model_id, model_slug):
    model = Model(int(model_id), 'eric-the-fish')
    validate_slug(model, model_slug)
    return HttpResponse("Allright!")


def raise_misago_403(request):
    raise PermissionDenied('Misago 403')


def raise_misago_404(request):
    raise Http404('Misago 404')


def raise_misago_405(request):
    return errorpages.not_allowed(request)


def raise_403(request):
    raise PermissionDenied()


def raise_404(request):
    raise Http404()


def test_noscript(request):
    return noscript(request, **request.POST)


@require_POST
def test_require_post(request):
    return HttpResponse("Request method: %s" % request.method)


@errorpages.shared_403_exception_handler
def mock_custom_403_error_page(request):
    return HttpResponse("Custom 403", status=403)


@errorpages.shared_404_exception_handler
def mock_custom_404_error_page(request):
    return HttpResponse("Custom 404", status=404)
