from datetime import timedelta

from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import npgettext_lazy


def check_daily_post_limit(request: HttpRequest) -> None:
    if not request.settings.daily_post_limit:
        return

    if request.user_permissions.exempt_from_posting_limits:
        return

    posts_cutoff = timezone.now() - timedelta(hours=24)
    posts_queryset = request.user.post_set.filter(posted_on__gt=posts_cutoff)

    if posts_queryset.count() >= request.settings.daily_post_limit:
        raise ValidationError(
            message=npgettext_lazy(
                "posts limits",
                "You can't post more than %(limit_value)s message within 24 hours.",
                "You can't post more than %(limit_value)s messages within 24 hours.",
                request.settings.daily_post_limit,
            ),
            code="daily_post_limit",
            params={
                "limit_value": request.settings.daily_post_limit,
            },
        )


def check_hourly_post_limit(request: HttpRequest) -> None:
    if not request.settings.hourly_post_limit:
        return

    if request.user_permissions.exempt_from_posting_limits:
        return

    posts_cutoff = timezone.now() - timedelta(hours=1)
    posts_queryset = request.user.post_set.filter(posted_on__gt=posts_cutoff)

    if posts_queryset.count() >= request.settings.hourly_post_limit:
        raise ValidationError(
            message=npgettext_lazy(
                "posts limits",
                "You can't post more than %(limit_value)s message within an hour.",
                "You can't post more than %(limit_value)s messages within an hour.",
                request.settings.hourly_post_limit,
            ),
            code="hourly_post_limit",
            params={
                "limit_value": request.settings.hourly_post_limit,
            },
        )
