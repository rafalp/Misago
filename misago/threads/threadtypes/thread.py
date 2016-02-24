from django.core.urlresolvers import reverse

from misago.threads.threadtypes import ThreadTypeBase


class Thread(ThreadTypeBase):
    type_name = 'thread'

    def get_category_name(self, category):
        return category.name

    def get_category_absolute_url(self, category):
            return reverse('misago:category', kwargs={
                'category_id': category.id, 'category_slug': category.slug
            })

    def get_new_thread_url(self, category):
        return reverse('misago:thread_new', kwargs={
            'category_id': category.id, 'category_slug': category.slug
        })

    def get_reply_url(self, thread):
        return reverse('misago:reply_thread', kwargs={
            'category_id': thread.category.id,
            'thread_id': thread.id,
        })

    def get_edit_post_url(self, post):
        return reverse('misago:edit_post', kwargs={
            'category_id': post.category_id,
            'thread_id': post.thread_id,
            'post_id': post.id
        })

    def get_thread_absolute_url(self, thread):
        return reverse('misago:thread', kwargs={
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

        url = reverse('misago:thread', kwargs=kwargs)
        return '%s#post-%s' % (url, post_id)

    def get_thread_last_reply_url(self, thread):
        return reverse('misago:thread_last', kwargs={
            'thread_slug': thread.slug,
            'thread_id': thread.id
        })

    def get_thread_new_reply_url(self, thread):
        return reverse('misago:thread_new', kwargs={
            'thread_slug': thread.slug,
            'thread_id': thread.id
        })

    def get_thread_moderated_url(self, thread):
        return reverse('misago:thread_moderated', kwargs={
            'thread_slug': thread.slug,
            'thread_id': thread.id
        })

    def get_thread_reported_url(self, thread):
        return reverse('misago:thread_reported', kwargs={
            'thread_slug': thread.slug,
            'thread_id': thread.id
        })

    def get_post_absolute_url(self, post):
        return reverse('misago:thread_post', kwargs={
            'thread_slug': post.thread.slug,
            'thread_id': post.thread.id,
            'post_id': post.id
        })

    def get_post_quote_url(self, post):
        return reverse('misago:quote_post', kwargs={
            'post_id': post.id
        })

    def get_post_approve_url(self, post):
        return reverse('misago:approve_post', kwargs={
            'post_id': post.id
        })

    def get_post_unhide_url(self, post):
        return reverse('misago:unhide_post', kwargs={
            'post_id': post.id
        })

    def get_post_hide_url(self, post):
        return reverse('misago:hide_post', kwargs={
            'post_id': post.id
        })

    def get_post_delete_url(self, post):
        return reverse('misago:delete_post', kwargs={
            'post_id': post.id
        })

    def get_post_report_url(self, post):
        return reverse('misago:report_post', kwargs={
            'post_id': post.id
        })

    def get_event_edit_url(self, event):
        return reverse('misago:edit_event', kwargs={
            'event_id': event.id
        })
