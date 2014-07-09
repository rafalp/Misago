from hashlib import md5

from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from misago.conf import settings
from misago.core.cache import cache
from misago.markup import common_flavour


def get_parsed_content(setting_name):
    cache_name = 'misago_legal_%s' % setting_name
    cached_content = cache.get(cache_name)

    unparsed_content = settings.get_lazy_setting(setting_name)

    checksum_source = '%s:%s' % (unparsed_content, settings.SECRET_KEY)
    unparsed_checksum = md5(checksum_source).hexdigest()

    if cached_content and cached_content.get('checksum') == unparsed_checksum:
        return cached_content['parsed']
    else:
        cached_content = {
            'checksum': unparsed_checksum,
            'parsed': common_flavour(unparsed_content)['parsed_text'],
        }
        cache.set(cache_name, cached_content)
        return cached_content['parsed']


def terms(request):
    if not (settings.terms_of_service or settings.terms_of_service_link):
        raise Http404()

    if settings.terms_of_service_link:
        return redirect(settings.terms_of_service_link)

    parsed_content = get_parsed_content('terms_of_service')
    return render(request, 'misago/legal/terms_of_service.html', {
        'title': settings.terms_of_service_title or _("Terms of service"),
        'content': parsed_content,
    })


def privacy_policy(request):
    if not (settings.privacy_policy or settings.privacy_policy_link):
        raise Http404()

    if settings.privacy_policy_link:
        return redirect(settings.privacy_policy_link)

    parsed_content = get_parsed_content('privacy_policy')
    return render(request, 'misago/legal/privacy_policy.html', {
        'title': settings.privacy_policy_title or _("Privacy policy"),
        'content': parsed_content,
    })
