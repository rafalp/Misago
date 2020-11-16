from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin

from .bans import get_request_ip_ban, get_user_ban
from .models import AnonymousUser, Online
from .online import tracker


class RealIPMiddleware(MiddlewareMixin):
    def process_request(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            request.user_ip = x_forwarded_for.split(",")[0]
        else:
            request.user_ip = request.META.get("REMOTE_ADDR")


class UserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_anonymous:
            request.user = AnonymousUser()
        elif not request.user.is_staff:
            if get_request_ip_ban(request) or get_user_ban(
                request.user, request.cache_versions
            ):
                logout(request)
                request.user = AnonymousUser()


class OnlineTrackerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                request._misago_online_tracker = request.user.online_tracker
            except Online.DoesNotExist:
                tracker.start_tracking(request, request.user)
        else:
            request._misago_online_tracker = None

    def process_response(self, request, response):
        if hasattr(request, "_misago_online_tracker"):
            online_tracker = request._misago_online_tracker

            if online_tracker:
                if request.user.is_anonymous:
                    tracker.stop_tracking(request, online_tracker)
                else:
                    tracker.update_tracker(request, online_tracker)

        return response
