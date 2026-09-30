from django.http import HttpRequest
from django.utils import timezone

from .models import SearchLog


def throttle_search(request: HttpRequest) -> int:
    queryset = SearchLog.objects

    if request.user.is_authenticated:
        min_search_interval = request.settings.user_min_search_interval
        queryset = queryset.filter(user=request.user)
    else:
        min_search_interval = request.settings.guest_min_search_interval
        queryset = queryset.filter(
            user__isnull=True,
            ip_address=request.user_ip,
        )

    if not min_search_interval:
        return 0

    latest_search = queryset.values_list("searched_at", flat=True).first()

    if not latest_search:
        return 0

    seconds_since_search = int((timezone.now() - latest_search).total_seconds())
    return max(min_search_interval - seconds_since_search, 0)
