from misago.threads import moderation

from . import PostingEndpoint, PostingMiddleware


class CloseMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return self.mode == PostingEndpoint.START and 'close' in self.request.data

    def post_save(self, serializer):
        if self.thread.category.acl['can_close_threads']:
            try:
                close = bool(self.request.data['close'])
            except (TypeError, ValueError):
                close = False

            if close:
                moderation.close_thread(self.request, self.thread)
