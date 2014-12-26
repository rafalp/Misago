from django.db.models import F
from django.db import transaction
from django.utils.html import escape

from misago.notifications.checksums import update_checksum
from misago.notifications.utils import hash_type


__all__ = [
    'notify_user',
    'read_user_notifications',
    'read_all_user_alerts',
    'assert_real_new_notifications_count',
]


def notify_user(user, message, url, type=None, formats=None, sender=None,
                update_user=True):
    from misago.notifications.models import Notification

    message_escaped = escape(message)
    if formats:
        final_formats = {}
        for format, replace in formats.items():
            final_formats[format] = '<strong>%s</strong>' % escape(replace)
        message_escaped = message_escaped % final_formats

    new_notification = Notification(user=user,
                                    hash=hash_type(type or message),
                                    url=url,
                                    message=message_escaped)

    if sender:
        new_notification.sender = sender
        new_notification.sender_username = sender.username
        new_notification.sender_slug = sender.slug

    new_notification.save()

    update_checksum(new_notification)
    new_notification.save(update_fields=['checksum'])

    user.new_notifications = F('new_notifications') + 1
    if update_user:
        user.save(update_fields=['new_notifications'])
    return new_notification


def read_user_notifications(user, types, atomic=True):
    if user.is_authenticated() and user.new_notifications:
        if atomic:
            with transaction.atomic():
                _real_read_user_notifications(user, types)
        else:
            _real_read_user_notifications(user, types)


def _real_read_user_notifications(user, types):
    if isinstance(types, basestring):
        types = [types]

    hashes = [hash_type(type) for type in types]
    update_qs = user.misago_notifications.filter(is_new=True)
    update_qs = update_qs.filter(hash__in=hashes)
    updated = update_qs.update(is_new=False)

    if updated:
        user.new_notifications -= updated
        if user.new_notifications < 0:
            # Cos no. of changed rows returned via update()
            # isn't always accurate, lets keep it at 0
            # if user's curious about real count, he can
            # trigger count sync via loading list
            user.new_notifications = 0
        user.save(update_fields=['new_notifications'])


def read_all_user_alerts(user):
    locked_user = user.lock()
    user.new_notifications = 0
    locked_user.new_notifications = 0
    locked_user.save(update_fields=['new_notifications'])
    locked_user.misago_notifications.update(is_new=False)


def assert_real_new_notifications_count(user):
    if user.new_notifications:
        real_new_count = user.misago_notifications.filter(is_new=True).count()
        if real_new_count != user.new_notifications:
            user.new_notifications = real_new_count
            user.save(update_fields=['new_notifications'])
