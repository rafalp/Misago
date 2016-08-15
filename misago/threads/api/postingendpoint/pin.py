from . import PostingEndpoint, PostingMiddleware
from ... import moderation


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
                if pin == 2:
                    moderation.pin_thread_globally(self.request, self.thread)
                elif pin == 1:
                    moderation.pin_thread_locally(self.request, self.thread)
