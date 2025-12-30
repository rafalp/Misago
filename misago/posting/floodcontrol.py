from datetime import timedelta

from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import pgettext_lazy


def flood_control(request: HttpRequest) -> None:
    if not request.settings.flood_control:
        return

    if request.user_permissions.exempt_from_flood_control:
        return

    flood_posts = timezone.now() - timedelta(seconds=request.settings.flood_control)
    posts_queryset = request.user.post_set.filter(posted_at__gt=flood_posts)

    if posts_queryset.exists():
        raise ValidationError(
            message=pgettext_lazy(
                "flood control validator",
                "You can't post a new message so soon after the previous one.",
            ),
            code="flood_control",
        )
