from django.db.models import Q

from .models import Notification, WatchedThread


def archive_user_notifications(sender, archive=None, **kwargs):
    queryset = Notification.objects.filter(Q(user=sender) | Q(actor=sender)).order_by(
        "id"
    )

    for notification in queryset.iterator(chunk_size=50):
        item_name = notification.created_at.strftime("%H%M%S-notification")
        archive.add_text(
            item_name,
            registry.get_message(notification),
            date=notification.created_at,
        )


def delete_user_account(user):
    Notification.objects.filter(actor=user).update(actor=None)
    Notification.objects.filter(user=user).delete()
    WatchedThread.objects.filter(user=user).delete()


def delete_user_data(user):
    Notification.objects.filter(Q(user=user) | Q(actor=user)).delete()
    WatchedThread.objects.filter(user=user).delete()


def update_actor_name(user, **kwargs):
    Notification.objects.filter(actor=user).update(actor_name=user.username)