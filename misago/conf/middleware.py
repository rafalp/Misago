from django.core.urlresolvers import reverse
from misago.conf.gateway import settings, db_settings  # noqa


class PreloadConfigMiddleware(object):
    def process_request(self, request):
        preloaded_settings = db_settings.get_public_settings()
        preloaded_settings.update({
            'loginApiUrl': settings.MISAGO_LOGIN_API_URL,

            'loginRedirectUrl': reverse(settings.LOGIN_REDIRECT_URL),
            'loginUrl': reverse(settings.LOGIN_URL),

            'logoutUrl': reverse(settings.LOGOUT_URL),
        })

        request.preloaded_ember_data.update({
            'misagoSettings': preloaded_settings,

            'staticUrl': settings.STATIC_URL,
            'mediaUrl': settings.MEDIA_URL,

            'csrfCookieName': settings.CSRF_COOKIE_NAME,
        })
