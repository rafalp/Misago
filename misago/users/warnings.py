from datetime import timedelta

from django.utils import timezone

from misago.users.models import WarningLevel


def get_warning_levels():
    return WarningLevel.objects.dict()


def fetch_user_valid_warnings(user):
    levels = get_warning_levels()
    max_level = len(levels) - 1

    if not max_level:
        return []

    # build initial list of valid exceptions
    queryset = user.warnings.exclude(is_canceled=True)
    warnings = [w for w in queryset.order_by('-id')[:max_level]]

    if not warnings:
        return []

    # expire levels
    active_warnings = []
    for length, level in enumerate(levels.values()[1:]):
        length += 1
        level_warnings = []
        if level.length_in_minutes:
            cutoff_date = timezone.now()
            cutoff_date -= timedelta(minutes=level.length_in_minutes)
            for warning in warnings:
                if warning.given_on >= cutoff_date:
                    level_warnings.append(warning)
            if len(level_warnings) == length:
                active_warnings = level_warnings[:length]
            else:
                break
        else:
            active_warnings = warnings[:length]
    return active_warnings



def update_user_warning_level(user):
    warnings = fetch_user_valid_warnings(user)
    user.warning_level = len(warnings)

    levels = get_warning_levels()

    if user.warning_level and levels[user.warning_level].length_in_minutes:
        level_length = levels[user.warning_level].length_in_minutes
        next_check_date = warnings[-1].given_on
        next_check_date += timedelta(minutes=level_length)
        user.warning_level_update_on = next_check_date
    else:
        user.warning_level_update_on = None

    user.save(update_fields=('warning_level', 'warning_level_update_on'))


def get_user_warning_level(user):
    warning_level_expiration = user.warning_level_update_on
    if warning_level_expiration and warning_level_expiration < timezone.now():
        update_user_warning_level(user)
    return user.warning_level


def get_user_warning_obj(user):
    warning_level = get_user_warning_level(user)
    if warning_level:
        return get_warning_levels()[warning_level]
    else:
        return None


def is_user_warning_level_max(user):
    user_level = get_user_warning_level(user)
    levels = len(get_warning_levels())
    return user_level == levels - 1


def warn_user(moderator, user, reason=''):
    warning = user.warnings.create(reason=reason,
                                   giver=moderator,
                                   giver_username=moderator.username,
                                   giver_slug=moderator.slug)

    user.warning_level_update_on = timezone.now()
    update_user_warning_level(user)
    return warning


def cancel_warning(moderator, user, warning):
    warning.cancel(moderator)

    user.warning_level_update_on = timezone.now()
    update_user_warning_level(user)


def delete_warning(moderator, user, warning):
    warning.delete()

    user.warning_level_update_on = timezone.now()
    update_user_warning_level(user)
