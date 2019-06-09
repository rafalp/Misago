from datetime import timedelta

from django.utils import timezone
from django.utils.translation import gettext as _

from . import PostingEndpoint, PostingInterrupt, PostingMiddleware

MIN_POSTING_INTERVAL = 3


class FloodProtectionMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return (
            not self.user_acl["can_omit_flood_protection"]
            and self.mode != PostingEndpoint.EDIT
        )

    def interrupt_posting(self, serializer):
        now = timezone.now()

        if self.user.last_posted_on:
            previous_post = now - self.user.last_posted_on
            if previous_post.total_seconds() < MIN_POSTING_INTERVAL:
                raise PostingInterrupt(
                    _("You can't post message so quickly after previous one.")
                )

        self.user.last_posted_on = timezone.now()
        self.user.update_fields.append("last_posted_on")

        if self.settings.hourly_post_limit:
            cutoff = now - timedelta(hours=24)
            if self.is_limit_exceeded(cutoff, self.settings.hourly_post_limit):
                raise PostingInterrupt(
                    _("Your account has exceed an hourly post limit.")
                )

        if self.settings.daily_post_limit:
            cutoff = now - timedelta(hours=1)
            if self.is_limit_exceeded(cutoff, self.settings.daily_post_limit):
                raise PostingInterrupt(_("Your account has exceed a daily post limit."))

    def is_limit_exceeded(self, cutoff, limit):
        return self.user.post_set.filter(posted_on__gte=cutoff).count() >= limit
