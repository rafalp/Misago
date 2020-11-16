from . import PostingEndpoint, PostingMiddleware
from ....categories import PRIVATE_THREADS_ROOT_NAME


class ModerationQueueMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        try:
            tree_name = self.tree_name
        except AttributeError:
            tree_name = self.thread.category.thread_type.root_name

        return tree_name != PRIVATE_THREADS_ROOT_NAME

    def save(self, serializer):
        if self.mode == PostingEndpoint.START:
            self.post.is_unapproved = self.thread.category.acl[
                "require_threads_approval"
            ]

        if self.mode == PostingEndpoint.REPLY:
            self.post.is_unapproved = self.thread.category.acl[
                "require_replies_approval"
            ]

        if self.mode == PostingEndpoint.EDIT:
            self.post.is_unapproved = self.thread.category.acl["require_edits_approval"]

        if self.post.is_unapproved:
            self.post.update_fields.append("is_unapproved")
