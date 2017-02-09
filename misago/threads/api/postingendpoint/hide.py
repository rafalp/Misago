from misago.threads import moderation

from . import PostingEndpoint, PostingMiddleware


class HideMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return self.mode == PostingEndpoint.START and 'hide' in self.request.data

    def post_save(self, serializer):
        if self.thread.category.acl['can_hide_threads']:
            try:
                hide = bool(self.request.data['hide'])
            except (TypeError, ValueError):
                hide = False

            if hide:
                moderation.hide_thread(self.request, self.thread)
                self.thread.update_all = True
                self.thread.save(update_fields=['is_hidden'])

                self.thread.category.synchronize()
                self.thread.category.update_all = True
