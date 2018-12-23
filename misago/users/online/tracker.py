from django.utils import timezone
from rest_framework.request import Request

from ..models import Online


def mute_tracker(request):
    request._misago_online_tracker = None


def start_tracking(request, user):
    online_tracker = Online.objects.create(user=user)

    request.user.online_tracker = online_tracker
    request._misago_online_tracker = online_tracker


def update_tracker(request, tracker):
    tracker.last_click = timezone.now()

    tracker.save(update_fields=["last_click"])


def stop_tracking(request, tracker):
    user = tracker.user
    user.last_login = tracker.last_click
    user.save(update_fields=["last_login"])

    tracker.delete()


def clear_tracking(request):
    if isinstance(request, Request):
        request = request._request  # Fugly unwrap restframework's request
    request._misago_online_tracker = None
