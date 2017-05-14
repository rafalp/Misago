from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from misago.categories import THREADS_ROOT_NAME

from . import ThreadType


class Thread(ThreadType):
    root_name = THREADS_ROOT_NAME

    def get_category_name(self, category):
        if category.level:
            return category.name
        else:
            return _('None (will become top level category)')

    def get_category_absolute_url(self, category):
        if category.level:
            return reverse(
                'misago:category', kwargs={
                    'pk': category.pk,
                    'slug': category.slug,
                }
            )
        else:
            return reverse('misago:threads')

    def get_category_last_thread_url(self, category):
        return reverse(
            'misago:thread',
            kwargs={
                'slug': category.last_thread_slug,
                'pk': category.last_thread_id,
            }
        )

    def get_category_last_thread_new_url(self, category):
        return reverse(
            'misago:thread-new',
            kwargs={
                'slug': category.last_thread_slug,
                'pk': category.last_thread_id,
            }
        )

    def get_category_last_post_url(self, category):
        return reverse(
            'misago:thread-last',
            kwargs={
                'slug': category.last_thread_slug,
                'pk': category.last_thread_id,
            }
        )

    def get_category_read_api_url(self, category):
        return '{}?category={}'.format(reverse('misago:api:thread-read'), category.pk)

    def get_thread_absolute_url(self, thread, page=1):
        if page > 1:
            return reverse(
                'misago:thread', kwargs={
                    'slug': thread.slug,
                    'pk': thread.pk,
                    'page': page,
                }
            )
        else:
            return reverse(
                'misago:thread', kwargs={
                    'slug': thread.slug,
                    'pk': thread.pk,
                }
            )

    def get_thread_last_post_url(self, thread):
        return reverse(
            'misago:thread-last', kwargs={
                'slug': thread.slug,
                'pk': thread.pk,
            }
        )

    def get_thread_new_post_url(self, thread):
        return reverse(
            'misago:thread-new', kwargs={
                'slug': thread.slug,
                'pk': thread.pk,
            }
        )

    def get_thread_unapproved_post_url(self, thread):
        return reverse(
            'misago:thread-unapproved', kwargs={
                'slug': thread.slug,
                'pk': thread.pk,
            }
        )

    def get_thread_api_url(self, thread):
        return reverse(
            'misago:api:thread-detail', kwargs={
                'pk': thread.pk,
            }
        )

    def get_thread_editor_api_url(self, thread):
        return reverse(
            'misago:api:thread-post-editor', kwargs={
                'thread_pk': thread.pk,
            }
        )

    def get_thread_merge_api_url(self, thread):
        return reverse(
            'misago:api:thread-merge', kwargs={
                'pk': thread.pk,
            }
        )

    def get_thread_poll_api_url(self, thread):
        return reverse(
            'misago:api:thread-poll-list', kwargs={
                'thread_pk': thread.pk,
            }
        )

    def get_thread_posts_api_url(self, thread):
        return reverse(
            'misago:api:thread-post-list', kwargs={
                'thread_pk': thread.pk,
            }
        )

    def get_poll_api_url(self, poll):
        return reverse(
            'misago:api:thread-poll-detail', kwargs={
                'thread_pk': poll.thread_id,
                'pk': poll.pk,
            }
        )

    def get_poll_votes_api_url(self, poll):
        return reverse(
            'misago:api:thread-poll-votes', kwargs={
                'thread_pk': poll.thread_id,
                'pk': poll.pk,
            }
        )

    def get_post_merge_api_url(self, thread):
        return reverse(
            'misago:api:thread-post-merge', kwargs={
                'thread_pk': thread.pk,
            }
        )

    def get_post_move_api_url(self, thread):
        return reverse(
            'misago:api:thread-post-move', kwargs={
                'thread_pk': thread.pk,
            }
        )

    def get_post_split_api_url(self, thread):
        return reverse(
            'misago:api:thread-post-split', kwargs={
                'thread_pk': thread.pk,
            }
        )

    def get_post_absolute_url(self, post):
        return reverse(
            'misago:thread-post',
            kwargs={
                'slug': post.thread.slug,
                'pk': post.thread.pk,
                'post': post.pk,
            }
        )

    def get_post_api_url(self, post):
        return reverse(
            'misago:api:thread-post-detail', kwargs={
                'thread_pk': post.thread_id,
                'pk': post.pk,
            }
        )

    def get_post_likes_api_url(self, post):
        return reverse(
            'misago:api:thread-post-likes', kwargs={
                'thread_pk': post.thread_id,
                'pk': post.pk,
            }
        )

    def get_post_editor_api_url(self, post):
        return reverse(
            'misago:api:thread-post-editor', kwargs={
                'thread_pk': post.thread_id,
                'pk': post.pk,
            }
        )

    def get_post_edits_api_url(self, post):
        return reverse(
            'misago:api:thread-post-edits', kwargs={
                'thread_pk': post.thread_id,
                'pk': post.pk,
            }
        )

    def get_post_read_api_url(self, post):
        return reverse(
            'misago:api:thread-post-read', kwargs={
                'thread_pk': post.thread_id,
                'pk': post.pk,
            }
        )
