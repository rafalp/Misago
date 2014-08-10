from django.utils import timezone

from misago.users.models import Online
from misago.users.online.ranks import clear_ranks_online_cache


def start_tracking(request, user):
    online_tracker = Online.objects.create(
        user=user,
        current_ip=request._misago_real_ip,
        is_visible_on_index=user.rank.is_on_index
    )

    if online_tracker.is_visible_on_index:
        clear_ranks_online_cache()

    request.user.online_tracker = online_tracker
    request._misago_online_tracker = online_tracker


def update_tracker(request, tracker):
    tracker.current_ip = request._misago_real_ip
    tracker.last_click = timezone.now()

    rank_visible_on_index = request.user.rank.is_on_index
    if tracker.is_visible_on_index != rank_visible_on_index:
        tracker.is_visible_on_index = rank_visible_on_index
        tracker.save(update_fields=[
            'last_click', 'current_ip', 'is_visible_on_index'
        ])
        clear_ranks_online_cache()
    else:
        tracker.save(update_fields=['last_click', 'current_ip'])


def stop_tracking(request, tracker):
    user = tracker.user
    user.last_login = tracker.last_click
    user.last_ip = tracker.current_ip
    user.save(update_fields=['last_login', 'last_ip'])

    if tracker.is_visible_on_index:
        clear_ranks_online_cache()

    tracker.delete()
