from . import PostingEndpoint, PostingMiddleware
from ....acl.objectacl import add_acl_to_obj
from ....categories import PRIVATE_THREADS_ROOT_NAME
from ....categories.models import Category


class PrivateThreadMiddleware(PostingMiddleware):
    """middleware that sets private threads category for thread and post"""

    def use_this_middleware(self):
        if self.mode == PostingEndpoint.START:
            return self.tree_name == PRIVATE_THREADS_ROOT_NAME
        return False

    def pre_save(self, serializer):
        category = Category.objects.private_threads()

        add_acl_to_obj(self.user_acl, category)

        # set flags for savechanges middleware
        category.update_all = False
        category.update_fields = []

        # assign category to thread and post
        self.thread.category = category
        self.post.category = category
