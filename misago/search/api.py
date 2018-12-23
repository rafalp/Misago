from time import time

from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..core.shortcuts import get_int_or_404
from .searchproviders import searchproviders


@api_view()
def search(request, search_provider=None):
    allowed_providers = searchproviders.get_allowed_providers(request)
    if not request.user_acl["can_search"] or not allowed_providers:
        raise PermissionDenied(_("You don't have permission to search site."))

    search_query = get_search_query(request)
    response = []
    for provider in allowed_providers:
        provider_data = {
            "id": provider.url,
            "name": str(provider.name),
            "icon": provider.icon,
            "url": reverse("misago:search", kwargs={"search_provider": provider.url}),
            "api": reverse(
                "misago:api:search", kwargs={"search_provider": provider.url}
            ),
            "results": None,
            "time": None,
        }

        if not search_provider or search_provider == provider.url:
            start_time = time()

            if search_provider == provider.url:
                page = get_int_or_404(request.query_params.get("page", 1))
            else:
                page = 1

            provider_data["results"] = provider.search(search_query, page)
            provider_data["time"] = float("%.2f" % (time() - start_time))

        response.append(provider_data)
    return Response(response)


def get_search_query(request):
    return request.query_params.get("q", "").strip()
