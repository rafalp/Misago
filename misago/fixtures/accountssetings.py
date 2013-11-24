from misago.utils.fixtures import load_settings_fixture, update_settings_fixture
from misago.utils.translation import ugettext_lazy as _

settings_fixture = (
    # Register and Sign-In Settings
    ('accounts', {
        'name': _("Users Accounts Settings"),
        'description': _("Those settings allow you to increase security of your members accounts."),
        'settings': (
            ('account_activation', {
                'value':        "none",
                'type':         "string",
                'input':        "choice",
                'extra':        {'choices': [('none', _("No validation required")), ('user', _("Activation Token sent to User")), ('admin', _("Activation by Administrator")), ('block', _("Dont allow new registrations"))]},
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
            ('username_length_min', {
                'value':        3,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 3},
                'separator':    _("Users Names"),
                'name':         _("Minimum allowed username length"),
            }),
            ('username_length_max', {
                'value':        16,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 3},
                'name':         _("Maxim allowed username length"),
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
            ('password_in_email', {
                'value':        False,
                'type':         "boolean",
                'input':        "yesno",
                'name':         _("Include User Password in Welcoming E-mail"),
                'description':  _("If you want to, Misago can include new user password in welcoming e-mail that is sent to new users after successful account creation."),
            }),
            ('subscribe_start', {
                'value':        2,
                'type':         "integer",
                'input':        "select",
                'extra':        {'choices': ((0, _("Don't watch")),
                                             (1, _("Put on watched threads list")),
                                             (2, _("Put on watched threads list and e-mail user when somebody replies")),
                                             )},
                'separator':    _("Default Watching Preferences"),
                'name':         _("Watch threads user started"),
            }),
            ('subscribe_reply', {
                'value':        2,
                'type':         "integer",
                'input':        "select",
                'extra':        {'choices': ((0, _("Don't watch")),
                                             (1, _("Put on watched threads list")),
                                             (2, _("Put on watched threads list and e-mail user when somebody replies")),
                                             )},
                'name':         _("Watch threads user replied in"),
            }),
            ('profiles_per_list', {
                'value':        24,
                'type':         "integer",
                'input':        "string",
                'extra':        {'min': 1, 'max': 128},
                'separator':    _("Users List"),
                'name':         _("Number of Profiles Per Page"),
            }),
        ),
    }),
)


def load():
    load_settings_fixture(settings_fixture)
    
    
def update():
    update_settings_fixture(settings_fixture)