from django.db.models import F

from . import EDIT, PostingMiddleware


class RecordEditMiddleware(PostingMiddleware):
    def __init__(self, **kwargs):
        super(RecordEditMiddleware, self).__init__(**kwargs)

        if self.mode == EDIT:
            self.original_title = self.thread.title
            self.original_post = self.post.original

    def save(self, form):
        if self.mode == EDIT:
            # record post or thread edit
            is_title_changed = self.original_title != self.thread.title
            is_post_changed = self.original_post != self.post.original

            if is_title_changed or is_post_changed:
                self.post.edits += 1
                self.post.last_editor_name = self.user.username
                self.post.update_fields.extend(('edits', 'last_editor_name'))
