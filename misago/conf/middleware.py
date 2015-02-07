from django.core.urlresolvers import reverse
from misago.conf.gateway import settings, db_settings  # noqa


class PreloadConfigMiddleware(object):
    def process_request(self, request):
        request.preloaded_ember_data.update({
            'misagoSettings': db_settings.get_public_settings(),

            'staticUrl': settings.STATIC_URL,
            'mediaUrl': settings.MEDIA_URL,

            'loginRedirectUrl': reverse('misago:index'),
            'loginUrl': reverse('misago:login'),

            'logoutUrl': reverse('misago:logout'),
        })
