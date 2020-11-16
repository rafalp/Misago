from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from .searchproviders import searchproviders


def landing(request):
    allowed_providers = searchproviders.get_allowed_providers(request)
    if not request.user_acl["can_search"] or not allowed_providers:
        raise PermissionDenied(_("You don't have permission to search site."))

    default_provider = allowed_providers[0]
    return redirect("misago:search", search_provider=default_provider.url)


def search(request, search_provider):
    all_providers = searchproviders.get_providers(request)
    if not request.user_acl["can_search"] or not all_providers:
        raise PermissionDenied(_("You don't have permission to search site."))

    for provider in all_providers:
        if provider.url == search_provider:
            provider.allow_search()
            break
    else:
        raise Http404()

    if "q" in request.GET:
        request.frontend_context["SEARCH_QUERY"] = request.GET.get("q")

    return render(request, "misago/search.html")
