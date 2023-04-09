from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from ...notifications.models import Notification
from ...notifications.permissions import allow_use_notifications
from ..pagination import paginate_queryset
from .serializers import NotificationSerializer


MAX_LIMIT = 50


@api_view(["GET"])
def notifications(request: HttpRequest) -> JsonResponse:
    allow_use_notifications(request.user)

    queryset = (
        Notification.objects.filter(user=request.user)
        .select_related("actor")
        .order_by("-id")
    )

    filter_state = request.GET.get("filter")
    if filter_state == "unread":
        queryset = queryset.filter(is_read=False)
    if filter_state == "read":
        queryset = queryset.filter(is_read=True)

    page = paginate_queryset(request, queryset, "-id", MAX_LIMIT)

    # Reset user unread notifications counter if its first page of unread notifications
    # and  its empty
    if (
        "after" not in request.GET
        and filter_state == "unread"
        and request.user.unread_notifications
        and not page.items
    ):
        request.user.unread_notifications = 0
        request.user.save(update_fields=["unread_notifications"])

    return JsonResponse(
        {
            "results": NotificationSerializer(page.items, many=True).data,
            "hasNext": page.has_next,
            "hasPrevious": page.has_previous,
        }
    )


@api_view(["POST"])
def notifications_read_all(request: HttpRequest) -> HttpResponse:
    allow_use_notifications(request.user)

    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    request.user.unread_notifications = 0
    request.user.save(update_fields=["unread_notifications"])
    return HttpResponse(status=201)
