import base64
from misago.admin.models import Section, Action
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid

admin_fixtures = {
    # Overview
    'overview': {
        'name': _('Overview'),
        'icon': 'signal',
        'pos': 0,
    },

    # Users
    'users': {
        'name': _('Users'),
        'icon': 'user',
        'pos': 100,
    },

    # Forums
    'forums': {
        'name': _('Forums'),
        'icon': 'comment',
        'pos': 200,
    },

    # Permissions
    'permissions': {
        'name': _('Permissions'),
        'icon': 'adjust',
        'pos': 300,
    },

    # System
    'system': {
        'name': _('System'),
        'icon': 'wrench',
        'pos': 400,
    },
}
