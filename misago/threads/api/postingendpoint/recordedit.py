from django.db.models import F

from . import PostingEndpoint, PostingMiddleware


class RecordEditMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        self.original_post = self.post.original

        return self.mode == PostingEndpoint.EDIT

    def save(self, serializer):
        is_post_changed = self.original_post != self.post.original
        if not is_post_changed:
            return

        self.post.updated_on = self.datetime
        self.post.edits = F('edits') + 1

        self.post.last_editor = self.user
        self.post.last_editor_name = self.user.username
        self.post.last_editor_slug = self.user.slug

        self.post.update_fields.extend(
            ('updated_on', 'edits', 'last_editor', 'last_editor_name', 'last_editor_slug', )
        )

        self.post.edits_record.create(
            category=self.post.category,
            thread=self.thread,
            edited_on=self.datetime,
            editor=self.user,
            editor_name=self.user.username,
            editor_slug=self.user.slug,
            editor_ip=self.request.user_ip,
            edited_from=self.original_post,
            edited_to=self.post.original,
        )
