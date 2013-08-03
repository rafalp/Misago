from misago.utils.fixtures import load_settings_fixture, update_settings_fixture
from misago.utils.translation import ugettext_lazy as _

settings_fixture = (
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
                'value':        100,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 5, 'max': 100},
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
                'value':        False,
                'type':         "boolean",
                'input':        "yesno",
                'name':         _("Display avatars on threads list"),
                'description':  _("Unlike basic user data, avatars are not cached - turning this option on will cause one extra query on threads lists."),
            }),
            ('thread_ranking_type', {
                'value':        "last",
                'type':         "string",
                'input':        "choice",
                'extra':        {'choices': [('none', _("Disabled")), ('popular', _("Popularity")), ('last', _("Last Reply")), ('start', _("Start Date"))]},
                'separator':    _("Thread List on Board Index"),
                'name':         _('List Type'),
                'description':  _('Different types are useful by different boards. If your board is extremly active, use "Popularity", otherwhise select either "Last Reply" or "Start Date"'),
            }),
            ('thread_ranking_size', {
                'value':        6,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 1, 'max': 30},
                'name':         _('Number of threads on list'),
                'description':  _('Enter number of threads to be displayed on threads list on board index.'),
            }),
            ('thread_ranking_refresh', {
                'value':        60,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 0},
                'name':         _('Ranking Update Frequency'),
                'description':  _('Enter minimum of number of minutes between ranking updates or zero to update ranking on every request - strongly discouraged for active forums.'),
            }),
            ('thread_ranking_initial_score', {
                'value':        30,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 0},
                'name':         _('Initial Thread Score'),
                'description':  _("Initial Thread Score helps new threads overtake old threads in ranking."),
            }),
            ('thread_ranking_reply_score', {
                'value':        5,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 0},
                'name':         _('New Reply Score'),
                'description':  _("Only replies visible to all members increase thread inflation."),
            }),
            ('thread_ranking_inflation', {
                'value':        20,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 0, 'max': 99},
                'name':         _('Score inflation'),
                'description':  _("Thread popularity system requires inflation to be defined in order to be effective. updatethreadranking task will lower thread scores by percent defined here on every launch. For example, if you enter 5, thread scores will be lowered by 5%% on every update. Enter zero to disable inflation."),
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


def load():
    load_settings_fixture(settings_fixture)


def update():
    update_settings_fixture(settings_fixture)
