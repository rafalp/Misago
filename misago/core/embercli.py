from django.conf import settings


def is_ember_cli_request(request):
    if settings.DEBUG and settings.MISAGO_EMBER_CLI_ORIGIN:
        http_origin = request.META.get('HTTP_ORIGIN', '')
        return http_origin.startswith(settings.MISAGO_EMBER_CLI_ORIGIN)
    else:
        return False
