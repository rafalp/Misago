from rest_framework.request import Request

from django.utils import timezone

from misago.users.models import Online


def unwrap_drf_request(f):
    """utility decorator that unwraps django request from rest frameworks wrapper"""
    def unwrapped_request_view(request, *args, **kwargs):
        if isinstance(request, Request):
            request = request._request
        return f(request, *args, **kwargs)
    return unwrapped_request_view


@unwrap_drf_request
def start_request_tracker(request):
    if request.user.is_authenticated:
        try:
            request._misago_online_tracker = request.user.online_tracker
        except Online.DoesNotExist:
            start_tracking(request, request.user)
    else:
        request._misago_online_tracker = None
    

@unwrap_drf_request
def update_request_tracker(request):
    try:
        online_tracker = request._misago_online_tracker
    except AttributeError:
        return

    if online_tracker:
        if request.user.is_anonymous:
            stop_tracking(request, online_tracker)
        else:
            update_tracking(request, online_tracker)


@unwrap_drf_request
def clear_request_tracker(request):
    request._misago_online_tracker = None


def start_tracking(request, user):
    online_tracker = Online.objects.create(
        user=user,
        current_ip=request.user_ip,
    )

    request.user.online_tracker = online_tracker
    request._misago_online_tracker = online_tracker


def update_tracking(request, online_tracker):
    online_tracker.current_ip = request.user_ip
    online_tracker.last_click = timezone.now()

    online_tracker.save(update_fields=['last_click', 'current_ip'])


def stop_tracking(request, online_tracker):
    user = online_tracker.user
    user.last_login = online_tracker.last_click
    user.last_ip = online_tracker.current_ip
    user.save(update_fields=['last_login', 'last_ip'])

    online_tracker.delete()
