from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from misago.threads.threadtypes import ThreadTypeBase


class PrivateThread(ThreadTypeBase):
    type_name = 'private_threads'

    def get_forum_name(self, forum):
        return _('Private Threads')

    def get_forum_absolute_url(self, forum):
        return reverse('misago:private_threads')

    def get_new_thread_url(self, forum):
        return reverse('misago:private_thread_new')

    def get_reply_url(self, thread):
        return reverse('misago:reply_private_thread', kwargs={
            'thread_id': thread.id,
        })

    def get_edit_post_url(self, post):
        return reverse('misago:edit_private_post', kwargs={
            'forum_id': post.forum_id,
            'thread_id': post.thread_id,
            'post_id': post.id
        })

    def get_thread_absolute_url(self, thread):
        return reverse('misago:private_thread', kwargs={
            'thread_slug': thread.slug,
            'thread_id': thread.id
        })

    def get_thread_post_url(self, thread, post_id, page):
        kwargs = {
            'thread_slug': thread.slug,
            'thread_id': thread.id,
        }
        if page > 1:
            kwargs['page'] = page

        url = reverse('misago:private_thread', kwargs=kwargs)
        return '%s#post-%s' % (url, post_id)

    def get_thread_last_reply_url(self, thread):
        return reverse('misago:private_thread_last', kwargs={
            'thread_slug': thread.slug,
            'thread_id': thread.id
        })

    def get_thread_new_reply_url(self, thread):
        return reverse('misago:private_thread_new', kwargs={
            'thread_slug': thread.slug,
            'thread_id': thread.id
        })

    def get_thread_moderated_url(self, thread):
        return reverse('misago:private_thread_moderated', kwargs={
            'thread_slug': thread.slug,
            'thread_id': thread.id
        })

    def get_thread_reported_url(self, thread):
        return reverse('misago:private_thread_reported', kwargs={
            'thread_slug': thread.slug,
            'thread_id': thread.id
        })

    def get_post_absolute_url(self, post):
        return reverse('misago:private_thread_post', kwargs={
            'thread_slug': post.thread.slug,
            'thread_id': post.thread.id,
            'post_id': post.id
        })

    def get_post_quote_url(self, post):
        return reverse('misago:quote_private_post', kwargs={
            'post_id': post.id
        })

    def get_post_unhide_url(self, post):
        return reverse('misago:unhide_private_post', kwargs={
            'post_id': post.id
        })

    def get_post_hide_url(self, post):
        return reverse('misago:hide_private_post', kwargs={
            'post_id': post.id
        })

    def get_post_delete_url(self, post):
        return reverse('misago:delete_private_post', kwargs={
            'post_id': post.id
        })

    def get_event_edit_url(self, event):
        return reverse('misago:edit_private_event', kwargs={
            'event_id': event.id
        })
