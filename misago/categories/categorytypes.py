from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from misago.threads.threadtypes import ThreadTypeBase


class RootCategory(ThreadTypeBase):
    type_name = 'root_category'

    def get_category_name(self, category):
        return _('None (will become top level category)')


class Category(ThreadTypeBase):
    type_name = 'category'

    def get_category_absolute_url(self, category):
        if category.level == 1:
            formats = (reverse('misago:index'), category.slug, category.id)
            return '%s#%s-%s' % formats
        else:
            return reverse('misago:category', kwargs={
                'category_id': category.id, 'category_slug': category.slug
            })