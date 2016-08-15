from . import PostingEndpoint, PostingMiddleware


class ProtectMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return self.mode == PostingEndpoint.EDIT and 'protect' in self.request.data

    def post_save(self, serializer):
        if self.thread.category.acl['can_protect_posts']:
            try:
                self.post.is_protected = bool(self.request.data['protect'])
                self.post.update_fields.append('is_protected')
            except (TypeError, ValueError):
                pass
