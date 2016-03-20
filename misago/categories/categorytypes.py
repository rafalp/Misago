from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from misago.threads.threadtypes.thread import Thread


class RootCategory(Thread):
    type_name = 'root_category'

    def get_category_name(self, category):
        return _('None (will become top level category)')

    def get_category_absolute_url(self, category):
        return reverse('misago:threads')


class Category(RootCategory):
    type_name = 'category'

    def get_category_name(self, category):
        return category.name

    def get_category_absolute_url(self, category):
        return reverse('misago:category', kwargs={
            'category_slug': category.slug,
            'category_id': category.id,
        })