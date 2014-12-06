from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from misago.threads.threadtypes import ThreadTypeBase


class RootCategory(ThreadTypeBase):
    type_name = 'root_category'

    def get_forum_name(self, forum):
        return _('None (will become top level category)')


class Category(ThreadTypeBase):
    type_name = 'category'

    def get_forum_absolute_url(self, forum):
        if forum.level == 1:
            formats = (reverse('misago:index'), forum.slug, forum.id)
            return '%s#%s-%s' % formats
        else:
            return reverse('misago:category', kwargs={
                'forum_id': forum.id, 'forum_slug': forum.slug
            })


class Redirect(ThreadTypeBase):
    type_name = 'redirect'

    def get_forum_absolute_url(self, forum):
        return reverse('misago:redirect', kwargs={
            'forum_id': forum.id, 'forum_slug': forum.slug
        })
