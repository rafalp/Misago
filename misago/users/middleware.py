from django.utils import timezone
from misago.users.models import AnonymousUser, Online


class UserMiddleware(object):
    def process_request(self, request):
        if request.user.is_anonymous():
            request.user = AnonymousUser()


class OnlineTrackerMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            try:
                request._misago_online_tracker = request.user.online_tracker
            except Online.DoesNotExist:
                online_tracker = Online.objects.create(user=request.user)
                request.user.online_tracker = online_tracker
                request._misago_online_tracker = online_tracker
        else:
            request._misago_online_tracker = None

    def process_response(self, request, response):
        if hasattr(request, '_misago_online_tracker'):
            tracker = request._misago_online_tracker

            if tracker:
                if request.user.is_anonymous():
                    # User logged off, update his last visit and blam tracker
                    user = tracker.user
                    user.last_active = tracker.last_click
                    user.save(update_fields=['last_active'])
                else:
                    # Bump user's tracker time
                    tracker.last_click = timezone.now()
                    tracker.save(update_fields=['last_click'])

        return response
