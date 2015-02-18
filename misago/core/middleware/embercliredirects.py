from django.conf import settings


class EmberCLIRedirectsMiddleware(object):
    """
    Utility middleware for development

    Redirects returned by Django point to dev server's port,
    thus pulling us out from Ember's dev server.

    This middleware detects requests coming from Ember and makes redirects
    point back to it instead.

    This middleware works only in DEBUG and requires browser to send Origin
    header that matches one in MISAGO_EMBER_CLI_ORIGIN setting.
    """
    def process_response(self, request, response):
        if settings.DEBUG and settings.MISAGO_EMBER_CLI_ORIGIN:
            rewrite_ember_cli_redirect_url = (
                response.status_code in (301, 302)
                and request.META.get('HTTP_ORIGIN')
                and self.is_ember_cli_request(request)
            )

            if rewrite_ember_cli_redirect_url:
                return self.rewrite_http_redirect_url(response)

        return response

    def is_ember_cli_request(self, request):
        http_origin = request.META.get('HTTP_ORIGIN', '')
        return http_origin.endswith(settings.MISAGO_EMBER_CLI_ORIGIN)

    def rewrite_http_redirect_url(self, response):
        final_location = settings.MISAGO_EMBER_CLI_ORIGIN, response['location']
        response['location'] = ''.join(final_location)
        return response
