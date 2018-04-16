from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin

from .bans import get_request_ip_ban, get_user_ban
from .models import AnonymousUser
from .online import tracker


class RealIPMiddleware(MiddlewareMixin):
    def process_request(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            request.user_ip = x_forwarded_for.split(',')[0]
        else:
            request.user_ip = request.META.get('REMOTE_ADDR')


class UserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_anonymous:
            request.user = AnonymousUser()
        elif not request.user.is_staff:
            if get_request_ip_ban(request) or get_user_ban(request.user):
                logout(request)
                request.user = AnonymousUser()


class OnlineTrackerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tracker.start_request_tracker(request)

    def process_response(self, request, response):
        tracker.update_request_tracker(request)
        return response
