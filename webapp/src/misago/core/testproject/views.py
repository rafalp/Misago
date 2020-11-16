from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from rest_framework.decorators import api_view
from social_core.backends.github import GithubOAuth2
from social_core.exceptions import AuthFailed, NotAllowedToDisconnect, WrongBackend

from .. import errorpages
from ...users.models import Ban
from ..decorators import require_POST
from ..exceptions import Banned, SocialAuthBanned, SocialAuthFailed
from ..shortcuts import paginate, paginated_response, validate_slug
from ..views import home_redirect
from .models import Model
from .serializers import MockSerializer


def test_pagination(request, page=None):
    items = range(15)
    page = paginate(items, page, 5)
    return HttpResponse(",".join([str(x) for x in page.object_list]))


@api_view()
def test_paginated_response(request):
    data = range(100)
    page = paginate(data, 2, 10)

    return paginated_response(page)


@api_view()
def test_paginated_response_data(request):
    data = range(100)
    page = paginate(data, 2, 10)

    return paginated_response(page, data=["a", "b", "c", "d", "e"])


@api_view()
def test_paginated_response_serializer(request):
    data = [0, 1, 2, 3]
    page = paginate(data, 0, 10)

    return paginated_response(page, serializer=MockSerializer)


@api_view()
def test_paginated_response_data_serializer(request):
    data = [0, 1, 2, 3]
    page = paginate(data, 0, 10)

    return paginated_response(
        page, data=["a", "b", "c", "d"], serializer=MockSerializer
    )


@api_view()
def test_paginated_response_data_extra(request):
    data = [0, 1, 2, 3]
    page = paginate(data, 0, 10)

    return paginated_response(
        page, data=["a", "b", "c", "d"], extra={"next": "EXTRA", "lorem": "ipsum"}
    )


def validate_slug_view(request, pk, slug):
    model = Model(int(pk), "eric-the-fish")
    validate_slug(model, slug)
    return HttpResponse("Allright!")


def raise_misago_banned(request):
    ban = Ban(user_message="Banned for test!")
    raise Banned(ban)


def raise_misago_403(request):
    raise PermissionDenied("Misago 403")


def raise_misago_404(request):
    raise Http404("Misago 404")


def raise_misago_405(request):
    return errorpages.not_allowed(request)


def raise_403(request):
    raise PermissionDenied()


def raise_404(request):
    raise Http404()


def raise_social_auth_failed(require_POST):
    raise AuthFailed(GithubOAuth2)


def raise_social_wrong_backend(request):
    raise WrongBackend("facebook")


def raise_social_not_allowed_to_disconnect(request):
    raise NotAllowedToDisconnect()


def raise_social_auth_failed_message(request):
    raise SocialAuthFailed(GithubOAuth2, "This message will be shown to user!")


def raise_social_auth_banned(request):
    ban = Ban(user_message="Banned in auth!")
    raise SocialAuthBanned(GithubOAuth2, ban)


def test_redirect(request):
    return home_redirect(request)


@require_POST
def test_require_post(request):
    return HttpResponse("Request method: %s" % request.method)


@errorpages.shared_403_exception_handler
def mock_custom_403_error_page(request, exception):
    return HttpResponse("Custom 403", status=403)


@errorpages.shared_404_exception_handler
def mock_custom_404_error_page(request, exception):
    return HttpResponse("Custom 404", status=404)
