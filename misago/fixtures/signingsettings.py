from misago.utils.fixtures import load_settings_fixture, update_settings_fixture
from misago.utils.translation import ugettext_lazy as _

settings_fixture = (
    # Register and Sign-In Settings
    ('signin', {
        'name': _("Sign-In and Sessions Settings"),
        'description': _("Those settings control behaviour of signed-in accounts."),
        'settings': (
            ('sessions_validate_ip', {
                'value':        True,
                'type':         "boolean",
                'input':        "yesno",
                'separator':    _("Sessions Settings"),
                'name':         _("Check IP on session authorization"),
                'description':  _("Makes sessions more secure, but can cause problems with proxies and VPN's."),
            }),
            ('sessions_tracker_sync_frequency', {
                'value':        300,
                'type':         "integer",
                'input':        "text",
                'extra':         {'min': 15},
                'name':         _("Online Tracker Updates Frequency"),
                'description':  _("How often do you want online tracker to synchronize itself with database? Low numbers provide good accuracy at cost of database traffic while great number provides your users with general idea how many are currently online while at same time keeping stress off your database."),
            }),
            ('remember_me_allow', {
                'value':        True,
                'type':         "boolean",
                'input':        "yesno",
                'separator':    _('"Remember Me" Feature'),
                'name':         _('Enable "Remember Me" feature'),
                'description':  _("Turning this option on allows users to sign in on to your board using cookie-based tokens. This may result in account compromisation when user fails to sign out on shared computer or his cookie is stolen."),
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
        ),
    }),
)


def load():
    load_settings_fixture(settings_fixture)


def update():
    update_settings_fixture(settings_fixture)