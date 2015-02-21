from django.conf import settings
from misago.core.embercli import is_ember_cli_request


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
        if (is_ember_cli_request(request) and
                response.status_code in (301, 302)):
            return self.rewrite_http_redirect_url(response)

        return response


    def rewrite_http_redirect_url(self, response):
        final_location = settings.MISAGO_EMBER_CLI_ORIGIN, response['location']
        response['location'] = ''.join(final_location)
        return response
