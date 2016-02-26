from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from misago.threads.threadtypes import ThreadTypeBase


class PrivateThread(ThreadTypeBase):
    type_name = 'private_threads'

    def get_category_name(self, category):
        return _('Private Threads')

    def get_category_absolute_url(self, category):
        return reverse('misago:private_threads')

    def get_thread_absolute_url(self, thread):
        return reverse('misago:private_thread', kwargs={
            'thread_slug': thread.slug,
            'thread_id': thread.id
        })