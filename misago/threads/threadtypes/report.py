from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from misago.threads.threadtypes import ThreadTypeBase


class Report(ThreadTypeBase):
    type_name = 'reports'

    def get_forum_name(self, forum):
        return _('Reports')
