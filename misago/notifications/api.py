from django.db.models import F
from django.db import transaction
from django.utils.html import escape

from misago.notifications.utils import hash_trigger


__all__ = [
    'notify_user',
    'read_user_notification',
    'read_all_user_alerts',
    'assert_real_new_notifications_count',
]


def notify_user(user, message, url, trigger, formats=None, sender=None,
                update_user=True):
    from misago.notifications.models import Notification

    message_escaped = escape(message)
    if formats:
        final_formats = {}
        for format, replace in formats.items():
            final_formats[format] = '<strong>%s</strong>' % escape(replace)
        message_escaped = message_escaped % final_formats

    new_notification = Notification(user=user,
                                    trigger=hash_trigger(trigger),
                                    url=url,
                                    message=message_escaped)

    if sender:
        new_notification.sender = sender
        new_notification.sender_username = sender.username
        new_notification.sender_slug = sender.slug

    new_notification.save()
    user.new_notifications = F('new_notifications') + 1
    if update_user:
        user.save(update_fields=['new_notifications'])
    return new_notification


def read_user_notification(user, trigger, atomic=True):
    if user.new_notifications:
        if atomic:
            with transaction.atomic():
                _real_read_user_notification(user, trigger)
        else:
            _real_read_user_notification(user, trigger)


def _real_read_user_notification(user, trigger):
    trigger_hash = hash_trigger(trigger)
    update_qs = user.notifications.filter(is_new=True)
    update_qs = update_qs.filter(trigger=trigger_hash)
    updated = update_qs.update(is_new=False)

    if updated:
        user.new_notifications -= updated
        if user.new_notifications < 0:
            # Cos no. of changed rows returned via update()
            # isn't always accurate
            user.new_notifications = 0
        user.save(update_fields=['new_notifications'])


def read_all_user_alerts(user):
    locked_user = user.lock()
    user.new_notifications = 0
    locked_user.new_notifications = 0
    locked_user.save(update_fields=['new_notifications'])
    locked_user.notifications.update(is_new=False)


def assert_real_new_notifications_count(user):
    if user.new_notifications:
        real_new_count = user.notifications.filter(is_new=True).count()
        if real_new_count != user.new_notifications:
            user.new_notifications = real_new_count
            user.save(update_fields=['new_notifications'])
