from .treesmap import trees_map


class ThreadType:
    """Abstract class for thread type strategy"""

    root_name = "undefined"

    def get_forum_name(self, category):
        return category.name

    def get_category_absolute_url(self, category):
        return None

    def get_category_last_thread_url(self, category):
        return None

    def get_category_last_post_url(self, category):
        return None

    def get_thread_absolute_url(self, thread, page=1):
        return None

    def get_thread_last_post_url(self, thread):
        return None

    def get_thread_new_post_url(self, thread):
        return None

    def get_thread_best_answer_url(self, thread):
        return None

    def get_thread_unapproved_post_url(self, thread):
        return None

    def get_thread_api_url(self, thread):
        return None

    def get_thread_editor_api_url(self, thread):
        return None

    def get_thread_merge_api_url(self, thread):
        return None

    def get_thread_poll_api_url(self, thread):
        return None

    def get_thread_posts_api_url(self, thread):
        return None

    def get_poll_api_url(self, poll):
        return None

    def get_poll_votes_api_url(self, poll):
        return None

    def get_post_merge_api_url(self, thread):
        return None

    def get_post_move_api_url(self, thread):
        return None

    def get_post_split_api_url(self, thread):
        return None

    def get_post_absolute_url(self, post):
        return None

    def get_post_api_url(self, post):
        return None

    def get_post_likes_api_url(self, post):
        return None

    def get_post_editor_api_url(self, post):
        return None

    def get_post_edits_api_url(self, post):
        return None

    def get_post_read_api_url(self, post):
        return None
