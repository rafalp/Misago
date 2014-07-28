from datetime import timedelta

from django.utils import timezone

from misago.users.bans import get_user_ban
from misago.users.models import Online


ACTIVITY_CUTOFF = timedelta(minutes=15)


def state_for_acl(user, acl):
    user_state = {
        'is_banned': False,
        'banned_until': False,
        'is_online': False,
        'is_hidden': user.is_hiding_presence,
        'last_click': user.last_login,
    }

    user_ban = get_user_ban(user)
    if user_ban:
        user_state['is_banned'] = True
        user_state['banned_until'] = user_ban.valid_until

    try:
        online_tracker = user.online_tracker
        if online_tracker.last_click >= timezone.now() - ACTIVITY_CUTOFF:
            user_state['is_online'] = True
            user_state['last_click'] = online_tracker.last_click
    except Online.DoesNotExist:
        pass

    return user_state
