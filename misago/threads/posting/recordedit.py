from django.db.models import F

from misago.threads.posting import PostingMiddleware, EDIT


class RecordEditMiddleware(PostingMiddleware):
    def __init__(self, **kwargs):
        super(RecordEditMiddleware, self).__init__(**kwargs)

        if self.mode == EDIT:
            self.original_title = self.thread.title
            self.original_post = self.post.original

    def save(self, form):
        if self.mode == EDIT:
            # record edit
            self.post.edits += 1
            self.post.update_fields.append('edits')
