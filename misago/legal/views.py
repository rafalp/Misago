from hashlib import md5

from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.encoding import force_bytes
from django.utils.translation import ugettext as _

from misago.conf import settings
from misago.core.cache import cache
from misago.markup import common_flavour


def get_parsed_content(request, setting_name):
    cache_name = 'misago_legal_%s' % setting_name
    cached_content = cache.get(cache_name)

    unparsed_content = settings.get_lazy_setting(setting_name)

    checksum_source = force_bytes('%s:%s' % (unparsed_content, settings.SECRET_KEY))
    unparsed_checksum = md5(checksum_source).hexdigest()

    if cached_content and cached_content.get('checksum') == unparsed_checksum:
        return cached_content['parsed']
    else:
        parsed = common_flavour(request, None, unparsed_content)['parsed_text']
        cached_content = {
            'checksum': unparsed_checksum,
            'parsed': parsed,
        }
        cache.set(cache_name, cached_content)
        return cached_content['parsed']


def privacy_policy(request):
    if not (settings.privacy_policy or settings.privacy_policy_link):
        raise Http404()

    if settings.privacy_policy_link:
        return redirect(settings.privacy_policy_link)

    parsed_content = get_parsed_content(request, 'privacy_policy')

    return render(
        request, 'misago/privacy_policy.html', {
            'id': 'privacy-policy',
            'title': settings.privacy_policy_title or _("Privacy policy"),
            'link': settings.privacy_policy_link,
            'body': parsed_content,
        }
    )


def terms_of_service(request):
    if not (settings.terms_of_service or settings.terms_of_service_link):
        raise Http404()

    if settings.terms_of_service_link:
        return redirect(settings.terms_of_service_link)

    parsed_content = get_parsed_content(request, 'terms_of_service')

    return render(
        request, 'misago/terms_of_service.html', {
            'id': 'terms-of-service',
            'title': settings.terms_of_service_title or _("Terms of service"),
            'link': settings.terms_of_service_link,
            'body': parsed_content,
        }
    )
