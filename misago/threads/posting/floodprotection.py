from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext as _

from . import PostingInterrupt, PostingMiddleware


MIN_POSTING_PAUSE = 3


class FloodProtectionMiddleware(PostingMiddleware):
    def interrupt_posting(self, form):
        now = timezone.now()

        if self.user.last_posted_on:
            previous_post = now - self.user.last_posted_on
            if previous_post.total_seconds() < MIN_POSTING_PAUSE:
                raise PostingInterrupt(_("You can't post message so "
                                         "quickly after previous one."))

        self.user.last_posted_on = timezone.now()
        self.user.update_fields.append('last_posted_on')

        if settings.MISAGO_HOURLY_POST_LIMIT:
            cutoff = now - timedelta(hours=24)
            count_qs = self.user.post_set.filter(posted_on__gte=cutoff)
            posts_count = count_qs.count()
            if posts_count > settings.MISAGO_HOURLY_POST_LIMIT:
                raise PostingInterrupt(_("Your account has excceed "
                                         "hourly post limit."))

        if settings.MISAGO_DIALY_POST_LIMIT:
            cutoff = now - timedelta(hours=1)
            count_qs = self.user.post_set.filter(posted_on__gte=cutoff)
            posts_count = count_qs.count()
            if posts_count > settings.MISAGO_DIALY_POST_LIMIT:
                raise PostingInterrupt(_("Your account has excceed "
                                         "dialy post limit."))
