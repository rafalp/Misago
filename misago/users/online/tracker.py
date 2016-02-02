from django.utils import timezone
from misago.users.models import Online


def mute_tracker(request):
    request._misago_online_tracker = None


def start_tracking(request, user):
    online_tracker = Online.objects.create(
        user=user,
        current_ip=request.user_ip,
        is_visible_on_index=user.rank.is_on_index
    )

    request.user.online_tracker = online_tracker
    request._misago_online_tracker = online_tracker


def update_tracker(request, tracker):
    tracker.current_ip = request.user_ip
    tracker.last_click = timezone.now()

    rank_visible_on_index = request.user.rank.is_on_index
    if tracker.is_visible_on_index != rank_visible_on_index:
        tracker.is_visible_on_index = rank_visible_on_index
        tracker.save(update_fields=[
            'last_click', 'current_ip', 'is_visible_on_index'
        ])
    else:
        tracker.save(update_fields=['last_click', 'current_ip'])


def stop_tracking(request, tracker):
    user = tracker.user
    user.last_login = tracker.last_click
    user.last_ip = tracker.current_ip
    user.save(update_fields=['last_login', 'last_ip'])

    tracker.delete()
