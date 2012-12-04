from misago.monitor.fixtures import load_monitor_fixture
from misago.settings.fixtures import load_settings_fixture, update_settings_fixture
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
                'position':     0,
            }),
            ('default_avatar', {
                'value':        "gravatar",
                'type':         "string",
                'input':        "select",
                'extra':        {'choices': [('gravatar', _("Gravatar")), ('gallery', _("Random Avatar from Gallery"))]},
                'name':         _("Default Avatar"),
                'description':  _("Default Avatar assigned to new members. If you creade directory and name it \"_default\", forum will select random avatar from that directory instead of regular gallery. If no avatar can be picked from gallery, Gravatar will be used."),
                'position':     1,
            }),
            ('upload_limit', {
                'value':        128,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 0},
                'separator':    _("Avatar Upload Settings"),
                'name':         _("Maxmimum size of uploaded file"),
                'description':  _("Select maximum allowed file size (in KB) for Avatar uploads."),
                'position':     2,
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
                'position':     0,
            }),
            ('default_timezone', {
                'value':        "utc",
                'type':         "string",
                'input':        "select",
                'extra':        {'choices': '#TZ#'},
                'name':         _("Default Timezone"),
                'description':  _("Used by guests, crawlers and newly registered users."),
                'position':     1,
            }),
            ('password_length', {
                'value':        4,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 1},
                'separator':    _("Users Passwords"),
                'name':         _("Minimum user password length"),
                'position':     2,
            }),
            ('password_complexity', {
                'value':        [],
                'type':         "array",
                'input':        "mlist",
                'extra':        {'choices': [('case', _("Require mixed Case")), ('digits', _("Require digits")), ('special', _("Require special characters"))]},
                'name':         _("Password Complexity"),
                'position':     3,
            }),
            ('password_lifetime', {
                'value':        0,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 0},
                'name':         _("Password Lifetime"),
                'description':  _("Enter number of days since password was set to force member to change it with new one, or 0 to dont force your members to change their passwords."),
                'position':     4,
            }),
            ('password_in_email', {
                'value':        False,
                'type':         "boolean",
                'input':        "yesno",
                'name':         _("Include User Password in Welcoming E-mail"),
                'description':  _("If you want to, Misago can include new user password in welcoming e-mail that is sent to new users after successful account creation."),
                'position':     5,
            }),
            ('sessions_validate_ip', {
                'value':        True,
                'type':         "boolean",
                'input':        "yesno",
                'name':         _("Check IP on session authorization"),
                'description':  _("Makes sessions more secure, but can cause problems with proxies and VPN's."),
                'position':     6,
            }),
            ('remember_me_allow', {
                'value':        True,
                'type':         "boolean",
                'input':        "yesno",
                'separator':    _("Sign-In Settings"),
                'name':         _('Enable "Remember Me" functionality'),
                'description':  _("Turning this option on allows users to sign in on to your board using cookie-based tokens. This may result in account compromisation when user fails to sign out on shared computer."),
                'position':     7,
            }),
            ('remember_me_lifetime', {
                'value':        90,
                'type':         "integer",
                'input':        "text",
                'name':         _('"Remember Me" token lifetime'),
                'description':  _('Number of days since either last use or creation of "Remember Me" token to its expiration.'),
                'position':     8,
            }),
            ('remember_me_extensible', {
                'value':        1,
                'type':         "boolean",
                'input':        "yesno",
                'name':         _('Allow "Remember Me" tokens refreshing'),
                'description':  _('Set this setting to off if you want to force your users to periodically update their "Remember Me" tokens by signing in. If this option is on, Tokens are updated when they are used to open new session.'),
                'position':     9,
            }),
            ('login_attempts_limit', {
                'value':        3,
                'default':      3,
                'type':         "integer",
                'input':        "text",
                'separator':    _("Brute-Force Countermeasures"),
                'name':         _("Limit Sign In attempts"),
                'description':  _('Enter maximal number of allowed Sign In attempts before IP address "jams".'),
                'position':     10,
            }),
            ('registrations_jams', {
                'value':        1,
                'default':      1,
                'type':         "boolean",
                'input':        "yesno",
                'name':         _("Count failed register attempts too"),
                'description':  _("Set this setting to yes if you want failed register attempts to count into limit."),
                'position':     11,
            }),
            ('jams_lifetime', {
                'value':        15,
                'default':      15,
                'type':         "integer",
                'input':        "text",
                'name':         _("Automaticaly unlock jammed IPs"),
                'description':  _('Enter number of minutes since IP address "jams" to automatically unlock it, or 0 to never unlock jammed IP adresses. Jams dont count as bans.'),
                'position':     12,
            }),
        ),
    }),
)


def load_fixtures():
    load_monitor_fixture(monitor_fixtures)
    load_settings_fixture(settings_fixtures)
    
    
def update_fixtures():
    update_settings_fixture(settings_fixtures)