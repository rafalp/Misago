from django.db.models import F
from django.db.transaction import atomic
from django.utils.html import escape

from misago.notifications.models import Notification


__all__ = ['notify_user']


def notify_user(user, message, url, trigger, formats=None, sender=None):
    message_escaped = escape(message)
    if formats:
        final_formats = {}
        for format, replace in formats.items():
            final_formats[format] = '<strong>%s</strong>' % escape(replace)
        message_escaped = message_escaped % final_formats

    new_notification = Notification(user=user,
                                    trigger=trigger,
                                    url=url,
                                    message=message_escaped)

    if sender:
        new_notification.sender = sender
        new_notification.sender_username = sender.username
        new_notification.sender_slug = sender.slug

    new_notification.save()
    user.new_notifications = F('new_notifications') + 1
    user.save(update_fields=['new_notifications'])


#def read_user_notifications(user, trigger):
#    pass


#def read_all_user_alerts(user):
#    pass
