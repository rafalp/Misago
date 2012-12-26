from misago.monitor.fixtures import load_monitor_fixture
from misago.settings.fixtures import load_settings_fixture, update_settings_fixture
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid

monitor_fixtures = {
                  'threads': 0,
                  'posts': 0,
                  }


settings_fixtures = (
    # Threads Settings
    ('threads', {
         'name': _("Threads and Posts Settings"),
         'description': _("Those settings control your forum's threads and posts."),
         'settings': (
            ('thread_name_min', {
                'value':        4,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 1},
                'separator':    _("Threads"),
                'name':         _("Min. Thread Name Length"),
                'description':  _('Minimal allowed thread name length.'),
            }),
            ('thread_name_max', {
                'value':        35,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 5, 'max': 60},
                'name':         _("Max. Thread Name Length"),
                'description':  _('Maximum allowed thread name length.'),
            }),
            ('threads_per_page', {
                'value':        40,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 5},
                'name':         _("Threads per page"),
                'description':  _("Number of threads displayed on page in forum view."),
            }),
            ('avatars_on_threads_list', {
                'value':        True,
                'type':         "boolean",
                'input':        "yesno",
                'name':         _("Display avatars on threads list"),
                'description':  _("Unlike basic user data, avatars are not cached - turning this option on will cause one extra query on threads lists."),
            }),
            ('post_length_min', {
                'value':        5,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 5},
                'separator':    _("Posts"),
                'name':         _("Min. Post Length"),
                'description':  _("Minimal allowed post length."),
            }),
            ('post_merge_time', {
                'value':        5,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 0},
                'name':         _("Automatic Post Merge timespan"),
                'description':  _("Forum can automatically merge member posts if interval between postings is shorter than specified number of minutes."),
            }),
            ('posts_per_page', {
                'value':        15,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 5},
                'name':         _("Posts per page"),
                'description':  _("Number of posts per page in thread view."),
            }),
            ('thread_length', {
                'value':        300,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 0},
                'name':         _("Thread Length Limit"),
                'description':  _('Long threads are hard to follow and search. You can force users to create few shorter threads instead of one long by setting thread lenght limits. Users with "Can close threads" permission will still be able to post in threads that have reached posts limit.'),
            }),
       ),
    }),
)


def load_fixtures():
    load_monitor_fixture(monitor_fixtures)
    load_settings_fixture(settings_fixtures)
    
    
def update_fixtures():
    update_settings_fixture(settings_fixtures)