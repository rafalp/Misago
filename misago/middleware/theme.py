from urlparse import urlparse
from django.conf import settings
from django.core.cache import cache
from misago.template.theme import activate_theme

class ThemeMiddleware(object):
    def process_request(self, request):
        if not settings.INSTALLED_THEMES:
            raise ValueError('There are no themes installed!')

        activate_theme(settings.INSTALLED_THEMES[0])

        if settings.MOBILE_SUBDOMAIN and settings.MOBILE_TEMPLATES:
            if settings.MOBILE_SUBDOMAIN == '*':
                activate_theme(settings.MOBILE_TEMPLATES)
            else:
                mobile_domain = '%s.%s/' % (settings.MOBILE_SUBDOMAIN, urlparse(settings.BOARD_ADDRESS).netloc)
                current_domain = '%s.%s/' % (settings.MOBILE_SUBDOMAIN, urlparse(request.META.get('HTTP_HOST')).netloc)
                
                if current_domain == mobile_domain:
                    activate_theme(settings.MOBILE_TEMPLATES)
                    
