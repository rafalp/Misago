from misago.threads import moderation
from misago.threads.models import Thread

from . import PostingEndpoint, PostingMiddleware


class PinMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return self.mode == PostingEndpoint.START and 'pin' in self.request.data

    def post_save(self, serializer):
        allowed_pin = self.thread.category.acl['can_pin_threads']
        if allowed_pin > 0:
            try:
                pin = int(self.request.data['pin'])
            except (TypeError, ValueError):
                pin = 0

            if pin <= allowed_pin:
                if pin == Thread.WEIGHT_GLOBAL:
                    moderation.pin_thread_globally(self.request, self.thread)
                elif pin == Thread.WEIGHT_PINNED:
                    moderation.pin_thread_locally(self.request, self.thread)
