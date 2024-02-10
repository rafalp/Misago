from django.db.models import F
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .exceptions import NotificationVerbError
from .models import Notification, WatchedThread
from .permissions import allow_use_notifications
from .registry import registry


def notifications(request: HttpRequest) -> HttpResponse:
    allow_use_notifications(request.user)
    return render(request, "misago/notifications.html")


def notification(request: HttpRequest, notification_id: int) -> HttpResponse:
    allow_use_notifications(request.user)

    user = request.user
    notification = get_object_or_404(
        Notification.objects.select_related(
            "actor",
            "category",
            "thread",
            "post",
        ),
        user=user,
        id=notification_id,
    )

    # Populate user relation cache
    notification.user = request.user

    if notification.category_id:
        # Populate relations caches on thread and post models
        if notification.thread_id:
            notification.thread.category = notification.category
        if notification.post_id:
            notification.post.thread = notification.thread
            notification.post.category = notification.category

    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=["is_read"])

        if user.unread_notifications:
            user.unread_notifications = F("unread_notifications") - 1
            user.save(update_fields=["unread_notifications"])

    try:
        return redirect(registry.get_redirect_url(request, notification))
    except NotificationVerbError as error:
        raise Http404() from error


def disable_email_notifications(
    request: HttpRequest, watched_thread_id: int, secret: str
) -> HttpResponse:
    watched_thread = get_object_or_404(
        WatchedThread.objects.select_related("user", "category", "thread"),
        id=watched_thread_id,
        secret=secret,
    )

    if watched_thread.send_emails:
        watched_thread.send_emails = False
        watched_thread.save(update_fields=["send_emails"])

    watched_thread.thread.category = watched_thread.category

    return render(
        request,
        "misago/notifications_disabled.html",
        {
            "watcher": watched_thread.user,
            "thread": watched_thread.thread,
        },
    )
