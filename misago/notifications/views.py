from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Notification
from .permissions import allow_use_notifications
from .redirects import redirect_factory


def notifications(request: HttpRequest) -> HttpResponse:
    allow_use_notifications(request.user)
    return render(request, "misago/notifications.html")


def notification(request: HttpRequest, notification_id: int) -> HttpResponse:
    allow_use_notifications(request.user)

    user = request.user
    notification = get_object_or_404(Notification, user=user, id=notification_id)

    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=["is_read"])

        if user.unread_notifications:
            user.unread_notifications = F("unread_notifications") - 1
            user.save(update_fields=["unread_notifications"])

    return redirect(redirect_factory.get_redirect_url(notification))
