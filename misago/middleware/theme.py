from django.conf import settings
from django.core.cache import cache
from misago.theme import Theme
from misago.models import ThemeAdjustment

class ThemeMiddleware(object):
    def process_request(self, request):
        if not settings.INSTALLED_THEMES:
            raise ValueError('There are no themes installed!')
        request.theme = Theme(settings.INSTALLED_THEMES[0])
        
        # Adjust theme for specific client?
        if request.META.get('HTTP_USER_AGENT'):
            adjustments = cache.get('client_adjustments', 'nada')
            if adjustments == 'nada':
                adjustments = ThemeAdjustment.objects.all()
                cache.set('client_adjustments', adjustments)
            if adjustments:
                user_agent = request.META.get('HTTP_USER_AGENT').lower()
                for item in adjustments:
                    if item.adjust_theme(user_agent):
                        request.theme = Theme(item.theme)
                        break
            
