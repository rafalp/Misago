from django.db.models import F

from misago.threads.posting import PostingMiddleware, START, REPLY, EDIT


class UpdateStatsMiddleware(PostingMiddleware):
    def save(self, form):
        self.update_thread()
        self.update_forum()
        self.update_user()

    def update_forum(self):
        if self.mode == START:
            self.forum.threads = F('threads') + 1

        if self.mode != EDIT:
            self.forum.set_last_thread(self.thread)
            self.forum.posts = F('posts') + 1
            self.forum.update_all = True

    def update_thread(self):
        if self.mode == START:
            self.thread.set_first_post(self.post)

        if self.mode != EDIT:
            self.thread.set_last_post(self.post)

        if self.mode == REPLY:
            self.thread.replies = F('replies') + 1

        self.thread.update_all = True

    def update_user(self):
        if self.mode == START:
            self.user.threads = F('threads') + 1
            self.user.update_fields.append('threads')

        if self.mode != EDIT:
            self.user.posts = F('posts') + 1
            self.user.update_fields.append('posts')
