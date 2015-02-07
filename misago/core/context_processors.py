from django.conf import settings


def site_address(request):
    if request.is_secure():
        site_protocol = 'https'
        address_template = 'https://%s'
    else:
        site_protocol = 'http'
        address_template = 'http://%s'

    return {
        'SITE_PROTOCOL': site_protocol,
        'SITE_HOST': request.get_host(),
        'SITE_ADDRESS': address_template % request.get_host()
    }


def preloaded_ember_data(request):
    return {'preloaded_ember_data': request.preloaded_ember_data}
