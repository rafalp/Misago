from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import six
from django.utils.translation import ugettext as _

from .searchproviders import searchproviders


def landing(request):
    allowed_providers = searchproviders.get_allowed_providers(request)
    if not request.user.acl['can_search'] or not allowed_providers:
        raise PermissionDenied(_("You don't have permission to search site."))

    default_provider = allowed_providers[0]
    return redirect('misago:search', search_provider=default_provider.url)


def search(request, search_provider):
    if not request.user.acl['can_search']:
        raise PermissionDenied(_("You don't have permission to search site."))

    for provider in searchproviders.get_providers(request):
        if provider.url == search_provider:
            provider.allow_search()
            break
    else:
        raise Http404()

    request.frontend_context['SEARCH_PROVIDERS'] = []
    for provider in searchproviders.get_allowed_providers(request):
        request.frontend_context['SEARCH_PROVIDERS'].append({
            'name': six.text_type(provider.name),
            'url': reverse('misago:search', kwargs={'search_provider': provider.url}),
            'api': provider.url,
            'results': None
        })

    return render(request, 'misago/search.html')
