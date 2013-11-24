from misago.utils.fixtures import load_settings_fixture, update_settings_fixture
from misago.utils.translation import ugettext_lazy as _

settings_fixture = (
    # Threads Settings
    ('private-threads', {
         'name': _("Private Threads Settings"),
         'description': _("Those settings control your forum's private threads."),
         'settings': (
            ('enable_private_threads', {
                'value':        True,
                'type':         "boolean",
                'input':        "yesno",
                'separator':    _("Private Threads"),
                'name':         _("Enable Private Threads"),
            }),
       ),
    }),
)


def load():
    load_settings_fixture(settings_fixture)


def update():
    update_settings_fixture(settings_fixture)
