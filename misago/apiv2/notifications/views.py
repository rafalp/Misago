from typing import List

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view

from ...conf import settings
from ...notifications.models import Notification
from ...notifications.permissions import allow_use_notifications
from ..pagination import paginate_queryset
from .serializers import NotificationSerializer


@api_view(["GET"])
def notifications(request: HttpRequest) -> JsonResponse:
    allow_use_notifications(request.user)

    queryset = (
        Notification.objects.filter(user=request.user)
        .select_related("actor")
        .order_by("-id")
    )

    filter_by = request.GET.get("filter")
    if filter_by == "unread":
        queryset = queryset.filter(is_read=False)
    if filter_by == "read":
        queryset = queryset.filter(is_read=True)

    page = paginate_queryset(
        request,
        queryset,
        "-id",
        settings.MISAGO_NOTIFICATIONS_PAGE_LIMIT,
    )

    # Clear user unread notifications counter if its first page of notifications
    # and the counter is obviously invalid
    if (
        "after" not in request.GET
        and filter_by != "read"
        and not page.items
        and request.user.unread_notifications
    ):
        request.user.unread_notifications = 0
        request.user.save(update_fields=["unread_notifications"])

    # Recount unread unread notifications if counter shows 0 but unread
    # notifications exist
    if not request.user.unread_notifications and unread_items_exist(
        filter_by, page.items
    ):
        count_limit = settings.MISAGO_UNREAD_NOTIFICATIONS_LIMIT + 1
        real_unread_notifications = queryset[:count_limit].count()
        if real_unread_notifications:
            request.user.unread_notifications = real_unread_notifications
            request.user.save(update_fields=["unread_notifications"])

    return JsonResponse(
        {
            "results": NotificationSerializer(page.items, many=True).data,
            "hasNext": page.has_next,
            "hasPrevious": page.has_previous,
            "firstCursor": page.first_cursor,
            "lastCursor": page.last_cursor,
            "unreadNotifications": (
                request.user.get_unread_notifications_for_display()
            ),
        }
    )


def unread_items_exist(filter_by: str, items: List[Notification]) -> int:
    if filter_by == "unread":
        return bool(items)

    if filter_by != "read":
        for notification in items:
            if not notification.is_read:
                return True

    return False


@api_view(["POST"])
def notifications_read_all(request: HttpRequest) -> HttpResponse:
    allow_use_notifications(request.user)

    Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).update(
        is_read=True,
        read_at=timezone.now(),
    )
    request.user.unread_notifications = 0
    request.user.save(update_fields=["unread_notifications"])
    return HttpResponse(status=204)
