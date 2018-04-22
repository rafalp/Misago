from misago.acl import add_acl
from misago.categories.models import PRIVATE_THREADS_ROOT, Category

from . import PostingEndpoint, PostingMiddleware


class PrivateThreadMiddleware(PostingMiddleware):
    """middleware that sets private threads category for thread and post"""

    def use_this_middleware(self):
        if self.mode == PostingEndpoint.START:
            return self.tree_name == PRIVATE_THREADS_ROOT
        return False

    def pre_save(self, serializer):
        category = Category.objects.private_threads()

        add_acl(self.user, category)

        # set flags for savechanges middleware
        category.update_all = False
        category.update_fields = []

        # assign category to thread and post
        self.thread.category = category
        self.post.category = category
