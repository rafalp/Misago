from django.utils.translation import get_language

from .momentjs import get_locale_url


def site_address(request):
    if request.is_secure():
        site_protocol = 'https'
        address_template = 'https://%s'
    else:
        site_protocol = 'http'
        address_template = 'http://%s'

    host = request.get_host()

    return {
        'SITE_PROTOCOL': site_protocol,
        'SITE_HOST': host,
        'SITE_ADDRESS': address_template % host,
        'REQUEST_PATH': request.path_info,
    }


def momentjs_locale(request):
    return {
        'MOMENTJS_LOCALE_URL': get_locale_url(get_language()),
    }
