from misago.ranks.models import Rank
from misago.settings.fixtures import load_settings_fixture, update_settings_fixture
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid


settings_fixtures = (
    # Users Ranking Settings
    ('ranking', {
        'name': _("Members Ranking"),
        'description': _("Those settings control mechanisms of members activity ranking which allows you to gamificate your forum."),
        'settings': (
            ('ranking_inflation', {
                'value':        5,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 0, 'max': 99},
                'separator':    _("Basic Ranking Settings"),
                'name':         _("Ranking Inflation"),
                'description':  _("Enter size of ranking scores inflation in percent. Scores inflation is important mechanism that allows ranking self-regulation, punishing inactivity and requiring users to remain active in order to remain high in ranking."),
            }),
            ('ranking_positions_visible', {
                'value':        True,
                'type':         "boolean",
                'input':        "yesno",
                'name':         _("Dont Keep Users Scores Secret"),
                'description':  _("Changing this to yes will cause forum to display user position in ranking on his profile page."),
            }),
            ('ranking_scores_visible', {
                'value':        True,
                'type':         "boolean",
                'input':        "yesno",
                'name':         _("Dont Keep Users Scores Secret"),
                'description':  _("Changing this to yes will cause forum to display user score on his profile page."),
            }),
            ('score_reward_new_thread', {
                'value':        50,
                'type':         "integer",
                'input':        "text",
                'separator':    _("Posting Rewards"),
                'name':         _("New Thread Reward"),
                'description':  _("Score user will receive (or lose) whenever he posts new thread."),
            }),
            ('score_reward_new_post', {
                'value':        100,
                'type':         "integer",
                'input':        "text",
                'name':         _("New Reply Reward"),
                'description':  _("Score user will receive (or lose) whenever he posts new reply in thread."),
            }),
            ('score_reward_new_post_cooldown', {
                'value':        180,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 0},
                'name':         _("Reward Cooldown"),
                'description':  _("Minimal time (in seconds) that has to pass between postings for new message to receive karma vote. This is useful to combat flood."),
            }),
            ('score_reward_karma_positive', {
                'value':        20,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 0},
                'separator':    _("Karma System"),
                'name':         _("Upvote Reward"),
                'description':  _("Score user will receive every time his post receives upvote."),
            }),
            ('score_reward_karma_negative', {
                'value':        10,
                'type':         "integer",
                'input':        "text",
                'extra':        {'min': 0},
                'name':         _("Downvote Punishment"),
                'description':  _("Score user will lose every time his post receives downvote."),
            }),
        ),
    }),
)


def load_fixtures():
    load_settings_fixture(settings_fixtures)
    Rank.objects.create(
                        name=_("Forum Team").message,
                        name_slug='forum-team',
                        title=_("Forum Team").message,
                        style='rank-team',
                        special=True,
                        order=0,
                        as_tab=True,
                        on_index=True,
                        )

    Rank.objects.create(
                        name=_("Most Valuable Posters").message,
                        name_slug='most-valuable-posters',
                        title=_("MVP").message,
                        style='rank-mvp',
                        special=True,
                        order=1,
                        as_tab=True,
                        )

    Rank.objects.create(
                        name=_("Lurkers").message,
                        name_slug='lurkers',
                        order=1,
                        criteria="100%"
                        )

    Rank.objects.create(
                        name=_("Members").message,
                        name_slug='members',
                        order=2,
                        criteria="75%"
                        )

    Rank.objects.create(
                        name=_("Active Members").message,
                        name_slug='active-members',
                        style='rank-active',
                        order=3,
                        criteria="10%",
                        as_tab=True,
                        )


def update_fixtures():
    update_settings_fixture(settings_fixtures)
