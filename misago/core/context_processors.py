from misago.core.embercli import is_ember_cli_request, get_embercli_host


def site_address(request):
    if request.is_secure():
        site_protocol = 'https'
        address_template = 'https://%s'
    else:
        site_protocol = 'http'
        address_template = 'http://%s'

    if is_ember_cli_request(request):
        host = get_embercli_host()
    else:
        host = request.get_host()

    return {
        'SITE_PROTOCOL': site_protocol,
        'SITE_HOST': host,
        'SITE_ADDRESS': address_template % host
    }


def preloaded_ember_data(request):
    return {'preloaded_ember_data': request.preloaded_ember_data}
