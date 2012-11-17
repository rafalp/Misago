from misago.settings.fixtures import load_settings_fixture
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid

settings_fixtures = (
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
    load_settings_fixture(settings_fixtures)