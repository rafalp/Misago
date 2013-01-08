from misago.settings.fixtures import load_settings_fixture, update_settings_fixture
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid

settings_fixtures = (
    # Register and Sign-In Settings
    ('brute-force', {
        'name': _("Brute-force Countermeasures"),
        'description': _("Those settings allow you to protect your forum from brute-force attacks."),
        'settings': (
            ('attempts_limit', {
                'value':        3,
                'default':      3,
                'type':         "integer",
                'input':        "text",
                'separator':    _("Brute-force Countermeasures"),
                'name':         _("IP invalid attempts limit"),
                'description':  _('Enter maximal number of allowed attempts before IP address "jams". Defautly forum records only failed sign-in attempts.'),
            }),
            ('registrations_jams', {
                'value':        False,
                'default':      False,
                'type':         "boolean",
                'input':        "yesno",
                'name':         _("Protect register form"),
                'description':  _("Set this setting to yes if you want failed register attempts to count into limit. Majority of failed register attempts are caused by CAPTCHA protection against spam-bots, however same protection may cause problems for users with disabilities or ones that have problems understanding Q&A challenge."),
            }),
            ('jams_lifetime', {
                'value':        15,
                'default':      15,
                'type':         "integer",
                'input':        "text",
                'name':         _("Automaticaly unlock jammed IPs"),
                'description':  _('Enter number of minutes since IP address "jams" to automatically unlock it, or 0 to never unlock jammed IP adresses. Jams don\'t count as bans.'),
            }),
        ),
    }),
)


def load_fixtures():
    load_settings_fixture(settings_fixtures)


def update_fixtures():
    update_settings_fixture(settings_fixtures)
