from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils import six

from .searchproviders import searchproviders


def search_providers(request):
    allowed_providers = []

    try:
        if request.user.acl_cache['can_search']:
            allowed_providers = searchproviders.get_allowed_providers(request)
    except AttributeError:
        # is user has no acl_cache attribute, cease entire middleware
        # this is edge case that occurs when debug toolbar intercepts
        # the redirect response from logout page and runs context providers
        # with non-misago's anonymous user model that has no acl support
        return {}

    request.frontend_context['search'] = []

    for provider in allowed_providers:
        request.frontend_context['search'].append({
            'id': provider.url,
            'name': six.text_type(provider.name),
            'icon': provider.icon,
            'results': None,
            'time': None,
        })

    return {}
