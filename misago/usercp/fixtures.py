from misago.settings.fixtures import load_settings_fixture, update_settings_fixture
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid

settings_fixtures = (
    # Avatars Settings
    ('avatars', {
         'name': _("Users Avatars Settings"),
         'description': _("Those settings allow you to control your users avatars."),
         'settings': (
            ('avatars_types', {
                'value':        ['gravatar', 'gallery'],
                'type':         "array",
                'input':        "mlist",
                'extra':        {'choices': [('gravatar', _("Gravatar")), ('upload', _("Uploaded Avatar")), ('gallery', _("Avatars Gallery"))]},
                'separator':    _("General Settings"),
                'name':         _("Allowed Avatars"),
                'description':  _("Select Avatar types allowed on your forum."),
            }),
            ('default_avatar', {
                'value':        "gravatar",
                'type':         "string",
                'input':        "select",
                'extra':        {'choices': [('gravatar', _("Gravatar")), ('gallery', _("Random Avatar from Gallery"))]},
                'name':         _("Default Avatar"),
                'description':  _("Default Avatar assigned to new members. If you creade directory and name it \"_default\", forum will select random avatar from that directory instead of regular gallery. If no avatar can be picked from gallery, Gravatar will be used."),
            }),
            ('upload_limit', {
                'value':        128,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 0},
                'separator':    _("Avatar Upload Settings"),
                'name':         _("Maxmimum size of uploaded file"),
                'description':  _("Select maximum allowed file size (in KB) for Avatar uploads."),
            }),
       ),
    }),
)


def load_fixtures():
    load_settings_fixture(settings_fixtures)


def update_fixtures():
    update_settings_fixture(settings_fixtures)
