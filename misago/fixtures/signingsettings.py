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
            ('online_counting', {
                'value':        "real",
                'type':         "string",
                'input':        "choice",
                'extra':        {'choices': [('no', _("Don't count users online")), ('snap', _("Periodically count and cache onlines")), ('real', _("Real time"))]},
                'separator':    _("Online Counting"),
                'name':         _("Count and display number of users online on board index."),
                'description':  _("Online counter helps members tell how active other members are at the moment. Large forums should use periodical counting that saves resources but is not accurate while small ones can use real time counting that offers complete accuracy without putting much stress on sessions table."),
            }),
            ('online_counting_frequency', {
                'value':        300,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 1},
                'name':         _("Cache expiration"),
                'description':  _('If you are using cache to count number of users online, here you can enter number of seconds after which cache is marked as expired and refreshed with new data.'),
            }),
        ),
    }),
)


def load():
    load_settings_fixture(settings_fixture)


def update():
    update_settings_fixture(settings_fixture)