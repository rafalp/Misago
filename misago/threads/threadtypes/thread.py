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

    def get_thread_absolute_url(self, thread):
        return reverse('misago:thread', kwargs={
            'thread_slug': thread.slug,
            'thread_id': thread.id
        })