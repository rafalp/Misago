from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from misago.threads.threadtypes import ThreadTypeBase


class RootCategory(ThreadTypeBase):
    type_name = 'root_category'

    def get_category_name(self, category):
        return _('None (will become top level category)')

    def get_category_absolute_url(self, category):
        return reverse('misago:threads')

    def get_thread_absolute_url(self, thread):
        return '/thread/not-yet-%s/' % thread.pk

    def get_last_thread_url(self, category):
        if category.last_thread_id:
            return '/not-yet-implemented/'
        else:
            return None


class Category(RootCategory):
    type_name = 'category'

    def get_category_name(self, category):
        return category.name

    def get_category_absolute_url(self, category):
        return reverse('misago:category', kwargs={
            'category_slug': category.slug,
            'category_id': category.id,
        })