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
    # Register and Sign-In Settings
    ('register-and-signin', {
        'name': _("Register and Sign-In Settings"),
        'description': _("Those settings allow you to increase security of your members accounts."),
        'settings': (
            ('account_activation', {
                'type':         "string",
                'input':        "choice",
                'extra':        {'choices': [('', _("No validation required")), ('user', _("Activation Token sent to User")), ('admin', _("Activation by Administrator")), ('block', _("Dont allow new registrations"))]},
                'separator':    _("Users Registrations"),
                'name':         _("New accounts validation"),
            }),
            ('default_timezone', {
                'value':        "utc",
                'type':         "string",
                'input':        "select",
                'extra':        {'choices': '#TZ#'},
                'name':         _("Default Timezone"),
                'description':  _("Used by guests, crawlers and newly registered users."),
            }),
            ('password_length', {
                'value':        4,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 1},
                'separator':    _("Users Passwords"),
                'name':         _("Minimum user password length"),
            }),
            ('password_complexity', {
                'value':        [],
                'type':         "array",
                'input':        "mlist",
                'extra':        {'choices': [('case', _("Require mixed Case")), ('digits', _("Require digits")), ('special', _("Require special characters"))]},
                'name':         _("Password Complexity"),
            }),
            ('password_lifetime', {
                'value':        0,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 0},
                'name':         _("Password Lifetime"),
                'description':  _("Enter number of days since password was set to force member to change it with new one, or 0 to dont force your members to change their passwords."),
            }),
            ('sessions_hidden', {
                'value':        True,
                'type':         "boolean",
                'input':        "yesno",
                'separator':    _("Sessions Settings"),
                'name':         _("Allow hidden sessions"),
                'description':  _("Enabling this option will allow users to hide their presence on forums from other members."),
            }),
            ('sessions_validate_ip', {
                'value':        True,
                'type':         "boolean",
                'input':        "yesno",
                'name':         _("Check IP on session authorization"),
                'description':  _("Makes sessions more secure, but can cause problems with proxies and VPN's."),
            }),
            ('remember_me_allow', {
                'value':        True,
                'type':         "boolean",
                'input':        "yesno",
                'separator':    _("Sign-In Settings"),
                'name':         _('Enable "Remember Me" functionality'),
                'description':  _("Turning this option on allows users to sign in on to your board using cookie-based tokens. This may result in account compromisation when user fails to sign out on shared computer."),
            }),
            ('remember_me_lifetime', {
                'value':        90,
                'type':         "integer",
                'input':        "text",
                'name':         _('"Remember Me" token lifetime'),
                'description':  _('Number of days since either last use or creation of "Remember Me" token to its expiration.'),
            }),
            ('remember_me_extensible', {
                'value':        1,
                'type':         "boolean",
                'input':        "yesno",
                'name':         _('Allow "Remember Me" tokens refreshing'),
                'description':  _('Set this setting to off if you want to force your users to periodically update their "Remember Me" tokens by signing in. If this option is on, Tokens are updated when they are used to open new session.'),
            }),
            ('login_attempts_limit', {
                'value':        3,
                'default':      3,
                'type':         "integer",
                'input':        "text",
                'separator':    _("Brute-Force Countermeasures"),
                'name':         _("Limit Sign In attempts"),
                'description':  _('Enter maximal number of allowed Sign In attempts before IP address "jams".'),
            }),
            ('registrations_jams', {
                'value':        1,
                'default':      1,
                'type':         "boolean",
                'input':        "yesno",
                'name':         _("Count failed register attempts too"),
                'description':  _("Set this setting to yes if you want failed register attempts to count into limit."),
            }),
            ('jams_lifetime', {
                'value':        15,
                'default':      15,
                'type':         "integer",
                'input':        "text",
                'name':         _("Automaticaly unlock jammed IPs"),
                'description':  _('Enter number of minutes since IP address "jams" to automatically unlock it, or 0 to never unlock jammed IP adresses. Jams dont count as bans.'),
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