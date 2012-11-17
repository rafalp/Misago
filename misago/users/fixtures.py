from misago.monitor.fixtures import load_monitor_fixture
from misago.settings.fixtures import load_settings_fixture
from misago.users.models import Rank, Group
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid

monitor_fixtures = {
                  'users': 0,
                  'users_inactive': 0,
                  'users_reported': 0,
                  'last_user': None,
                  'last_user_name': None,
                  'last_user_slug': None,
                  }

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

def load_fixture():
    load_monitor_fixture(monitor_fixtures)
    load_settings_fixture(settings_fixtures)
    
    rank_staff = Rank(
                      name=_("Forum Staff").message,
                      style='staff',
                      title=_("Forum Staff").message,
                      special=True,
                      order=1,
                      )
    rank_guest = Rank(
                      name=_("Unregistered").message,
                      style='guest',
                      title=_("Guest").message,
                      special=True,
                      order=2,
                      )
    rank_lurker = Rank(
                      name=_("Lurker").message,
                      style='lurker',
                      title=_("Lurker").message,
                      order=3,
                      criteria=0
                      )
    rank_member = Rank(
                      name=_("Member").message,
                      title=_("Member").message,
                      order=4,
                      criteria=">15"
                      )
    rank_active = Rank(
                      name=_("Active Member").message,
                      title=_("Active Member").message,
                      order=5,
                      criteria="15%"
                      )
    
    rank_staff.save(force_insert=True)
    rank_guest.save(force_insert=True)
    rank_lurker.save(force_insert=True)
    rank_member.save(force_insert=True)
    rank_active.save(force_insert=True)
    
    group_admins = Group(
                         name=_("Administrators").message,
                         name_slug='administrators',
                         tab=_("Staff").message,
                         position=1,
                         rank=rank_staff,
                         special=True,
                         )
    group_mods = Group(
                       name=_("Moderators").message,
                       name_slug='moderators',
                       tab=_("Staff").message,
                       position=2,
                       rank=rank_staff,
                       )
    group_registered = Group(
                         name=_("Registered").message,
                         name_slug='registered',
                         hidden=True,
                         position=3,
                         special=True,
                         )
    group_guests = Group(
                         name=_("Guests").message,
                         name_slug='guests',
                         hidden=True,
                         position=4,
                         rank=rank_guest,
                         special=True,
                         )
    group_crawlers = Group(
                           name=_("Web Crawlers").message,
                           name_slug='web-crawlers',
                           hidden=True,
                           position=5,
                           rank=rank_guest,
                           special=True,
                           )
    
    group_admins.save(force_insert=True)
    group_mods.save(force_insert=True)
    group_registered.save(force_insert=True)
    group_guests.save(force_insert=True)
    group_crawlers.save(force_insert=True)    