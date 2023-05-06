from ....notifications.tasks import notify_on_new_thread_reply
from ....notifications.threads import (
    watch_replied_thread,
    watch_started_thread,
)
from . import PostingEndpoint, PostingMiddleware


class NotificationsMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return self.mode != PostingEndpoint.EDIT

    def post_save(self, serializer):
        if self.mode == PostingEndpoint.START:
            watch_started_thread(self.user, self.thread)
        elif self.mode == PostingEndpoint.REPLY:
            watch_replied_thread(self.user, self.thread)

        if self.mode == PostingEndpoint.REPLY:
            notify_on_new_thread_reply.delay(self.post.id)
