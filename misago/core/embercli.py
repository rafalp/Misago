from django.conf import settings
from django.utils.six.moves.urllib.parse import urlparse


def is_ember_cli_request(request):
    if settings.DEBUG and settings.MISAGO_EMBER_CLI_ORIGIN:
        http_origin = request.META.get('HTTP_ORIGIN', '')
        return http_origin.startswith(settings.MISAGO_EMBER_CLI_ORIGIN)
    else:
        return False


def get_embercli_host():
    if settings.MISAGO_EMBER_CLI_ORIGIN:
        parsed_url = urlparse(settings.MISAGO_EMBER_CLI_ORIGIN)
        return '%s:%s' % (parsed_url.hostname, parsed_url.port)
    else:
        return None
