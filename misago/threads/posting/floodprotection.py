from django.utils import timezone
from django.utils.translation import ugettext as _

from misago.threads.posting import PostingMiddleware, PostingInterrupt


MIN_POSTING_PAUSE = 3


class FloodProtectionMiddleware(PostingMiddleware):
    def save(self, form):
        message = _("You can't post message so quickly after previous one.")
        if self.user.last_post:
            previous_post = timezone.now() - self.user.last_post
            if previous_post.total_seconds() < MIN_POSTING_PAUSE:
                raise PostingInterrupt(message)

        self.user.last_post = timezone.now()
        self.user.update_fields.append('last_post')
