from django.db.models import F

from misago.categories import THREADS_ROOT_NAME

from . import PostingEndpoint, PostingMiddleware


class UpdateStatsMiddleware(PostingMiddleware):
    def save(self, serializer):
        self.update_user(self.user, self.post)
        self.update_thread(self.thread, self.post)
        self.update_category(self.thread.category, self.thread, self.post)

    def update_category(self, category, thread, post):
        if post.is_unapproved:
            return  # don't update category on moderated post

        if self.mode == PostingEndpoint.START:
            category.threads = F('threads') + 1

        if self.mode != PostingEndpoint.EDIT:
            category.set_last_thread(thread)
            category.posts = F('posts') + 1
            category.update_all = True

    def update_thread(self, thread, post):
        if post.is_unapproved:
            thread.has_unapproved_posts = True
            if self.post.id == self.thread.first_post_id:
                thread.is_unapproved = True
        else:
            if self.mode != PostingEndpoint.EDIT:
                thread.set_last_post(post)

            if self.mode == PostingEndpoint.REPLY:
                thread.replies = F('replies') + 1

        thread.update_all = True

    def update_user(self, user, post):
        if post.is_unapproved:
            return  # don't update user on moderated post

        if self.thread.thread_type.root_name == THREADS_ROOT_NAME:
            if self.mode == PostingEndpoint.START:
                user.threads = F('threads') + 1
                user.update_fields.append('threads')

            if self.mode != PostingEndpoint.EDIT:
                user.posts = F('posts') + 1
                user.update_fields.append('posts')
