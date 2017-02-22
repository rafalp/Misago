from datetime import timedelta

from django.utils import timezone
from django.utils.translation import ugettext as _

from misago.conf import settings

from . import PostingEndpoint, PostingInterrupt, PostingMiddleware


MIN_POSTING_PAUSE = 3


class FloodProtectionMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return not self.user.acl_cache['can_omit_flood_protection'
                                       ] and self.mode != PostingEndpoint.EDIT

    def interrupt_posting(self, serializer):
        now = timezone.now()

        if self.user.last_posted_on:
            previous_post = now - self.user.last_posted_on
            if previous_post.total_seconds() < MIN_POSTING_PAUSE:
                raise PostingInterrupt(_("You can't post message so quickly after previous one."))

        self.user.last_posted_on = timezone.now()
        self.user.update_fields.append('last_posted_on')

        if settings.MISAGO_HOURLY_POST_LIMIT:
            cutoff = now - timedelta(hours=24)
            if self.is_limit_exceeded(cutoff, settings.MISAGO_HOURLY_POST_LIMIT):
                raise PostingInterrupt(_("Your account has excceed hourly post limit."))

        if settings.MISAGO_DIALY_POST_LIMIT:
            cutoff = now - timedelta(hours=1)
            if self.is_limit_exceeded(cutoff, settings.MISAGO_DIALY_POST_LIMIT):
                raise PostingInterrupt(_("Your account has excceed dialy post limit."))

    def is_limit_exceeded(self, cutoff, limit):
        return self.user.post_set.filter(posted_on__gte=cutoff).count() >= limit
