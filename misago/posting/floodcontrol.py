from datetime import timedelta

from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import pgettext_lazy

# Time window to detect duplicate submissions
DUPLICATE_WINDOW_SECONDS = 5


def flood_control(request: HttpRequest) -> None:
    if not request.settings.flood_control:
        return

    if request.user_permissions.bypass_flood_control:
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


def check_duplicate_submission(request: HttpRequest, title: str = None) -> None:
    """Check if this appears to be a duplicate form submission.

    Prevents double-posting by checking if the same user created a very
    recent thread/post that looks like a duplicate.
    """
    now = timezone.now()
    window = now - timedelta(seconds=DUPLICATE_WINDOW_SECONDS)

    recent_posts = request.user.post_set.filter(posted_at__gt=window).order_by(
        "-posted_at"
    )

    if title:
        from ..core.utils import slugify

        slug = slugify(title)
        recent_threads = request.user.thread_set.filter(
            started_at__gt=window, slug=slug
        )
        if recent_threads.exists():
            raise ValidationError(
                message=pgettext_lazy(
                    "duplicate submission error",
                    "A thread with this title was just posted. Please wait a moment before posting again.",
                ),
                code="duplicate_submission",
            )
    else:
        if recent_posts.exists():
            raise ValidationError(
                message=pgettext_lazy(
                    "duplicate submission error",
                    "A post was just submitted. Please wait a moment before posting again.",
                ),
                code="duplicate_submission",
            )
