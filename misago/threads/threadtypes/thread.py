from django.core.urlresolvers import reverse

from misago.threads.threadtypes import ThreadTypeBase


class Thread(ThreadTypeBase):
    type_name = 'thread'

    def get_category_name(self, category):
        return category.name

    def get_category_absolute_url(self, category):
        return reverse('misago:category', kwargs={
            'pk': category.pk,
            'slug': category.slug,
        })

    def get_thread_absolute_url(self, thread):
        return '/threads/not-implemented-yet-%s/' % thread.pk

    def get_thread_last_post_url(self, thread):
        return '/threads/not-implemented-yet-%s/last/' % thread.pk

    def get_thread_new_post_url(self, thread):
        return '/threads/not-implemented-yet-%s/new/' % thread.pk

    def get_thread_api_url(self, thread):
        return reverse('misago:api:thread-detail', kwargs={'pk': thread.pk})