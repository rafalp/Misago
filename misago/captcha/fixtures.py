from misago.settings.fixtures import load_settings_fixture, update_settings_fixture
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid


settings_fixtures = (
   # Spam Countermeasures
   ('spam', {
        'name': _("Spam Countermeasures"),
        'description': _("Those settings allow you to combat automatic registrations and spam messages on your forum."),
        'settings': (
            ('bots_registration', {
                'type':         "string",
                'input':        "choice",
                'extra':        {'choices': [('', _("No protection")), ('recaptcha', _("reCaptcha")), ('qa', _("Question & Answer"))]},
                'separator':    _("Spambots Registrations"),
                'name':         _("CAPTCHA type"),
                'description':  _('CAPTCHA stands for "Completely Automated Public Turing test to tell Computers and Humans Apart". Its type of test developed on purpose of blocking automatic registrations.'),
                'position':     0,
            }),
            ('recaptcha_public', {
                'type':         "string",
                'input':        "text",
                'separator':    _("reCaptcha"),
                'name':         _("Public Key"),
                'description':  _("Enter public API key that you have received from reCaptcha."),
                'position':     1,
            }),
            ('recaptcha_private', {
                'type':         "string",
                'input':        "text",
                'name':         _("Private Key"),
                'description':  _("Enter private API key that you have received from reCaptcha."),
                'position':     2,
            }),
            ('recaptcha_ssl', {
                'value':        False,
                'type':         "boolean",
                'input':        "yesno",
                'name':         _("Use SSL in reCaptcha"),
                'description':  _("Do you want forum to use SSL when making requests to reCaptha servers?"),
                'position':     3,
            }),
            ('qa_test', {
                'type':         "string",
                'input':        "text",
                'separator':    _("Question and Answer Test"),
                'name':         _("Question"),
                'description':  _("Question visible to your users."),
                'position':     4,
            }),
            ('qa_test_help', {
                'type':         "string",
                'input':        "text",
                'name':         _("Help Message"),
                'description':  _("Optional help message displayed on form."),
                'position':     5,
            }),
            ('qa_test_answers', {
                'type':         "string",
                'input':        "textarea",
                'name':         _("Answers"),
                'description':  _("Enter allowed answers to this question, each in new line. Test is case-insensitive."),
                'position':     6,
            }),
        ),
    }),
)


def load_fixtures():
    load_settings_fixture(settings_fixtures)


def update_fixtures():
    update_settings_fixture(settings_fixtures)