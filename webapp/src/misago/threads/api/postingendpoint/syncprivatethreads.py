from . import PostingEndpoint, PostingMiddleware
from ....categories import PRIVATE_THREADS_ROOT_NAME
from ...participants import set_users_unread_private_threads_sync


class SyncPrivateThreadsMiddleware(PostingMiddleware):
    """middleware that sets private thread participants to sync unread threads"""

    def use_this_middleware(self):
        if self.mode == PostingEndpoint.REPLY:
            return self.thread.thread_type.root_name == PRIVATE_THREADS_ROOT_NAME
        return False

    def post_save(self, serializer):
        set_users_unread_private_threads_sync(
            participants=self.thread.participants_list, exclude_user=self.user
        )
