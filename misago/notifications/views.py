from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import pgettext

from ..permissions.notifications import check_notifications_permission
from ..privatethreads.views.backend import private_thread_backend
from ..threads.models import Thread
from ..threads.views.backend import thread_backend
from ..threads.views.generic import GenericThreadView
from .enums import ThreadNotifications
from .exceptions import NotificationVerbError
from .models import Notification, WatchedThread
from .registry import registry
from .templates import (
    WATCH_THREAD_BUTTON_TEMPLATE,
    WATCH_THREAD_DROPDOWN_TEMPLATE,
)
from .threads import unwatch_thread, watch_thread


def notifications(request: HttpRequest) -> HttpResponse:
    check_notifications_permission(request.user_permissions)
    return render(request, "misago/notifications.html")


def notification(request: HttpRequest, notification_id: int) -> HttpResponse:
    check_notifications_permission(request.user_permissions)

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


class WatchView(GenericThreadView):
    template_name = "misago/watch_thread/htmx.html"

    def post(self, request: HttpRequest, thread_id: int, slug: str) -> HttpResponse:
        if request.user.is_anonymous:
            raise PermissionDenied(
                pgettext(
                    "watch thread permission error",
                    "You must be signed in to watch threads.",
                )
            )

        thread = self.get_thread(request, thread_id)

        watched_thread = None
        notifications = self.get_notification_level(request)

        if notifications:
            watched_thread, created = self.watch_thread(request, thread, notifications)
            if created:
                message = pgettext("thread watched", "Notifications enabled")
                messages.success(request, message)
        else:
            if unwatch_thread(thread, request.user, request):
                message = pgettext("thread unwatched", "Notifications disabled")
                messages.info(request, message)

        if request.is_htmx:
            return render(
                request,
                self.template_name,
                get_watched_thread_context_data(watched_thread),
            )

        # Redirect back to the `next` url
        next_thread_url = self.get_next_thread_url(request, thread)
        return redirect(next_thread_url)

    def get_notification_level(self, request: HttpRequest) -> int | None:
        try:
            return ThreadNotifications(int(request.POST.get("notifications")))
        except (ValueError, TypeError):
            return None

    @transaction.atomic
    def watch_thread(
        self, request: HttpRequest, thread: Thread, notifications: int
    ) -> tuple[WatchedThread, bool]:
        deleted, _ = WatchedThread.objects.filter(
            user=request.user, thread=thread
        ).delete()

        watched_thread = watch_thread(
            thread,
            request.user,
            send_emails=notifications == ThreadNotifications.SITE_AND_EMAIL,
            request=request,
        )

        return watched_thread, not deleted


class ThreadWatchView(WatchView):
    backend = thread_backend


class PrivateThreadWatchView(WatchView):
    backend = private_thread_backend


def get_watched_thread_context_data(
    watched_thread: WatchedThread | None = None,
) -> dict:
    return {
        "button_template": WATCH_THREAD_BUTTON_TEMPLATE,
        "dropdown_template": WATCH_THREAD_DROPDOWN_TEMPLATE,
        "notifications_enabled": bool(watched_thread),
        "notifications_site_and_email": bool(
            watched_thread and watched_thread.send_emails
        ),
        "notifications_site_only": bool(
            watched_thread and not watched_thread.send_emails
        ),
        "notifications_disabled": not watched_thread,
    }
