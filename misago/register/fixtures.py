from misago.settings.fixtures import load_settings_fixture, update_settings_fixture
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid

settings_fixtures = (
    # Register and Sign-In Settings
    ('accounts', {
        'name': _("Users Accounts Settings"),
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
        ),
    }),
)


def load_fixtures():
    load_settings_fixture(settings_fixtures)
    
    
def update_fixtures():
    update_settings_fixture(settings_fixtures)