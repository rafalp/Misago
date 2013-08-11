from misago.utils.fixtures import load_settings_fixture, update_settings_fixture
from misago.utils.translation import ugettext_lazy as _

settings_fixture = (
   # Basic options
   ('basic', {
        'name': _("Basic Settings"),
        'settings': (
            ('board_name', {
                'value':        "Misago",
                'type':         "string",
                'input':        "text",
                'separator':    _("Board Name"),
                'name':         _("Board Name"),
            }),
            ('board_header', {
                'type':         "string",
                'input':        "text",
                'name':         _("Board Header"),
                'description':  _("Some themes allow you to define text in board header. Leave empty to use Board Name instead."),
            }),
            ('board_header_postscript', {
                'value':        "Work in progress",
                'type':         "string",
                'input':        "text",
                'name':         _("Board Header Postscript"),
                'description':  _("Additional text displayed in some themes board header after board name."),
            }),
            ('board_index_title', {
                'type':         "string",
                'input':        "text",
                'separator':    _("Board Index"),
                'name':         _("Board Index Title"),
                'description':  _("If you want to, you can replace page title content on Board Index with custom one."),
            }),
            ('board_index_meta', {
                'type':         "string",
                'input':        "text",
                'name':         _("Board Index Meta-Description"),
                'description':  _("Meta-Description used to describe your board's index page."),
            }),
            ('board_credits', {
                'type':         "string",
                'input':        "textarea",
                'separator':    _("Board Footer"),
                'name':         _("Custom Credit"),
                'description':  _("Custom Credit to display in board footer above software and theme copyright information. You can use HTML."),
            }),
            ('email_footnote', {
                'type':         "string",
                'input':        "textarea",
                'separator':    _("Board E-Mails"),
                'name':         _("Custom Footnote in HTML E-mails"),
                'description':  _("Custom Footnote to display in HTML e-mail messages sent by board."),
            }),
            ('email_footnote_plain', {
                'type':         "string",
                'input':        "textarea",
                'name':         _("Custom Footnote in plain text E-mails"),
                'description':  _("Custom Footnote to display in plain text e-mail messages sent by board."),
            }),
        ),
   }),
)


def load():
    load_settings_fixture(settings_fixture)


def update():
    update_settings_fixture(settings_fixture)
