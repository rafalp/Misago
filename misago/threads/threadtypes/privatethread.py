from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from . import ThreadType


class PrivateThread(ThreadType):
    root_name = 'private_threads'

    def get_category_name(self, category):
        return _('Private Threads')

    def get_category_absolute_url(self, category):
        return reverse('misago:private-threads')

    def get_thread_absolute_url(self, thread, page=1):
        if page > 1:
            return reverse('misago:private-thread', kwargs={
                'slug': thread.slug,
                'pk': thread.pk,
                'page': page
            })
        else:
            return reverse('misago:private-thread', kwargs={
                'slug': thread.slug,
                'pk': thread.pk
            })
